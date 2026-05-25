from fastapi import FastAPI, HTTPException

from app.memory.state_store import get_state, update_claim_data
from app.schemas.claim_schemas import ClaimRequest, ClaimUpdateRequest
from app.services.orchestrator import process_new_claim, run_workflow_from_state

app = FastAPI()

@app.post("/process_claim")
def create_claim(claim: ClaimRequest):
    result = process_new_claim(claim.model_dump())
    return result   

@app.get("/health")
def health_check():
    return {"status": "ok"} 

@app.get("/claims/{claim_id}/state")
def get_claim_state(claim_id: str):
    state = get_state(claim_id)
    if state is None:
        raise HTTPException(status_code=404, detail=f"No state found for claim_id: {claim_id}")
    return state.model_dump()

@app.patch("/claims/{claim_id}/missing-info")
def submit_missing_info(claim_id: str, update_data: ClaimUpdateRequest):
    try:
        state = update_claim_data(claim_id=claim_id, new_data=update_data.model_dump())
        result = run_workflow_from_state(state)
        return result
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))