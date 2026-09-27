"""add complaint constraints and indexes

Revision ID: ea54a29d8a1c
Revises: 2b2f0e9fa794
Create Date: 2026-09-27 20:12:18.712064

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea54a29d8a1c'
down_revision: Union[str, Sequence[str], None] = '2b2f0e9fa794'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_check_constraint(
        "check_complaint_text_length",
        "complaints",
        "char_length(text) >= 10 AND char_length(text) <= 2000"
    )

    op.create_check_constraint(
        "check_complaint_category",
        "complaints",
        "category IN ('water', 'electricity', 'sanitation', 'roads', 'streetlights', 'other')"
    )

    op.create_check_constraint(
        "check_complaint_priority",
        "complaints",
        "priority IN ('high', 'normal', 'low')"
    )

    op.create_check_constraint(
        "check_complaint_status",
        "complaints",
        "status IN ('open', 'in_progress', 'resolved', 'rejected')"
    )

    op.create_index(
        "ix_complaints_category",
        "complaints",
        ["category"],
        unique=False
    )

    op.create_index(
        "ix_complaints_created_at",
        "complaints",
        ["created_at"],
        unique=False
    )

    op.create_index(
        "ix_complaints_priority",
        "complaints",
        ["priority"],
        unique=False
    )

    op.create_index(
        "ix_complaints_status",
        "complaints",
        ["status"],
        unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        "ix_complaints_status",
        table_name="complaints"
    )

    op.drop_index(
        "ix_complaints_priority",
        table_name="complaints"
    )

    op.drop_index(
        "ix_complaints_created_at",
        table_name="complaints"
    )

    op.drop_index(
        "ix_complaints_category",
        table_name="complaints"
    )

    op.drop_constraint(
        "check_complaint_status",
        "complaints",
        type_="check"
    )

    op.drop_constraint(
        "check_complaint_priority",
        "complaints",
        type_="check"
    )

    op.drop_constraint(
        "check_complaint_category",
        "complaints",
        type_="check"
    )

    op.drop_constraint(
        "check_complaint_text_length",
        "complaints",
        type_="check"
    )