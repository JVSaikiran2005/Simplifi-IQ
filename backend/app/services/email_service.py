import base64
from pathlib import Path
from typing import Optional

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Attachment, Content, Email, Mail

from ..config import settings


def build_email_message(sender: str, recipient: str, subject: str, plain_text: str, html_content: str, attachment_path: Optional[str] = None) -> Mail:
    message = Mail(
        from_email=Email(sender),
        to_emails=recipient,
        subject=subject,
        plain_text_content=Content("text/plain", plain_text),
        html_content=Content("text/html", html_content),
    )

    if settings.SENDGRID_REPLY_TO:
        message.reply_to = Email(settings.SENDGRID_REPLY_TO)

    if attachment_path:
        with open(attachment_path, "rb") as f:
            file_data = f.read()
        encoded = base64.b64encode(file_data).decode()
        attached_file = Attachment()
        attached_file.file_content = encoded
        attached_file.file_type = "application/pdf"
        attached_file.file_name = Path(attachment_path).name
        attached_file.disposition = "attachment"
        message.add_attachment(attached_file)

    return message


def send_report_email(full_name: str, recipient_email: str, company_name: str, pdf_path: str) -> None:
    if settings.email_provider != "sendgrid":
        raise RuntimeError("No email provider configured. Set SENDGRID_API_KEY for SendGrid delivery.")

    subject = f"{company_name} digital maturity audit & growth brief"
    plain_text = (
        f"Hi {full_name},\n\n"
        "I prepared a short audit and recommendation brief for your website. "
        "Please find the attached PDF and let me know if you want a follow-up conversation.\n\n"
        "Best regards,\nYour growth advisor"
    )
    html_content = (
        f"<p>Hi {full_name},</p>"
        f"<p>I have prepared a professional audit report for <strong>{company_name}</strong>. "
        "The attached PDF includes an executive summary, digital maturity review, UX observations, SEO opportunities, and AI automation ideas.</p>"
        "<p>If you want, I can help turn these recommendations into a short execution plan.</p>"
        "<p>Best regards,<br/>Your growth advisor</p>"
    )

    message = build_email_message(
        sender=settings.SENDGRID_FROM_EMAIL,
        recipient=recipient_email,
        subject=subject,
        plain_text=plain_text,
        html_content=html_content,
        attachment_path=pdf_path,
    )
    client = SendGridAPIClient(settings.SENDGRID_API_KEY)
    response = client.send(message)
    if response.status_code >= 400:
        raise RuntimeError(f"Email send failed with status {response.status_code}: {response.body}")
