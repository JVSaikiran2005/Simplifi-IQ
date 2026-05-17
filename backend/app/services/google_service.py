import json
from pathlib import Path
from typing import Any

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from ..config import settings


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]


def load_google_credentials() -> Credentials | None:
    if not settings.GOOGLE_SERVICE_ACCOUNT_FILE:
        return None

    service_account_ref = settings.GOOGLE_SERVICE_ACCOUNT_FILE.strip()
    if service_account_ref.startswith("{"):
        data = json.loads(service_account_ref)
        return Credentials.from_service_account_info(data, scopes=SCOPES)

    file_path = Path(service_account_ref)
    if not file_path.exists():
        return None

    return Credentials.from_service_account_file(str(file_path), scopes=SCOPES)


def log_lead_to_google_sheets(lead_id: int, lead_data: dict[str, Any], report_path: str, status: str) -> None:
    if not settings.GOOGLE_SHEETS_ID:
        return

    credentials = load_google_credentials()
    if not credentials:
        return

    try:
        service = build("sheets", "v4", credentials=credentials)
        sheet = service.spreadsheets()
        row = [
            lead_id,
            lead_data.get("full_name", ""),
            lead_data.get("email", ""),
            lead_data.get("company_name", ""),
            lead_data.get("company_website", ""),
            status,
            report_path,
            lead_data.get("scrape_error", ""),
        ]
        sheet.values().append(
            spreadsheetId=settings.GOOGLE_SHEETS_ID,
            range="Sheet1!A:H",
            valueInputOption="RAW",
            body={"values": [row]},
        ).execute()
    except Exception:
        pass


def archive_report_to_google_drive(pdf_path: str, lead_id: int, company_name: str) -> None:
    if not settings.GOOGLE_DRIVE_FOLDER_ID:
        return

    credentials = load_google_credentials()
    if not credentials:
        return

    try:
        service = build("drive", "v3", credentials=credentials)
        file_metadata = {
            "name": f"lead_{lead_id}_{company_name.lower().replace(' ', '_')}.pdf",
            "parents": [settings.GOOGLE_DRIVE_FOLDER_ID],
        }
        media = MediaFileUpload(pdf_path, mimetype="application/pdf")
        service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    except Exception:
        pass
