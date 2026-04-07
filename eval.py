import time
import uuid
import random
import builtins
from models.schema import Ticket
from agents.flow import app

# Mock input to prevent hanging during human review node
builtins.input = lambda prompt: "y"

def run_eval():
    print("Running evaluation on 50 mock tickets to generate metrics...")
    
    start_time = time.time()
    
    total_tickets = 50
    auto_resolved = 0
    human_in_loop = 0
    total_latency = 0.0
    
    # Mocking different ticket complexities
    tickets = []
    for i in range(total_tickets):
        length = random.choice([50, 100, 200, 500])
        subject = f"Eval Ticket {i}"
        description = "word " * length
        tickets.append(Ticket(
            id=str(uuid.uuid4()),
            subject=subject,
            description=description,
            customer_id=f"CUST-{random.randint(100, 999)}"
        ))
        
    for i, ticket in enumerate(tickets):
        t0 = time.time()
        inputs = {"ticket": ticket, "history": []}
        
        # Capture resolution state
        final_state = app.invoke(inputs)
        t1 = time.time()
        
        latency = t1 - t0
        total_latency += latency
        
        if final_state.get('resolution'):
            res = final_state['resolution']
            if res.requires_human_review:
                human_in_loop += 1
            else:
                auto_resolved += 1
                
        if (i+1) % 100 == 0:
            print(f"Processed {i+1} tickets...")
            
    total_time = time.time() - start_time
    avg_latency = total_latency / total_tickets
    
    print("\n--- EVALUATION RESULTS ---")
    print(f"Total Tickets Processed: {total_tickets}")
    print(f"Auto-resolved: {auto_resolved} ({(auto_resolved/total_tickets)*100:.1f}%)")
    print(f"Human-in-loop Escalations: {human_in_loop} ({(human_in_loop/total_tickets)*100:.1f}%)")
    print(f"Average Query Latency: {avg_latency*1000:.2f}ms")
    print(f"Total Processing Time: {total_time:.2f}s")
    
if __name__ == "__main__":
    run_eval()
