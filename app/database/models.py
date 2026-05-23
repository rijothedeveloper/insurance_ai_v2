from sqlalchemy import Column, Integer, String, Float
from app.database.database import Base

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(String)
    customer_id = Column(String)
    incident_description = Column(String)
    estimated_damage = Column(Float)
    status = Column(String)