import random

def run_fraud_agent(claim):
    # Simulate fraud detection with random results
    fraud_score = random.uniform(0, 1)
    if fraud_score > 0.7:
        recomendation = "ESCLATE"
    else:
        recomendation = "LOW_RISK"
    return {
        "fraud_score": fraud_score,
        "recomendation": recomendation
    }