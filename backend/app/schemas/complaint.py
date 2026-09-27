from pydantic import BaseModel, Field


class ComplaintCreate(BaseModel):
    text: str = Field(min_length=10, max_length=2000)
    location: str = Field(min_length=3, max_length=200)
    reporter_contact: str | None = None


class ComplaintResponse(BaseModel):
    id: str
    text: str
    location: str
    reporter_contact: str | None = None
    category: str
    priority: str
    status: str
    ai_summary: str
    triaged_by: str