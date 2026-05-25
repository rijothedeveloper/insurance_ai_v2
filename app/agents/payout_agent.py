from app.schemas.state_schema import ClaimState
from app.tools.policy_lookup_tool import lookup_policy
from app.tools.tool_audit import record_tool_call


def run_payout_agent(state: ClaimState) -> ClaimState:
    claim = state.claim

    customer_id = claim.get("customer_id")
    estimated_damage = claim.get("estimated_damage") or 0

    policy_result = lookup_policy(customer_id)
        
    state = record_tool_call(
        state=state,
        tool_name="policy_lookup",
        tool_input={
            "customer_id": customer_id,
        },
        tool_output=policy_result,
    )
    
    if not policy_result["policy_active"]:
        state.payout_agent_result = {
            "estimated_damage": estimated_damage,
            "estimated_payout": 0,
            "adjustment_notes": [
                "Policy is inactive. No payout can be estimated."
            ],
        }
        state.status = "PAYOUT_COMPLETED"

        state.audit_trail.append(
            "Payout Agent completed with inactive policy"
        )

        return state
    
    deductible = policy_result["deductible"]
    coverage_limit = policy_result["coverage_limit"]

    estimated_payout = estimated_damage - deductible

    if estimated_payout < 0:
        estimated_payout = 0

    if estimated_payout > coverage_limit:
        estimated_payout = coverage_limit

    adjustment_notes = []

    if estimated_damage > coverage_limit:
        adjustment_notes.append(
            "Estimated damage exceeds policy coverage limit."
        )

    if deductible > 0:
        adjustment_notes.append(
            f"Applied deductible of {deductible}."
        )

    state.payout_agent_result = {
        "estimated_damage": estimated_damage,
        "deductible": deductible,
        "coverage_limit": coverage_limit,
        "estimated_payout": estimated_payout,
        "policy_active": policy_result["policy_active"],
        "adjustment_notes": adjustment_notes,
    }

    state.status = "PAYOUT_COMPLETED"

    state.audit_trail.append(
        f"Payout Agent estimated payout as {estimated_payout}"
    )

    return state