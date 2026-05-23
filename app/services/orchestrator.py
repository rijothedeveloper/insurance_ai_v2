from app.agents.intake_agent import run_intake_agent
from app.agents.fraud_agent import run_fraud_agent
from app.agents.payout_agent import run_payout_agent
from app.agents.decision_agent import run_decision_agent

def process_claim(claim):
    intake_result = run_intake_agent(claim)
    fraud_result = run_fraud_agent(claim)
    payout_result = run_payout_agent(claim)
    decision = run_decision_agent(fraud_result, payout_result)
    
    return {
        "intake_result": intake_result,
        "fraud_result": fraud_result,
        "payout_result": payout_result,
        "decision": decision
    }