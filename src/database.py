import sqlite3
import os
import pandas as pd 

DB_PATH = os.path.join("data","app.db")

def get_db_connection():
  """Establishes and returns a connection to the SQLite database."""
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  return conn

def init_db():
  with get_db_connection() as conn:
    conn.execute(""" CREATE TABLE IF NOT EXISTS customers(
      customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
      age INTEGER NOT NULL,
      tenure_months INTEGER NOT NULL,
      monthly_charges REAL NOT NULL,
      contract_type TEXT NOT NULL,
      total_services INTEGER NOT NULL,
      churn INTEGER NOT NULL
    )
    """)

def seed_initial_data():
  with get_db_connection() as conn:
    cursor = conn.cursor()
    count = cursor.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    if count == 0 :
      sample_customer = [
                (34, 12, 65.0, "Month-to-month", 2, 0),
                (45, 24, 80.5, "One year", 4, 0),
                (23, 3, 95.0, "Month-to-month", 1, 1),
                (52, 48, 110.0, "Two year", 5, 0),
                (29, 6, 70.0, "Month-to-month", 2, 1)
            ]
      cursor.executemany("""
      INSERT INTO customers(age , tenure_months , monthly_charges, contract_type, total_services,churn)
      VALUES ( ?,?,?,?,?,?)
      """,sample_customer)

def load_data_to_df():
  """Extracts customer feature data from SQLite into a Pandas DataFrame."""
  with get_db_connection() as conn :
    df = pd.read_sql_query("SELECT * FROM customers", conn)
    return df

if __name__ == "__main__":
  init_db()
  seed_initial_data()
  df = load_data_to_df()
  print("Database setup complete. Loaded DataFrame:")
  print(df)


