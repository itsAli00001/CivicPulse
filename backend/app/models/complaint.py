import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Complaint(Base):
    __tablename__ = "complaints"

    __table_args__ = (
        CheckConstraint(
            "char_length(text) >= 10 AND char_length(text) <= 2000",
            name="check_complaint_text_length"
        ),
        CheckConstraint(
            "category IN ('water', 'electricity', 'sanitation', 'roads', 'streetlights', 'other')",
            name="check_complaint_category"
        ),
        CheckConstraint(
            "priority IN ('high', 'normal', 'low')",
            name="check_complaint_priority"
        ),
        CheckConstraint(
            "status IN ('open', 'in_progress', 'resolved', 'rejected')",
            name="check_complaint_status"
        ),
        Index("ix_complaints_category", "category"),
        Index("ix_complaints_priority", "priority"),
        Index("ix_complaints_status", "status"),
        Index("ix_complaints_created_at", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    location: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    reporter_contact: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="open"
    )

    ai_summary: Mapped[str] = mapped_column(
        String(140),
        nullable=False
    )

    triaged_by: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    triage_latency_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )