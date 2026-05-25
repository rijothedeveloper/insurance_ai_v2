from pydantic import BaseModel
from typing import Optional

class ClaimRequest(BaseModel):
    claim_id: str
    customer_id: Optional[str] = None
    incident_description: Optional[str] = None
    estimated_damage: Optional[float] = None
    
class ClaimUpdateRequest(BaseModel):
    customer_id: Optional[str] = None
    incident_description: Optional[str] = None
    estimated_damage: Optional[float] = None