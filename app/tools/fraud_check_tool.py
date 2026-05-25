from typing import Any, Dict


def check_fraud(claim: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mock Fraud Check Tool.

    Later this can call a real endpoint:
    POST /fraud/check
    """

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