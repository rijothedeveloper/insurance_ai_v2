from app.schemas.state_schema import ClaimState


def run_payout_agent(state: ClaimState) -> ClaimState:
    claim = state.claim

    estimated_damage = claim.get("estimated_damage", 0)

    deductible = 500
    coverage_limit = 10000

    estimated_payout = estimated_damage - deductible
    
    if estimated_payout < 0:
        estimated_payout = 0

    if estimated_payout > coverage_limit:
        estimated_payout = coverage_limit
        
    state.payout_agent_result = {
        "estimated_damage": estimated_damage,
        "deductible": deductible,
        "coverage_limit": coverage_limit,
        "estimated_payout": estimated_payout,
    }

    state.status = "PAYOUT_COMPLETED"

    state.audit_trail.append(
        f"Payout Agent estimated payout as {estimated_payout}"
    )

    return state