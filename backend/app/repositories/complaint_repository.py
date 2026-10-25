
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.complaint import Complaint


class ComplaintRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, complaint: Complaint) -> Complaint:
        self.db.add(complaint)
        self.db.commit()
        self.db.refresh(complaint)
        return complaint

    def get_by_id(self, complaint_id: UUID) -> Complaint | None:
        return (
            self.db.query(Complaint)
            .filter(Complaint.id == complaint_id)
            .first()
        )

    def get_all(
        self,
        status: str | None = None,
        category: str | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[Complaint]:
        query = self.db.query(Complaint)

        if status is not None:
            query = query.filter(Complaint.status == status)

        if category is not None:
            query = query.filter(Complaint.category == category)

        return (
            query.order_by(Complaint.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    def update_status(
        self,
        complaint: Complaint,
        new_status: str
    ) -> Complaint:
        complaint.status = new_status
        self.db.commit()
        self.db.refresh(complaint)
        return complaint
