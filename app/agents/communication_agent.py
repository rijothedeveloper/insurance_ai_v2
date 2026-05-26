from app.schemas.state_schema import ClaimState


def run_communication_agent(state: ClaimState) -> ClaimState:
    status = state.status

    if status == "APPROVED":
        state.communication_result = build_approval_message(state)

    elif status == "REJECTED":
        state.communication_result = build_rejection_message(state)

    elif status == "HUMAN_REVIEW":
        state.communication_result = build_human_review_message(state)

    elif status == "MISSING_INFORMATION":
        state.communication_result = build_missing_information_message(state)

    else:
        state.communication_result = build_generic_message(state)

    state.audit_trail.append(
        f"Communication Agent generated message for status: {status}"
    )

    return state


def build_approval_message(state: ClaimState) -> dict:
    claim_id = state.claim.get("claim_id")
    payout = state.payout_agent_result.get("estimated_payout", 0)

    return {
        "customer_message": (
            f"Your claim {claim_id} has been approved. "
            f"The estimated payout is ${payout}."
        ),
        "adjuster_summary": (
            f"Claim {claim_id} was auto-approved. "
            f"Fraud score: {state.fraud_agent_result.get('fraud_score')}. "
            f"Estimated payout: ${payout}."
        ),
        "audit_summary": (
            "Auto-approval generated based on low fraud risk, "
            "active policy, and payout within approval threshold."
        ),
    }


def build_rejection_message(state: ClaimState) -> dict:
    claim_id = state.claim.get("claim_id")
    reason = state.decision_agent_result.get("reason", "Claim was rejected.")

    return {
        "customer_message": (
            f"Your claim {claim_id} was not approved. "
            f"Reason: {reason}"
        ),
        "adjuster_summary": (
            f"Claim {claim_id} was rejected. "
            f"Reason: {reason}"
        ),
        "audit_summary": (
            f"Rejection recorded with reason: {reason}"
        ),
    }


def build_human_review_message(state: ClaimState) -> dict:
    claim_id = state.claim.get("claim_id")
    reason = state.decision_agent_result.get(
        "reason",
        "Claim requires human review.",
    )

    return {
        "customer_message": (
            f"Your claim {claim_id} is currently under review. "
            "An adjuster will review the details before a final decision is made."
        ),
        "adjuster_summary": (
            f"Claim {claim_id} requires human review. "
            f"Reason: {reason}. "
            f"Fraud result: {state.fraud_agent_result}. "
            f"Payout result: {state.payout_agent_result}."
        ),
        "audit_summary": (
            f"Claim escalated to human review. Reason: {reason}"
        ),
    }


def build_missing_information_message(state: ClaimState) -> dict:
    claim_id = state.claim.get("claim_id")

    missing_fields = []

    if state.intake_agent_result:
        missing_fields = state.intake_agent_result.get("missing_fields", [])

    return {
        "customer_message": (
            f"Your claim {claim_id} is missing required information. "
            f"Please provide: {', '.join(missing_fields)}."
        ),
        "adjuster_summary": (
            f"Claim {claim_id} is paused because required fields are missing: "
            f"{missing_fields}."
        ),
        "audit_summary": (
            f"Missing information requested: {missing_fields}"
        ),
    }


def build_generic_message(state: ClaimState) -> dict:
    claim_id = state.claim.get("claim_id")

    return {
        "customer_message": (
            f"Your claim {claim_id} has status: {state.status}."
        ),
        "adjuster_summary": (
            f"Claim {claim_id} currently has status: {state.status}."
        ),
        "audit_summary": (
            f"Generic communication generated for status: {state.status}"
        ),
    }
    