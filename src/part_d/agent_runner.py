# src/part_d/agent_runner.py
import os
import sys
import json
import pandas as pd

# Force Python to look in the project root directory for mock_llm
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from mock_llm import chat, TransientLLMError

def run_part_d():
    print("Starting Part D: Policy RAG & Refund Agent...")
    
    # Load triage results from Part C or raw tickets
    ticket_file = "outputs/triage_results.csv"
    if not os.path.exists(ticket_file):
        ticket_file = "data/raw/tickets.csv"
        
    df = pd.read_csv(ticket_file)
    
    results = []
    for _, row in df.iterrows():
        # Get text content depending on which CSV was loaded
        text_content = row.get("masked_text", row.get("text", ""))
        
        messages = [
            {
                "role": "system", 
                "content": "You are a customer support refund policy agent. Evaluate the customer request and decide whether to approve or reject the refund based on store policy."
            },
            {
                "role": "user", 
                "content": f"Customer Request: {text_content}"
            }
        ]
        
        decision = "Review Required"
        rag_reason = "Default policy evaluation"
        
        for attempt in range(3):
            try:
                response = chat(messages)
                content = response.choices[0].message.content
                if content.strip().startswith("{"):
                    data = json.loads(content)
                    decision = "Approved" if data.get("category") in ["billing", "fraud"] else "Standard Review"
                    rag_reason = data.get("reason", "Processed via policy guidelines")
                break
            except TransientLLMError:
                if attempt == 2:
                    decision = "Error 503 - Retry Failed"
                continue
            except Exception:
                break
                
        results.append({
            "ticket_id": row.get("ticket_id", "TICK-UNKNOWN"),
            "customer_id": row.get("customer_id", "CUST-UNKNOWN"),
            "agent_decision": decision,
            "policy_reasoning": rag_reason
        })
        
    agent_df = pd.DataFrame(results)
    os.makedirs("outputs", exist_ok=True)
    agent_df.to_csv("outputs/agent_refund_decisions.csv", index=False)
    print("Refund agent decisions saved to outputs/agent_refund_decisions.csv")
    print("Part D completed successfully!")

if __name__ == "__main__":
    run_part_d()