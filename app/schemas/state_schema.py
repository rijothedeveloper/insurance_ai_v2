from typing import Any,Dict, List, Optional
from pydantic import BaseModel, Field

class ClaimState(BaseModel):
    claim :Dict[str, Any]
    
    intake_agent_result: Optional[Dict[str, Any]] = None
    fraud_agent_result: Optional[Dict[str, Any]] = None
    payout_agent_result: Optional[Dict[str, Any]] = None
    decision_agent_result: Optional[Dict[str, Any]] = None
    
    status: str = "RECEIVED"
    
    errors: List[str] = Field(default_factory=list)
    
    retry_counts: Dict[str, int] = Field(
        default_factory=lambda: {
            "intake": 0,
            "fraud": 0,
            "payout": 0,
            "decision": 0   
        }
    )
    
    max_retries: Dict[str, int] = Field(
        default_factory=lambda: {
            "intake": 3,
            "fraud": 3,
            "payout": 3,
            "decision": 1,
        }
    )

    tool_results: Dict[str, Any] = Field(default_factory=dict)
    tool_audit_trail: List[Dict[str, Any]] = Field(default_factory=list)
    audit_trail: List[str] = Field(default_factory=list)