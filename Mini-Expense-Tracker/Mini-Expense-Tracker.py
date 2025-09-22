"""
Mini Expense Tracker - Python client
Run after executing init.sql.
Requires: mysql-connector-python
"""

import os
import csv
import getpass
from datetime import date
from typing import List, Dict, Optional

import mysql.connector
from mysql.connector import Error

# ---- Configure via env vars or edit here ----
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root")
DB_NAME = os.getenv("DB_NAME", "mini_expense")

# Global variable to store the password once entered
_db_password = None

def get_db_password():
    """Get database password from user input (hidden) if not already set"""
    global _db_password
    if _db_password is None:
        print(f"Connecting to MySQL database '{DB_NAME}' on {DB_HOST}")
        print("Note: Password will be hidden as you type (this is normal for security)")
        _db_password = getpass.getpass(f"Enter password for MySQL user '{DB_USER}': ")
    return _db_password

def get_conn():
    return mysql.connector.connect(
        host=DB_HOST, 
        user=DB_USER, 
        password=get_db_password(), 
        database=DB_NAME
    )

# ---- Core DB helpers ----
def insert_expense(occurred_on: str, amount: float, category: str, note: Optional[str] = None) -> None:
    sql = """
      INSERT INTO expenses (occurred_on, amount, category, note)
      VALUES (%s, %s, %s, %s)
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (occurred_on, amount, category, note))
        conn.commit()

def import_csv(csv_path: str) -> int:
    """
    CSV columns (case-insensitive): date, amount, category, note
    amount: negative = expense, positive = income
    """
    count = 0
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            occurred_on = (r.get("date") or r.get("Date")).strip()
            amount = float(r.get("amount") or r.get("Amount"))
            category = (r.get("category") or r.get("Category") or "Uncategorized").strip()
            note = (r.get("note") or r.get("Note") or "").strip() or None
            insert_expense(occurred_on, amount, category, note)
            count += 1
    return count

def fetch_all(sql: str, params: Optional[tuple] = None) -> List[Dict]:
    with get_conn() as conn:
        with conn.cursor(dictionary=True) as cur:
            cur.execute(sql, params or ())
            return cur.fetchall()

# ---- Reports ----
def report_monthly_totals() -> None:
    rows = fetch_all("SELECT * FROM v_monthly_totals;")
    print("\n=== Monthly Net (income - expenses) ===")
    for r in rows:
        print(f"{r['month_start']}: {r['net_amount']:.2f}")

def report_category_breakdown(month_yyyy_mm: str) -> None:
    rows = fetch_all(
        "SELECT category, total_amount, txn_count FROM v_monthly_category WHERE month_start=%s;",
        (f"{month_yyyy_mm}-01",),
    )
    print(f"\n=== Category Breakdown for {month_yyyy_mm} ===")
    if not rows:
        print("No data.")
    for r in rows:
        amt = float(r["total_amount"])
        print(f"{r['category']:<16} {amt:>10.2f}  ({r['txn_count']} txns)")

# ---- Demo runner ----
SAMPLE_CSV = """date,amount,category,note
2025-09-10,-18.90,Dining,Coffee & bagel
2025-09-11,-82.45,Groceries,WF run
2025-09-12,2000.00,Income,Paycheck
"""

def write_sample_csv(path="sample_expenses.csv") -> str:
    with open(path, "w", encoding="utf-8") as f:
        f.write(SAMPLE_CSV)
    return path

def main():
    print("Mini Expense Tracker (DB:", DB_NAME, ")")
    
    # Just display existing data - no automatic inserts
    print("Displaying current data from database...\n")
    
    # Display reports from existing data
    report_monthly_totals()
    report_category_breakdown("2025-09")

    print("\nDone.")
    print("\nNote: To add data, you can:")
    print("- Edit the database directly in MySQL Workbench")
    print("- Uncomment the insert/import lines in the code if needed")

if __name__ == "__main__":
    main()
