import operator
from typing import Annotated, TypedDict, Union, List, Optional
from langgraph.graph import StateGraph, END
from models.schema import Ticket, Resolution
from knowledge.base import kb
from tools.crm import CRMTool, EmailTool
import random

# Define State
class AgentState(TypedDict):
    ticket: Ticket
    context: str
    resolution: Optional[Resolution]
    history: Annotated[List[str], operator.add]

# Nodes
def retrieve_node(state: AgentState):
    print("--- RETRIEVING CONTEXT ---")
    query = f"{state['ticket'].subject} {state['ticket'].description}"
    context = kb.query(query)
    return {"context": context, "history": ["Retrieved context from knowledge base"]}

def draft_response_node(state: AgentState):
    print("--- DRAFTING RESPONSE ---")
    # Simulate LLM Logic
    confidence = random.uniform(0.3, 0.95)
    intent = "General Support"
    
    # Mocking generating a response based on context
    draft = f"Hello! Based on our records: {state['context'][:100]}... We recommend checking your settings."
    
    res = Resolution(
        ticket_id=state['ticket'].id,
        response=draft,
        confidence_score=confidence,
        auto_resolved=False,
        requires_human_review=confidence < 0.8,
        intent=intent
    )
    return {"resolution": res, "history": [f"Drafted response with confidence {confidence:.2f}"]}

def execute_node(state: AgentState):
    print("--- EXECUTING RESOLUTION ---")
    res = state['resolution']
    CRMTool.update_ticket_status(res.ticket_id, "Resolved")
    EmailTool.send_response("customer@example.com", res.response)
    return {"history": ["Executed resolution and notified customer"]}

def learn_node(state: AgentState):
    print("--- LEARNING FROM RESOLUTION ---")
    res = state['resolution']
    kb.add_documents([f"Ticket: {state['ticket'].subject}\nResolution: {res.response}"])
    return {"history": ["Updated knowledge base with new resolution"]}

def human_review_node(state: AgentState):
    print("\n--- HUMAN REVIEW REQUIRED ---")
    res = state['resolution']
    print(f"Ticket: {state['ticket'].description}")
    print(f"Suggested Response: {res.response}")
    print(f"Confidence: {res.confidence_score:.2f}")
    
    # In a real app, this would wait for input. For this demo, we simulate approval or editing.
    action = input("Approve? (y/n) or type correction: ")
    if action.lower() == 'y':
        res.requires_human_review = False
    elif action.lower() == 'n':
        res.response = "Escalated to human expert."
        res.requires_human_review = False
    else:
        res.response = action
        res.requires_human_review = False
        
    return {"resolution": res, "history": ["Human reviewed and approved/modified response"]}

# Conditional logic
def decide_review(state: AgentState):
    if state['resolution'].requires_human_review:
        return "human_review"
    return "execute"

# Build Graph
workflow = StateGraph(AgentState)

workflow.add_node("retrieve", retrieve_node)
workflow.add_node("draft", draft_response_node)
workflow.add_node("execute", execute_node)
workflow.add_node("learn", learn_node)
workflow.add_node("human_review", human_review_node)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "draft")

workflow.add_conditional_edges(
    "draft",
    decide_review,
    {
        "human_review": "human_review",
        "execute": "execute"
    }
)

workflow.add_edge("human_review", "execute")
workflow.add_edge("execute", "learn")
workflow.add_edge("learn", END)

app = workflow.compile()
