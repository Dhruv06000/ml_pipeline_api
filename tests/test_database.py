
import pandas as pd
from src.database import load_data_to_df


def test_load_data_to_df_returns_dataframe():
  # Call the database extraction method
  df = load_data_to_df()
  # Assert df is a DataFrame and has rows
  assert isinstance(df, pd.DataFrame)

def test_dataframe_has_expected_columns():
  df = load_data_to_df()

  expected_column= [
    "customer_id", 
        "age", 
        "tenure_months", 
        "monthly_charges", 
        "contract_type", 
        "total_services", 
        "churn"
  ]

  for col in expected_column:
    assert col in df.columns