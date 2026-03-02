from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
import asyncio

from models.schema import Ticket, Resolution
from agents.flow import app as graph_app
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Support Agent API")

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for demo purposes
tickets_db = {}
history_db = {}

class TicketCreate(BaseModel):
    subject: str
    description: str
    customer_id: str

@app.post("/api/tickets")
async def create_ticket(ticket_in: TicketCreate, background_tasks: BackgroundTasks):
    ticket_id = str(uuid.uuid4())
    ticket = Ticket(
        id=ticket_id,
        subject=ticket_in.subject,
        description=ticket_in.description,
        customer_id=ticket_in.customer_id
    )
    tickets_db[ticket_id] = {"ticket": ticket, "status": "processing", "resolution": None}
    history_db[ticket_id] = []
    
    # Run the graph in the background
    background_tasks.add_task(run_graph, ticket_id)
    
    return {"ticket_id": ticket_id}

@app.get("/api/tickets")
async def get_tickets():
    return list(tickets_db.values())

@app.get("/api/tickets/{ticket_id}")
async def get_ticket(ticket_id: str):
    if ticket_id not in tickets_db:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {**tickets_db[ticket_id], "history": history_db[ticket_id]}

async def run_graph(ticket_id: str):
    ticket = tickets_db[ticket_id]["ticket"]
    inputs = {"ticket": ticket, "history": []}
    
    try:
        # Note: In a real app we would use SSE to stream this to the frontend
        # For this demo, we'll just update the DB as nodes complete
        async for output in graph_app.astream(inputs):
            for node_name, state_update in output.items():
                history_db[ticket_id].append(f"Node '{node_name}' completed")
                if "resolution" in state_update:
                    tickets_db[ticket_id]["resolution"] = state_update["resolution"]
                
                # Check if we need human review
                if node_name == "draft":
                    res = state_update.get("resolution")
                    if res and res.requires_human_review:
                        tickets_db[ticket_id]["status"] = "awaiting_review"
                    else:
                        tickets_db[ticket_id]["status"] = "resolved"
                
                if node_name == "execute":
                    tickets_db[ticket_id]["status"] = "resolved"
                    
    except Exception as e:
        print(f"Error running graph for {ticket_id}: {e}")
        tickets_db[ticket_id]["status"] = "failed"

class ReviewRequest(BaseModel):
    approved: bool
    feedback: Optional[str] = None

@app.post("/api/tickets/{ticket_id}/review")
async def review_ticket(ticket_id: str, review: ReviewRequest):
    approved = review.approved
    feedback = review.feedback
    if ticket_id not in tickets_db:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # In a full LangGraph implementation, we would use interrupts/checkpoints
    # For this demo, we'll simulate the "human_review" completion
    ticket_data = tickets_db[ticket_id]
    if ticket_data["status"] != "awaiting_review":
        raise HTTPException(status_code=400, detail="Ticket not awaiting review")
    
    res = ticket_data["resolution"]
    if not approved and feedback:
        res.response = feedback
    
    res.requires_human_review = False
    ticket_data["status"] = "resolved"
    history_db[ticket_id].append("Human review completed")
    
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
