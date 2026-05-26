from app.schemas.state_schema import ClaimState
from app.services.workflow_event_service import log_workflow_event
from app.tools.fraud_check_tool import check_fraud, fallback_fraud_check
from app.tools.retry import call_tool_with_retries
from app.tools.tool_audit import record_tool_call


def run_fraud_agent(state: ClaimState) -> ClaimState:
    claim = state.claim

    tool_input = {
        "claim": claim,
        "confidence": 0.55,
    }

    try:
        state, fraud_tool_result = call_tool_with_retries(
            state=state,
            tool_name="fraud_check",
            tool_input=tool_input,
            tool_function=check_fraud,
            retry_key="fraud",
        )

    except RuntimeError as error:
        state.errors.append(str(error))
        state.degraded_mode = True
        state.fallback_used.append("cached_fraud_model")
        
        log_workflow_event(
        claim_id=state.claim.get("claim_id"),
        event_type="FALLBACK_USED",
        tool_name="cached_fraud_model",
        status="FALLBACK",
        payload_json={
            "failed_tool": "fraud_check",
            "fallback": "cached_fraud_model",
            "error": str(error),
        },
    )

        state.audit_trail.append(
            "Fraud API failed. Using cached fraud model fallback."
        )

        fraud_tool_result = fallback_fraud_check(claim)

        state = record_tool_call(
            state=state,
            tool_name="cached_fraud_model",
            tool_input=tool_input,
            tool_output=fraud_tool_result,
            status="FALLBACK_SUCCESS",
        )

        state.confidence_scores["fraud_check"] = fraud_tool_result[
            "confidence"
        ]

    fraud_score = fraud_tool_result["risk_score"]

    state.fraud_agent_result = {
        "fraud_score": fraud_score,
        "recommendation": fraud_tool_result["recommendation"],
        "signals": fraud_tool_result["signals"],
        "source": fraud_tool_result.get("source", "fraud_tool"),
        "confidence": fraud_tool_result["confidence"],
        "explanation": build_fraud_explanation(fraud_tool_result),
    }

    state.status = "FRAUD_COMPLETED"

    state.audit_trail.append(
        f"Fraud Agent completed with score {fraud_score}"
    )

    return state


def build_fraud_explanation(fraud_tool_result: dict) -> str:
    signals = fraud_tool_result["signals"]
    source = fraud_tool_result["source"]
    confidence = fraud_tool_result["confidence"]

    if not signals:
        return (
            f"No major fraud signals detected. "
            f"Source: {source}. Confidence: {confidence}."
        )

    return (
        f"Fraud signals detected: {', '.join(signals)}. "
        f"Source: {source}. Confidence: {confidence}."
    )