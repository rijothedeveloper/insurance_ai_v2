from typing import Dict, Optional

from app.schemas.state_schema import ClaimState


CLAIM_STATE_STORE: Dict[str, ClaimState] = {}


def save_state(state: ClaimState) -> ClaimState:
    claim_id = state.claim.get("claim_id")

    if not claim_id:
        raise ValueError("Cannot save state without claim_id")

    CLAIM_STATE_STORE[claim_id] = state

    return state


def get_state(claim_id: str) -> Optional[ClaimState]:
    return CLAIM_STATE_STORE.get(claim_id)


def update_claim_data(claim_id: str, new_data: dict) -> ClaimState:
    state = get_state(claim_id)

    if state is None:
        raise ValueError(f"No claim state found for claim_id: {claim_id}")

    for key, value in new_data.items():
        if value is not None:
            state.claim[key] = value

    state.audit_trail.append(
        f"Claim data updated with fields: {list(new_data.keys())}"
    )

    save_state(state)

    return state