def run_decision_agent(fraud_result, payout_result):
    # Simple decision logic based on the results from the other agents
    if fraud_result['recomendation'] == "ESCLATE":
        return "HUMAN_REVIEW"
    
    if payout_result['estimated_payout'] < 5000:
        return "APPROVED"
    
    return "REVIEW"
    
    