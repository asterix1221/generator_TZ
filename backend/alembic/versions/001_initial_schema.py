"""Initial database schema

Revision ID: 001
Revises:
Create Date: 2026-05-05
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("email", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
    )

    # Create templates table
    op.create_table(
        "templates",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("complexity", sa.Integer(), nullable=False),
        sa.Column("structure", JSONB(), nullable=False),
        sa.UniqueConstraint("type", "complexity", name="uq_type_complexity"),
    )

    # Create specifications table
    op.create_table(
        "specifications",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("template_id", UUID(as_uuid=True), sa.ForeignKey("templates.id"), nullable=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("content", JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("complexity", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
    )

    # Create shared_links table
    op.create_table(
        "shared_links",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("token", sa.String(64), unique=True, nullable=False, index=True),
        sa.Column("spec_id", UUID(as_uuid=True), sa.ForeignKey("specifications.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.UniqueConstraint("spec_id", name="uq_spec_shared_link"),
    )


def downgrade() -> None:
    op.drop_table("shared_links")
    op.drop_table("specifications")
    op.drop_table("templates")
    op.drop_table("users")