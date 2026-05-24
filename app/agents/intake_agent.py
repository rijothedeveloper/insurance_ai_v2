from app.schemas.state_schema import ClaimState

def run_intake_agent(state: ClaimState) -> ClaimState:
    claim = state.claim
    missing_fields = []
    required_fields = [
        "claim_id",
        "customer_id",
        "incident_description",
        "estimated_damage",
    ]
    
    for field in required_fields:
        if field not in claim or claim[field] in [None, ""]:
            missing_fields.append(field)
            
    completeness_score = 1 - (len(missing_fields) / len(required_fields))
    
    state.intake_agent_result = {
        "missing_fields": missing_fields,
        "completeness_score": completeness_score,
        "is_complete": len(missing_fields) == 0
    }
    
    if missing_fields:
        state.status = "MISSING_INFORMATION"
        state.audit_trail.append(f"Intake Agent found missing fields: Missing fields: {missing_fields}")
        
    else:
        state.status = "INTAKE_COMPLETED"
        state.audit_trail.append("Intake Agent completed SUCCESSFULLY")
        
    return state