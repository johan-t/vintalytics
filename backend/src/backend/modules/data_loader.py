import pandas as pd
import glob
from google.cloud import bigquery
from typing import Literal

def load_data(source: Literal["csv", "bigquery"] = "csv", project_id: str = None) -> pd.DataFrame:
    """
    Load and process data from either CSV files or BigQuery.
    Args:
        source: "csv" or "bigquery"
        project_id: Required for BigQuery source
    Returns:
        A deduplicated pandas DataFrame containing all data.
    """
    if source == "csv":
        return _load_from_csv()
    elif source == "bigquery":
        if not project_id:
            raise ValueError("project_id is required for BigQuery source")
        return _load_from_bigquery(project_id)
    else:
        raise ValueError("Invalid source. Use 'csv' or 'bigquery'")

def _load_from_csv() -> pd.DataFrame:
    """Load data from CSV files in the dataset folder."""
    # Get all CSV files from dataset folder
    csv_files = glob.glob("backend/dataset/*.csv")
    
    # Create empty list to store dataframes
    dfs = []
    
    # Read each CSV file and append to list
    for file in csv_files:
        df = pd.read_csv(file)
        dfs.append(df)
    
    # Concatenate all dataframes
    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        # Remove duplicates based on all columns
        combined_df = combined_df.drop_duplicates()
        return combined_df
    return pd.DataFrame()

def _load_from_bigquery(project_id: str) -> pd.DataFrame:
    """Load data from all tables in BigQuery dataset."""
    try:
        # Initialize BigQuery client
        client = bigquery.Client()
        
        # BigQuery settings
        dataset_id = 'vinted_dataset'
        
        # Get list of all tables in the dataset
        dataset_ref = client.dataset(dataset_id, project=project_id)
        tables = list(client.list_tables(dataset_ref))
        
        # Create empty list to store dataframes
        dfs = []
        
        # Query each table
        for table in tables:
            query = f"""
                SELECT 
                    Brand,
                    Item_Date,
                    Price,
                    Title,
                    URL
                FROM `{project_id}.{dataset_id}.{table.table_id}`
            """
            
            # Run query and append result to list
            df = client.query(query).to_dataframe()
            dfs.append(df)
        
        if dfs:
            # Concatenate all dataframes
            combined_df = pd.concat(dfs, ignore_index=True)
            # Remove duplicates
            combined_df = combined_df.drop_duplicates()
            return combined_df
            
        return pd.DataFrame()
        
    except Exception as e:
        print(f"Error loading from BigQuery: {e}")
        return pd.DataFrame()

# Example usage in main.py:
"""
from modules.data_loader import load_data

# For CSV:
df = load_data(source="csv")

# For BigQuery:
df = load_data(source="bigquery", project_id="your-project-id")
"""
