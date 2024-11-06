import pandas as pd
import glob

def load_data():
    """
    Load and process CSV data from the dataset folder.
    Returns a deduplicated pandas DataFrame containing all CSV data.
    """
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
