from app.memory.state_store import get_state, list_human_review_states, save_state
from app.schemas.state_schema import ClaimState
from app.agents.communication_agent import run_communication_agent


VALID_HUMAN_DECISIONS = {
    "APPROVED",
    "REJECTED",
    "REQUEST_MORE_INFORMATION",
}


def get_human_review_queue() -> list[dict]:
    states = list_human_review_states()

    queue = []

    for state in states:
        queue.append(
            {
                "claim_id": state.claim.get("claim_id"),
                "customer_id": state.claim.get("customer_id"),
                "status": state.status,
                "fraud_result": state.fraud_agent_result,
                "payout_result": state.payout_agent_result,
                "decision_result": state.decision_agent_result,
                "degraded_mode": state.degraded_mode,
                "fallback_used": state.fallback_used,
            }
        )

    return queue


def apply_human_review_decision(
    claim_id: str,
    decision: str,
    reviewer_id: str,
    comments: str | None = None,
) -> ClaimState:
    state = get_state(claim_id)

    if state is None:
        raise ValueError(f"No claim state found for claim_id: {claim_id}")

    if state.status != "HUMAN_REVIEW":
        raise ValueError(
            f"Claim {claim_id} is not currently in HUMAN_REVIEW"
        )

    normalized_decision = decision.upper()

    if normalized_decision not in VALID_HUMAN_DECISIONS:
        raise ValueError(
            f"Invalid human decision: {decision}"
        )

    state.human_review = {
        "reviewer_id": reviewer_id,
        "decision": normalized_decision,
        "comments": comments,
    }

    state.requires_human_review = False

    if normalized_decision == "APPROVED":
        state.status = "APPROVED"
        state.decision_result = {
            "decision": "APPROVED",
            "reason": "Human reviewer approved the claim.",
            "source": "human_review",
        }

    elif normalized_decision == "REJECTED":
        state.status = "REJECTED"
        state.decision_result = {
            "decision": "REJECTED",
            "reason": "Human reviewer rejected the claim.",
            "source": "human_review",
        }

    elif normalized_decision == "REQUEST_MORE_INFORMATION":
        state.status = "MISSING_INFORMATION"
        state.requires_human_review = False
        state.decision_result = {
            "decision": "REQUEST_MORE_INFORMATION",
            "reason": "Human reviewer requested additional information.",
            "source": "human_review",
        }

    state.audit_trail.append(
        f"Human reviewer {reviewer_id} submitted decision: {normalized_decision}"
    )

    if comments:
        state.audit_trail.append(
            f"Human review comments: {comments}"
        )

    state = run_communication_agent(state)
    
    save_state(state)

    return state