import pandas as pd
import glob
import os


def load_data() -> pd.DataFrame:
    """
    Load and process CSV data from the dataset folder.
    Returns a deduplicated pandas DataFrame containing all CSV data.
    """
    # Get absolute path to dataset directory
    base_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    )
    dataset_path = os.path.join(base_dir, "dataset", "*.csv")

    # Get all CSV files from dataset folder
    csv_files = glob.glob(dataset_path)

    if not csv_files:
        print(f"No CSV files found in {dataset_path}")
        return pd.DataFrame()

    # Create empty list to store dataframes
    dfs = []

    # Read each CSV file and append to list
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            dfs.append(df)
            print(f"Successfully loaded {file}")
        except Exception as e:
            print(f"Error loading {file}: {str(e)}")

    # Concatenate all dataframes
    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        # Remove duplicates based on all columns
        combined_df = combined_df.drop_duplicates()
        print(f"Final DataFrame columns: {combined_df.columns.tolist()}")
        return combined_df

    return pd.DataFrame()
