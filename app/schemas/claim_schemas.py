from pydantic import BaseModel

class ClaimRequest(BaseModel):
    claim_id: str
    customer_id: str
    incident_description: str
    estimated_damage: float