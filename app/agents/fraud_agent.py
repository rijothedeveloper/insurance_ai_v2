import random
from app.schemas.state_schema import ClaimState
from app.tools.fraud_check_tool import check_fraud
from app.tools.tool_audit import record_tool_call


def run_fraud_agent(state: ClaimState) -> ClaimState:
    claim = state.claim

    fraud_tool_result = check_fraud(claim)

    state = record_tool_call(
        state=state,
        tool_name="fraud_check",
        tool_input={
            "claim_id": claim.get("claim_id"),
            "customer_id": claim.get("customer_id"),
            "estimated_damage": claim.get("estimated_damage"),
        },
        tool_output=fraud_tool_result,
    )

    fraud_score = fraud_tool_result["risk_score"]
   

    state.fraud_agent_result = {
        "fraud_score": fraud_score,
        "recommendation": fraud_tool_result["recommendation"],
        "signals": fraud_tool_result["signals"],
        "explanation": build_fraud_explanation(fraud_tool_result),
    }
    
    state.status = "FRAUD_COMPLETED"

    state.audit_trail.append(
        f"Fraud Agent completed with score {round(fraud_score, 2)}"
    )

    return state

def build_fraud_explanation(fraud_tool_result: dict) -> str:
    signals = fraud_tool_result["signals"]

    if not signals:
        return "No major fraud signals detected."

    return f"Fraud signals detected: {', '.join(signals)}."