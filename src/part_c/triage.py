# src/part_c/triage.py
import os
import sys
import re
import json
import pandas as pd

# Force Python to look in the project root directory for mock_llm
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from mock_llm import chat, TransientLLMError

def mask_pii(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r'\b[6-9]\d{9}\b', '[PHONE]', text)
    text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '[EMAIL]', text)
    text = re.sub(r'\b(?:\d[ -]*){13,16}\b', '[CARD]', text)
    return text

def run_part_c():
    print("Starting Part C: Support Ticket Triage & Guardrails...")
    tickets_df = pd.read_csv("data/raw/tickets.csv", keep_default_na=False)
    
    results = []
    for _, row in tickets_df.iterrows():
        masked_txt = mask_pii(row["text"])
        
        messages = [
            {"role": "system", "content": "CLASSIFY incoming support ticket into category."},
            {"role": "user", "content": masked_txt}
        ]
        
        predicted_cat = "technical"
        reason = "default"
        
        for attempt in range(3):
            try:
                response = chat(messages)
                content = response.choices[0].message.content
                if content.strip().startswith("{"):
                    data = json.loads(content)
                    predicted_cat = data.get("category", "technical")
                    reason = data.get("reason", "keyword match")
                break
            except TransientLLMError:
                if attempt == 2:
                    predicted_cat = "error_503"
                continue
            except Exception:
                break
                
        results.append({
            "ticket_id": row["ticket_id"],
            "customer_id": row["customer_id"],
            "order_id": row["order_id"],
            "masked_text": masked_txt,
            "true_category": row["true_category"],
            "predicted_category": predicted_cat,
            "classification_reason": reason
        })
        
    triage_results = pd.DataFrame(results)
    os.makedirs("outputs", exist_ok=True)
    triage_results.to_csv("outputs/triage_results.csv", index=False)
    print("Triage results saved to outputs/triage_results.csv")
    
    triage_results["priority"] = triage_results["predicted_category"].apply(lambda x: "High" if x in ["fraud", "billing"] else "Normal")
    triage_results.to_csv("outputs/triage_budget_demo.csv", index=False)
    print("Triage budget demo saved to outputs/triage_budget_demo.csv")

if __name__ == "__main__":
    run_part_c()