from typing import Any, Optional

from app.database.database import SessionLocal
from app.database.models import WorkflowEventRecord


def log_workflow_event(
    claim_id: str,
    event_type: str,
    status: str = "SUCCESS",
    agent_name: Optional[str] = None,
    tool_name: Optional[str] = None,
    latency_ms: Optional[int] = None,
    payload_json: Optional[dict[str, Any]] = None,
) -> None:
    db = SessionLocal()

    try:
        event = WorkflowEventRecord(
            claim_id=claim_id,
            event_type=event_type,
            agent_name=agent_name,
            tool_name=tool_name,
            status=status,
            latency_ms=latency_ms,
            payload_json=payload_json or {},
        )

        db.add(event)
        db.commit()

    finally:
        db.close()

def list_workflow_events(claim_id: str) -> list[dict[str, Any]]:
    db = SessionLocal()

    try:
        records = (
            db.query(WorkflowEventRecord)
            .filter(WorkflowEventRecord.claim_id == claim_id)
            .order_by(WorkflowEventRecord.created_at.asc())
            .all()
        )

        return [
            {
                "id": record.id,
                "claim_id": record.claim_id,
                "event_type": record.event_type,
                "agent_name": record.agent_name,
                "tool_name": record.tool_name,
                "status": record.status,
                "latency_ms": record.latency_ms,
                "payload_json": record.payload_json,
                "created_at": record.created_at.isoformat(),
            }
            for record in records
        ]

    finally:
        db.close()