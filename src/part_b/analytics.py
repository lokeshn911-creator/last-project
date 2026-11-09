import pandas as pd
import os

def run_customer_analytics():
    os.makedirs("outputs", exist_ok=True)
    
    # Load support tickets data for customer metrics
    tickets_df = pd.read_csv("data/raw/tickets.csv")
    
    # Customer volume segmentation logic
    customer_summary = tickets_df.groupby("customer_id").agg(
        total_tickets=("ticket_id", "count")
    ).reset_index()
    
    # Classify risk tiers
    customer_summary["risk_level"] = customer_summary["total_tickets"].apply(
        lambda x: "High Risk" if x > 2 else "Standard Risk"
    )
    
    # Export Part B output CSV
    customer_summary.to_csv("outputs/customer_segmentation.csv", index=False)
    print("Part B: Customer segmentation analysis saved to outputs/customer_segmentation.csv")

if __name__ == "__main__":
    run_customer_analytics()