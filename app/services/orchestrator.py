from app.agents.intake_agent import run_intake_agent
from app.agents.fraud_agent import run_fraud_agent
from app.agents.payout_agent import run_payout_agent
from app.agents.decision_agent import run_decision_agent
from app.schemas.state_schema import ClaimState
from app.utils.state_printer import print_state_summary
from app.services.missing_info_service import build_missing_info_response


def process_claim(claim: dict) -> dict:
    state = ClaimState(claim=claim)
    state.audit_trail.append("Claim workflow started")

    try:
        state = run_intake_agent(state)
        if state.status == "MISSING_INFORMATION":
            state.audit_trail.append(
            "Workflow paused because claim information is missing"
        )
        return build_missing_info_response(state)

        if state.status == "INTAKE_FAILED":
            state.audit_trail.append(
                "Workflow stopped because intake failed"
            )
            return {
                "status": state.status,
                "message": "Claim intake failed after maximum retries.",
                "claim": state.claim,
                "errors": state.errors,
                "audit_trail": state.audit_trail,
            }
        
        state = run_fraud_agent(state)
        state = run_payout_agent(state)
        state = run_decision_agent(state)
        state.audit_trail.append("Claim workflow completed") 
        
    except Exception as e:
        error_message = f"Error processing claim: {str(e)}"
        state.errors.append(error_message)
        state.status = "ERROR"
        state.audit_trail.append(error_message)
        
    print_state_summary(state)
       
    return state.model_dump()