from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .db import fetch_lead_by_id, initialize_database, insert_lead, update_lead_status
from .schemas import ApiResponse, LeadCreate, LeadStatusResponse
from .services.ai_engine import generate_company_analysis
from .services.email_service import send_report_email
from .services.enrichment import enrich_company_profile
from .services.google_service import archive_report_to_google_drive, log_lead_to_google_sheets
from .services.pdf_generator import build_pdf


app = FastAPI(
    title="AI Lead Audit Automation",
    description="Backend API for lead intake, enrichment, AI audit report generation, PDF export, and email delivery.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    initialize_database()
    Path(settings.REPORT_DIR).mkdir(parents=True, exist_ok=True)


def process_lead_workflow(lead_id: int, lead: LeadCreate) -> None:
    try:
        enriched = enrich_company_profile(lead.company_name, lead.company_website, lead.email)
        analysis = generate_company_analysis(lead.company_name, enriched["company_website"], lead.email, enriched)

        report_name = f"lead_{lead_id}_{lead.company_name.lower().replace(' ', '_')}.pdf"
        report_path = Path(settings.REPORT_DIR) / report_name
        pdf_location = build_pdf(str(report_path), {**lead.dict(), **enriched}, analysis)

        if settings.email_provider == "sendgrid":
            send_report_email(lead.full_name, lead.email, lead.company_name, pdf_location)

        log_lead_to_google_sheets(lead_id, {**lead.dict(), **enriched}, pdf_location, "completed")
        archive_report_to_google_drive(pdf_location, lead_id, lead.company_name)

        update_lead_status(lead_id, status="completed", report_path=pdf_location)
    except Exception as exc:
        update_lead_status(lead_id, status="failed", error=str(exc))


@app.post("/api/leads", response_model=ApiResponse)
def submit_lead(lead: LeadCreate, background_tasks: BackgroundTasks) -> ApiResponse:
    try:
        lead_id = insert_lead(lead.full_name, lead.email, lead.company_name, str(lead.company_website))
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Unable to log lead: {error}")

    background_tasks.add_task(process_lead_workflow, lead_id, lead)
    return ApiResponse(
        message="Lead received and processing has started. You can check lead status after a few moments.",
        lead_id=lead_id,
    )


@app.get("/api/leads/{lead_id}", response_model=LeadStatusResponse)
def read_lead_status(lead_id: int) -> LeadStatusResponse:
    record = fetch_lead_by_id(lead_id)
    if not record:
        raise HTTPException(status_code=404, detail="Lead not found.")
    return LeadStatusResponse(**record)
