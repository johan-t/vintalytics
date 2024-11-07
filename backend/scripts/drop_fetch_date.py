import pandas as pd
import glob
import os

def modify_columns():
    """
    Modify CSV files:
    - Remove Fetch_Date column
    - Add classification columns (Category, Colors, Materials, Styles)
    Creates a backup of original files before modifying.
    """
    # Get all CSV files from dataset folder
    csv_files = glob.glob("backend/dataset/*.csv")
    
    if not csv_files:
        print("No CSV files found in dataset folder")
        return
    
    # Create backup folder if it doesn't exist
    backup_folder = "backend/dataset/backup"
    os.makedirs(backup_folder, exist_ok=True)
    
    processed_count = 0
    skipped_count = 0
    
    # New columns to add
    new_columns = ['Category', 'Colors', 'Materials', 'Styles']
    
    for file in csv_files:
        try:
            # Read CSV
            df = pd.read_csv(file)
            
            # Create backup
            filename = os.path.basename(file)
            backup_path = os.path.join(backup_folder, f"backup_{filename}")
            df.to_csv(backup_path, index=False)
            
            # Drop Fetch_Date column if it exists
            if 'Fetch_Date' in df.columns:
                df = df.drop(columns=['Fetch_Date'])
                print(f"Removed Fetch_Date from: {filename}")
            
            # Add new columns if they don't exist
            for column in new_columns:
                if column not in df.columns:
                    df[column] = ''  # Empty string for initial values
                    print(f"Added {column} column to: {filename}")
            
            # Save modified file
            df.to_csv(file, index=False)
            
            processed_count += 1
            print(f"Processed: {filename}")
                
        except Exception as e:
            print(f"Error processing {os.path.basename(file)}: {str(e)}")
    
    print("\nSummary:")
    print(f"Files processed: {processed_count}")
    print(f"Files skipped: {skipped_count}")
    print(f"Backups saved to: {backup_folder}")

if __name__ == "__main__":
    print("Starting to modify columns in dataset...")
    modify_columns()
    print("Done!")