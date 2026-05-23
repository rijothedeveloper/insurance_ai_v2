from fastapi import FastAPI

from app.schemas.claim_schemas import ClaimRequest
from app.services.orchestrator import process_claim

app = FastAPI()

@app.post("/process_claim")
def create_claim(claim: ClaimRequest):
    result = process_claim(claim.model_dump())
    return result   