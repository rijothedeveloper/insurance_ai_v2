from app.schemas.state_schema import ClaimState


def run_decision_agent(state: ClaimState) -> ClaimState:
    fraud_score = state.fraud_agent_result["fraud_score"]
    estimated_payout = state.payout_agent_result["estimated_payout"]
    if state.payout_agent_result is None:
        policy_active = True
    else:
        policy_active = state.payout_agent_result.get("policy_active", True)
        
    if state.fraud_agent_result is None:
        fraud_confidence = 1.0
    else:
        fraud_confidence = state.fraud_agent_result.get("confidence", 1.0)

    if not policy_active:
        decision = "REJECTED"
        reason = "Policy is inactive."
        
    elif state.degraded_mode and fraud_confidence < 0.7:
        decision = "HUMAN_REVIEW"
        reason = (
            "Fraud tool failed and fallback confidence is below threshold."
        )

    elif fraud_score > 0.7:
        decision = "HUMAN_REVIEW"
        reason = "Fraud score is above threshold."

    elif estimated_payout > 10000:
        decision = "HUMAN_REVIEW"
        reason = "Estimated payout exceeds approval limit."

    elif fraud_score < 0.3 and estimated_payout < 5000:
        decision = "APPROVED"
        reason = "Low fraud risk and payout below auto-approval limit."

    else:
        decision = "REVIEW"
        reason = "Claim requires standard review."

    state.decision_agent_result = {
        "decision": decision,
        "reason": reason,
        "inputs": {
            "fraud_score": fraud_score,
            "estimated_payout": estimated_payout,
            "policy_active": policy_active,
        },
    }

    state.status = decision
    
    if decision == "HUMAN_REVIEW":
        state.requires_human_review = True
        state.audit_trail.append(
            "Claim added to human review queue"
        )
    else:
        state.requires_human_review = False

    state.audit_trail.append(
        f"Decision Agent completed with decision: {decision}"
    )

    return state