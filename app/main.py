from fastapi import FastAPI, HTTPException
from app.database.database import Base, engine

from app.memory.state_store import get_state, update_claim_data
from app.schemas.claim_schemas import ClaimRequest, ClaimUpdateRequest, HumanReviewDecisionRequest
from app.services.orchestrator import process_new_claim, run_workflow_from_state
from app.services.human_review_service import apply_human_review_decision, get_human_review_queue
from app.services.workflow_event_service import list_workflow_events

Base.metadata.create_all(bind=engine)

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
    
@app.get("/human-review/claims")
def list_human_review_claims():
    return {
        "claims": get_human_review_queue()
    }


@app.post("/human-review/claims/{claim_id}/decision")
def submit_human_review_decision(
    claim_id: str,
    review: HumanReviewDecisionRequest,
):
    try:
        state = apply_human_review_decision(
            claim_id=claim_id,
            decision=review.decision,
            reviewer_id=review.reviewer_id,
            comments=review.comments,
        )

        return state.model_dump()

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
        
@app.get("/claims/{claim_id}/events")
def get_claim_events(claim_id: str):
    return {
        "claim_id": claim_id,
        "events": list_workflow_events(claim_id),
    }