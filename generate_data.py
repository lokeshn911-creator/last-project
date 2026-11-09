# generate_data.py
import os
import pandas as pd

def generate_sample_data():
    # Ensure directories exist
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    
    # Sample ticket data for Part C and RAG agent
    tickets_data = [
        {
            "ticket_id": "TICK-101",
            "customer_id": "CUST-001",
            "order_id": "ORD-5001",
            "text": "Hi, I was charged twice for my grocery order. My phone number is 9876543210 and my email is test@example.com. Please refund my money.",
            "true_category": "billing"
        },
        {
            "ticket_id": "TICK-102",
            "customer_id": "CUST-002",
            "order_id": "ORD-5002",
            "text": "There is a suspicious transaction on my account that I did not authorize. Please help!",
            "true_category": "fraud"
        },
        {
            "ticket_id": "TICK-103",
            "customer_id": "CUST-003",
            "order_id": "ORD-5003",
            "text": "The app crashes every time I try to view my past orders. Can you fix this technical glitch?",
            "true_category": "technical"
        }
    ]
    
    df_tickets = pd.DataFrame(tickets_data)
    df_tickets.to_csv("data/raw/tickets.csv", index=False)
    print("Successfully generated data/raw/tickets.csv")

if __name__ == "__main__":
    generate_sample_data()