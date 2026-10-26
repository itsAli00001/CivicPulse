import json
from uuid import UUID

from app.cache.redis_client import (
    get_cached_statistics,
    invalidate_statistics_cache,
    set_cached_statistics,
)
from app.models.complaint import Complaint
from app.providers.triage_factory import get_triage_provider
from app.repositories.complaint_repository import ComplaintRepository
from app.schemas.complaint import ComplaintCreate


class ComplaintService:

    VALID_TRANSITIONS = {
        "open": {"in_progress", "rejected"},
        "in_progress": {"resolved", "rejected"},
        "resolved": set(),
        "rejected": set(),
    }

    def __init__(self, repository: ComplaintRepository):
        self.repository = repository
        self.triage_provider = get_triage_provider()

    def create_complaint(
        self,
        complaint: ComplaintCreate
    ) -> Complaint:

        triage_result = self.triage_provider.triage(
            complaint.text
        )

        complaint_model = Complaint(
            text=complaint.text,
            location=complaint.location,
            reporter_contact=complaint.reporter_contact,
            category=triage_result.category,
            priority=triage_result.priority,
            status="open",
            ai_summary=triage_result.ai_summary,
            triaged_by=triage_result.triaged_by,
        )

        created_complaint = self.repository.create(
            complaint_model
        )

        invalidate_statistics_cache()

        return created_complaint

    def get_complaint(
        self,
        complaint_id: UUID
    ) -> Complaint | None:

        return self.repository.get_by_id(
            complaint_id
        )

    def get_complaints(
        self,
        status: str | None = None,
        category: str | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[Complaint]:

        return self.repository.get_all(
            status=status,
            category=category,
            limit=limit,
            offset=offset,
        )

    def update_complaint_status(
        self,
        complaint_id: UUID,
        new_status: str
    ) -> Complaint | None:

        complaint = self.repository.get_by_id(
            complaint_id
        )

        if complaint is None:
            return None

        allowed_statuses = self.VALID_TRANSITIONS.get(
            complaint.status,
            set()
        )

        if new_status not in allowed_statuses:
            raise ValueError(
                f"Cannot change status from "
                f"{complaint.status} to {new_status}"
            )

        updated_complaint = self.repository.update_status(
            complaint,
            new_status
        )

        invalidate_statistics_cache()

        return updated_complaint

    def get_statistics(self) -> tuple[dict, str]:

        cached_data = get_cached_statistics()

        if cached_data is not None:
            return json.loads(cached_data), "HIT"

        statistics = self.repository.get_statistics()

        set_cached_statistics(
            json.dumps(statistics)
        )

        return statistics, "MISS"