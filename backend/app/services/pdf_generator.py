from datetime import datetime
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def build_pdf(report_path: str, lead_data: dict, analysis: dict) -> str:
    report_file = Path(report_path)
    report_file.parent.mkdir(parents=True, exist_ok=True)

    title_style = ParagraphStyle(
        name="Title",
        fontSize=24,
        leading=28,
        spaceAfter=16,
        alignment=1,
    )
    heading_style = ParagraphStyle(
        name="Heading",
        fontSize=14,
        leading=18,
        spaceBefore=14,
        spaceAfter=8,
        textColor=colors.HexColor("#1f2937"),
    )
    body_style = ParagraphStyle(
        name="Body",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#111827"),
    )

    document = SimpleDocTemplate(str(report_file), pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    content = []

    content.append(Paragraph(f"{lead_data['company_name']} Audit & Growth Brief", title_style))
    content.append(Paragraph(f"Prepared for {lead_data['full_name']} | {lead_data['email']}", body_style))
    content.append(Spacer(1, 0.2 * inch))
    content.append(Paragraph(f"Website: {lead_data['company_website']}", body_style))
    content.append(Paragraph(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", body_style))
    content.append(Spacer(1, 0.4 * inch))

    sections = [
        ("Company Snapshot", [
            f"Company: {lead_data['company_name']}",
            f"Website title: {lead_data.get('website_title', '')}",
            f"Meta description: {lead_data.get('website_description', '')}",
        ]),
        ("Executive Summary", [analysis.get("executive_summary", "No summary available.")]),
        ("Key Recommendations", [analysis.get("growth_recommendations", "No recommendations available.")]),
        ("AI Opportunities", [analysis.get("ai_opportunities", "No AI opportunities available.")]),
        ("UX & Conversion Insights", [analysis.get("ux_observations", "No UX observations available.")]),
        ("SEO Observations", [analysis.get("seo_observations", "No SEO observations available.")]),
        ("Conclusion", [analysis.get("conclusion", "No conclusion available.")]),
    ]

    for heading, paragraphs in sections:
        content.append(Paragraph(heading, heading_style))
        for paragraph in paragraphs:
            content.append(Paragraph(paragraph.replace("\n", "<br/>"), body_style))
            content.append(Spacer(1, 0.1 * inch))

    metrics = [
        [Paragraph("Report element", heading_style), Paragraph("Insights", heading_style)],
        [Paragraph("Digital maturity", body_style), Paragraph(analysis.get("digital_maturity", "N/A"), body_style)],
        [Paragraph("Business model clarity", body_style), Paragraph(analysis.get("business_model", "N/A"), body_style)],
    ]
    table = Table(metrics, colWidths=[2.2 * inch, 3.8 * inch], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111827")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d1d5db")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    content.append(Spacer(1, 0.2 * inch))
    content.append(table)

    document.build(content)
    return str(report_file)
