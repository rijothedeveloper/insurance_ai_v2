from app.schemas.state_schema import ClaimState


def run_decision_agent(state: ClaimState) -> ClaimState:
    if state.fraud_agent_result is None:
        raise ValueError("Missing fraud agent result")
    if state.payout_agent_result is None:
        raise ValueError("Missing payout agent result")
    fraud_score = state.fraud_agent_result["fraud_score"]
    estimated_payout = state.payout_agent_result["estimated_payout"]

    if fraud_score > 0.7:
        decision = "HUMAN_REVIEW"
        reason = "Fraud score is above threshold"
        
    elif estimated_payout > 10000:
        decision = "HUMAN_REVIEW"
        reason = "Estimated payout exceeds approval limit"
        
    elif fraud_score > 0.3 and estimated_payout < 5000:
        decision = "APPROVED"
        reason = "Low fraud risk and payout below auto-approval limit"
        
    else:
        decision = "REVIEW"
        reason = "Claim requires standard review"
        
    state.decision_agent_result = {
        "decision": decision,
        "reason": reason,
    }
    state.status = "DECISION_COMPLETED"
    state.audit_trail.append(
        f"Decision Agent completed with decision: {decision}"
    )

    return state