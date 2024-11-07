import pandas as pd
import glob
import os

def remove_columns():
    """
    Remove Category and Currency columns from all CSV files.
    Creates a backup before modifying.
    """
    # Get all CSV files from dataset folder
    csv_files = glob.glob("backend/src/backend/dataset/*.csv")
    
    if not csv_files:
        print("No CSV files found in dataset folder")
        return
    
    # Create backup folder if it doesn't exist
    backup_folder = "backend/dataset/backup"
    os.makedirs(backup_folder, exist_ok=True)
    
    processed_count = 0
    skipped_count = 0
    
    # Columns to remove
    columns_to_remove = ['Category', 'Currency']
    
    for file in csv_files:
        try:
            # Read CSV
            df = pd.read_csv(file)
            
            # Create backup
            filename = os.path.basename(file)
            backup_path = os.path.join(backup_folder, f"backup_remove_cols_{filename}")
            df.to_csv(backup_path, index=False)
            
            # Remove specified columns if they exist
            columns_removed = []
            for column in columns_to_remove:
                if column in df.columns:
                    df = df.drop(columns=[column])
                    columns_removed.append(column)
            
            if columns_removed:
                print(f"Removed columns {', '.join(columns_removed)} from: {filename}")
                # Save modified file
                df.to_csv(file, index=False)
                processed_count += 1
                print(f"Processed: {filename}")
            else:
                print(f"No specified columns found in: {filename}")
                skipped_count += 1
                
        except Exception as e:
            print(f"Error processing {os.path.basename(file)}: {str(e)}")
            skipped_count += 1
    
    print("\nSummary:")
    print(f"Files processed: {processed_count}")
    print(f"Files skipped: {skipped_count}")
    print(f"Backups saved to: {backup_folder}")

if __name__ == "__main__":
    print("Starting to remove columns from dataset...")
    remove_columns()
    print("Done!")