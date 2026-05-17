# Simplifi IQ

An end-to-end AI-powered lead automation system prototype for lead intake, company enrichment, AI audit report generation, PDF export, and email delivery.

## Architecture Overview

- `frontend/` - Next.js + Tailwind UI for lead submission.
- `backend/` - FastAPI backend implementing validation, scraping, AI analysis, PDF creation, email delivery, and SQLite logging.
- `backend/app/services/` - Modular services for enrichment, AI, PDF generation, and email.

## Workflow

1. Prospect submits their name, email, company, and website.
2. Backend validates input and logs the lead.
3. Website metadata is scraped and enriched.
4. AI generates a consulting-grade audit report.
5. Report is rendered to a polished PDF.
6. The PDF is emailed automatically to the prospect.
7. Submission status is stored in SQLite.

## Setup Instructions

### Backend

1. Ensure you are using Python 3.10.9 or newer. This project is compatible with Python 3.10.x.
2. Navigate to `backend/`
3. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

3. Copy environment variables:

```bash
copy .env.example .env
```

4. Add keys to `.env`:
- `OPENAI_API_KEY` — your Gemini or OpenAI-compatible API key.
- `SENDGRID_API_KEY` — your SendGrid API key.
- `SENDGRID_FROM_EMAIL` — a verified sender email address in SendGrid.
- `SENDGRID_REPLY_TO` — the email address you want replies to go to.

#### Gemini API Setup
- Create a Google Cloud project or use the Gemini-compatible OpenAI layer.
- Generate a Gemini API key from your Google Cloud console or OpenAI-compatible access.
- Set that key as `OPENAI_API_KEY`.
- If using Gemini via OpenAI compatibility, keep the same variable name and set `OPENAI_MODEL=gemini-1.5` in `.env`.

#### SendGrid Setup
1. Visit https://sendgrid.com and sign up (or log in).
2. Go to Settings > API Keys and create a new API key with `Full Access` or `Mail Send` permissions.
3. Copy the generated key and paste it into `SENDGRID_API_KEY`.
4. Go to Sender Authentication to verify your sending domain or single sender.
5. Set your verified sender address in `SENDGRID_FROM_EMAIL`.
6. Optionally set `SENDGRID_REPLY_TO` to the address where you want replies to land.

5. Run the API server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

1. Navigate to `frontend/`
2. Install dependencies:

```bash
npm install
```

3. Run the development server:

```bash
npm run dev
```

4. Open the UI at `http://localhost:3000`

## API Routes

- `POST /api/leads` - Submit a new lead.
- `GET /api/leads/{lead_id}` - Fetch lead processing status.

## Environment Variables

- `OPENAI_API_KEY` - OpenAI or Gemini-compatible key.
- `SENDGRID_API_KEY` - SendGrid API key.
- `SENDGRID_FROM_EMAIL` - Verified sender email address.
- `SENDGRID_REPLY_TO` - Optional reply-to address.
- `DATABASE_PATH` - SQLite database path.
- `REPORT_DIR` - PDF storage directory.

## Assumptions

- SendGrid is the default email provider for the prototype.
- AI content is generated through a single structured prompt.
- The system is designed for simple, realistic deployment using Vercel for frontend and Render/Railway for backend.

## Tradeoffs

- Using background processing keeps the endpoint responsive, but a dedicated job queue is not included to reduce complexity.
- AI analysis returns a single narrative to preserve prompt structure rather than storing many fine-grained fields.
- Google Sheets / Drive integration is left as a future enhancement rather than a required core dependency.

## Limitations

- The PDF generator uses ReportLab and does not include advanced graphic design.
- If scraping fails, the report is still produced from available metadata but may be less detailed.
- The prototype does not include authentication or an admin dashboard.

## Future Improvements

- Add Google Sheets logging and Google Drive archival.
- Add an asynchronous task queue (Celery, RQ) for large-scale processing.
- Add email provider fallback for Resend and provider health monitoring.
- Add a status dashboard for lead review and resend controls.
