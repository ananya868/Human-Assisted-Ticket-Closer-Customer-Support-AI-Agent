from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class Ticket(BaseModel):
    id: str
    subject: str
    description: str
    customer_id: str
    priority: Optional[Literal["low", "medium", "high"]] = "medium"

class Resolution(BaseModel):
    ticket_id: str
    response: str
    confidence_score: float
    auto_resolved: bool
    requires_human_review: bool
    intent: Optional[str] = None
