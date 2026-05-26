from typing import Any, Dict

from app.tools.exceptions import FraudToolError


def check_fraud(claim: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mock Fraud Check Tool.

    Later this can call a real endpoint:
    POST /fraud/check
    """

    claim_id = claim.get("claim_id")

    # Simulate Fraud API failure for testing.
    if claim_id == "CLM-FAIL-FRAUD":
        raise FraudToolError("Fraud API unavailable")
    
    estimated_damage = claim.get("estimated_damage") or 0
    customer_id = claim.get("customer_id")

    risk_score = 0.1
    signals = []

    if estimated_damage > 10000:
        risk_score += 0.45
        signals.append("high_damage_amount")

    if customer_id == "CUS-777":
        risk_score += 0.5
        signals.append("known_suspicious_customer")

    if "theft" in str(claim.get("incident_description", "")).lower():
        risk_score += 0.2
        signals.append("theft_related_claim")

    risk_score = min(risk_score, 1.0)

    if risk_score > 0.7:
        recommendation = "ESCALATE"
    elif risk_score > 0.4:
        recommendation = "REVIEW"
    else:
        recommendation = "LOW_RISK"

    return {
        "risk_score": round(risk_score, 2),
        "signals": signals,
        "recommendation": recommendation,
    }
    
def fallback_fraud_check(claim: Dict[str, Any]) -> Dict[str, Any]:
    """
    Cached/local fallback fraud model.

    This is less accurate than the main fraud API.
    """

    estimated_damage = claim.get("estimated_damage") or 0
    incident_description = str(
        claim.get("incident_description", "")
    ).lower()

    risk_score = 0.25
    signals = ["fraud_api_unavailable"]

    if estimated_damage > 10000:
        risk_score += 0.25
        signals.append("high_damage_amount")

    if "theft" in incident_description:
        risk_score += 0.15
        signals.append("theft_related_claim")

    risk_score = min(risk_score, 1.0)

    if risk_score > 0.6:
        recommendation = "ESCALATE"
    elif risk_score > 0.35:
        recommendation = "REVIEW"
    else:
        recommendation = "LOW_RISK"
        
    return {
        "risk_score": round(risk_score, 2),
        "signals": signals,
        "recommendation": recommendation,
        "source": "cached_fraud_model",
        "confidence": 0.55,
    }