from typing import Dict, Optional
from app.database.database import SessionLocal
from app.database.models import ClaimStateRecord
from app.schemas.state_schema import ClaimState




def save_state(state: ClaimState) -> ClaimState:
    claim_id = state.claim.get("claim_id")

    if not claim_id:
        raise ValueError("Cannot save state without claim_id")

    db = SessionLocal()
    try:
        existing_record = db.query(ClaimStateRecord).filter(ClaimStateRecord.claim_id == claim_id).first()
        state_data = state.model_dump()
        if existing_record:
            existing_record.status = state.status
            existing_record.state_json = state_data
            
        else:
            new_record = ClaimStateRecord(
                claim_id=claim_id,
                status=state.status,
                state_json=state_data
            )
            db.add(new_record)
        db.commit()

        return state
    finally:
        db.close()
        
    CLAIM_STATE_STORE[claim_id] = state

    return state


def get_state(claim_id: str) -> Optional[ClaimState]:
    db = SessionLocal()
    try:
        record = db.query(ClaimStateRecord).filter(ClaimStateRecord.claim_id == claim_id).first()
        if record is None:
            return None
        
        return ClaimState(**record.state_json)
        # return ClaimState(**record.state_json.values())
    finally:
        db.close()


def update_claim_data(claim_id: str, new_data: dict) -> ClaimState:
    state = get_state(claim_id)

    if state is None:
        raise ValueError(f"No claim state found for claim_id: {claim_id}")

    for key, value in new_data.items():
        if value is not None:
            state.claim[key] = value
            
    updated_fields = [key for key, value in new_data.items() if value is not None]

    state.audit_trail.append(
        f"Claim data updated with fields: {updated_fields}"
    )

    save_state(state)

    return state