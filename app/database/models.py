from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from app.database.database import Base


class ClaimStateRecord(Base):
    __tablename__ = "claim_states"

    id = Column(Integer, primary_key=True, index=True)

    claim_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    status = Column(
        String,
        nullable=False,
        default="RECEIVED",
    )

    state_json = Column(
        JSONB,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.now,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
    )
    
class WorkflowEventRecord(Base):
    __tablename__ = "workflow_events"

    id = Column(Integer, primary_key=True, index=True)

    claim_id = Column(
        String,
        index=True,
        nullable=False,
    )

    event_type = Column(
        String,
        index=True,
        nullable=False,
    )

    agent_name = Column(
        String,
        nullable=True,
    )

    tool_name = Column(
        String,
        nullable=True,
    )

    status = Column(
        String,
        nullable=False,
        default="SUCCESS",
    )

    latency_ms = Column(
        Integer,
        nullable=True,
    )

    payload_json = Column(
        JSONB,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )