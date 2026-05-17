from datetime import datetime
from pydantic import BaseModel, EmailStr, HttpUrl


class LeadCreate(BaseModel):
    full_name: str
    email: EmailStr
    company_name: str
    company_website: HttpUrl


class LeadStatusResponse(BaseModel):
    lead_id: int
    status: str
    error: str | None = None
    created_at: datetime
    updated_at: datetime


class ApiResponse(BaseModel):
    message: str
    lead_id: int | None = None
