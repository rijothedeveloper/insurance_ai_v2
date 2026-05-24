from app.schemas.state_schema import ClaimState


def print_state_summary(state: ClaimState) -> None:
    print("------ CLAIM STATE SUMMARY ------")
    print(f"Claim ID: {state.claim.get('claim_id')}")
    print(f"Status: {state.status}")
    print(f"Decision: {state.decision_agent_result}")
    print("Audit Trail:")
    for item in state.audit_trail:
        print(f"- {item}")
    print("--------------------------------")