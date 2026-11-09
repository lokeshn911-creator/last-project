import pandas as pd
import sqlite3
import os

def setup_database():
    os.makedirs("data/processed", exist_ok=True)
    conn = sqlite3.connect("data/processed/instamart.db")
    
    # Load raw tickets and handle missing values
    tickets_df = pd.read_csv("data/raw/tickets.csv")
    tickets_df.fillna({"text": "Unknown query", "true_category": "general"}, inplace=True)
    
    # Save to SQLite database table
    tickets_df.to_sql("support_tickets", conn, if_exists="replace", index=False)
    conn.close()
    print("Part A: Database initialized and tables populated successfully!")

if __name__ == "__main__":
    setup_database()