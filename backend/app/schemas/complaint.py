
import re
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class ComplaintCreate(BaseModel):
    text: str = Field(min_length=10, max_length=2000)
    location: str = Field(min_length=3, max_length=200)
    reporter_contact: str | None = None

    @field_validator("reporter_contact")
    @classmethod
    def validate_reporter_contact(cls, value):
        if value is None:
            return value

        if not re.fullmatch(r"03\d{9}", value):
            raise ValueError(
                "reporter_contact must be a valid Pakistani mobile number"
            )

        return value


class ComplaintResponse(BaseModel):
    id: UUID
    text: str
    location: str
    reporter_contact: str | None = None
    category: str
    priority: str
    status: str
    ai_summary: str
    triaged_by: str

    model_config = {"from_attributes": True}
