import random
from app.schemas.state_schema import ClaimState


def run_fraud_agent(state: ClaimState) -> ClaimState:
    claim = state.claim

    estimated_damage = claim.get("estimated_damage", 0)

    base_score = random.uniform(0, 0.5)

    if estimated_damage > 10000:
        base_score += 0.3
        
    fraud_score = min(base_score, 1.0)
    
    if fraud_score > 0.7:
        recommendation = "ESCALATE"
    elif fraud_score > 0.4:
        recommendation = "REVIEW"
    else:
        recommendation = "LOW_RISK"

    state.fraud_agent_result = {
        "fraud_score": round(fraud_score, 2),
        "recommendation": recommendation,
        "signals": [
            "high_damage_amount"
        ] if estimated_damage > 10000 else [],
    }
    
    state.status = "FRAUD_COMPLETED"

    state.audit_trail.append(
        f"Fraud Agent completed with score {round(fraud_score, 2)}"
    )

    return state