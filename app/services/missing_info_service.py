from app.schemas.state_schema import ClaimState


def build_missing_info_response(state: ClaimState) -> dict:
    missing_fields = state.intake_agent_result["missing_fields"]
    
    return {
        "status": state.status,
        "message": "Please provide the missing claim information.",
        "missing_fields": missing_fields,
        "retry_count": state.retry_counts["intake"],
        "max_retries": state.max_retries["intake"],
        "claim": state.claim,
        "communication_result": state.communication_result,
        "audit_trail": state.audit_trail,
        "errors": state.errors,
    }