from app.agents.intake_agent import run_intake_agent
from app.agents.fraud_agent import run_fraud_agent
from app.agents.payout_agent import run_payout_agent
from app.agents.decision_agent import run_decision_agent
from app.schemas.state_schema import ClaimState
from app.utils.state_printer import print_state_summary

def process_claim(claim: dict) -> ClaimState:
    state = ClaimState(claim=claim)
    state.audit_trail.append("Claim workflow started")

    try:
        state = run_intake_agent(state)
        if state.status == "MISSING_INFORMATION":
            state.audit_trail.append("Workflow stopped because information is missing")
            return state
        
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
       
    return state