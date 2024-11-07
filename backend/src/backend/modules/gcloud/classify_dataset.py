import pandas as pd
import glob
import os
from image_classifier import classify_image
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import threading

# Initialize colorama for colored output
init()

# Thread-safe print lock
print_lock = threading.Lock()

# Define target brands
TARGET_BRANDS = ['H&M', 'Zara', 'Nike', 'adidas', 'C&A', 'SHEIN', 'ONLY']

def safe_print(*args, **kwargs):
    """Thread-safe printing function."""
    with print_lock:
        print(*args, **kwargs)

def needs_classification(row):
    """Check if the row needs classification."""
    return (
        pd.isna(row.get('Categories')) or 
        pd.isna(row.get('Colors')) or 
        pd.isna(row.get('Materials')) or 
        pd.isna(row.get('Styles')) or
        row.get('Categories') == '' or 
        row.get('Colors') == '' or 
        row.get('Materials') == '' or 
        row.get('Styles') == ''
    )

def process_row(row, image_dirs, csv_file, df_lock):
    """Process a single row with image classification."""
    try:
        # Skip if already classified
        if not needs_classification(row):
            safe_print(f"{Fore.BLUE}Skipping ID {row['ID']}: Already classified{Style.RESET_ALL}")
            return True, row['ID']  # Count as success but skip processing
        
        # Find image file
        image_path = find_image(str(row['ID']), image_dirs)
        if not image_path:
            safe_print(f"{Fore.YELLOW}Image not found for ID: {row['ID']}{Style.RESET_ALL}")
            return False, row['ID']
        
        # Classify image
        classification = classify_image(row['Title'], image_path)
        
        # Prepare classifications
        categories = ' '.join(str(classification['categories']).split(','))
        colors = ' '.join(classification['colors'])
        materials = ' '.join(classification['materials'])
        styles = ' '.join(classification['styles'])
        
        # Update CSV with thread safety
        with df_lock:
            df = pd.read_csv(csv_file)
            df.loc[df['ID'] == row['ID'], 'Categories'] = categories
            df.loc[df['ID'] == row['ID'], 'Colors'] = colors
            df.loc[df['ID'] == row['ID'], 'Materials'] = materials
            df.loc[df['ID'] == row['ID'], 'Styles'] = styles
            df.to_csv(csv_file, index=False)
        
        safe_print(f"\n{Fore.GREEN}Processed ID: {row['ID']}{Style.RESET_ALL}")
        safe_print(f"Brand: {row['Brand']}")
        safe_print(f"Title: {row['Title']}")
        safe_print(f"Categories: {Fore.CYAN}{categories}{Style.RESET_ALL}")
        safe_print(f"Colors: {Fore.CYAN}{colors}{Style.RESET_ALL}")
        safe_print(f"Materials: {Fore.CYAN}{materials}{Style.RESET_ALL}")
        safe_print(f"Styles: {Fore.CYAN}{styles}{Style.RESET_ALL}")
        safe_print("-" * 80)
        
        return True, row['ID']
        
    except Exception as e:
        safe_print(f"{Fore.RED}Error processing ID {row['ID']}: {str(e)}{Style.RESET_ALL}")
        return False, row['ID']

def process_csv_file(csv_file, image_dirs):
    """Process a single CSV file."""
    safe_print(f"\n{Fore.CYAN}Processing {csv_file}...{Style.RESET_ALL}")
    df = pd.read_csv(csv_file)
    
    # Filter for target brands
    df_filtered = df[df['Brand'].isin(TARGET_BRANDS)]
    
    if df_filtered.empty:
        safe_print(f"{Fore.YELLOW}No target brands found in {csv_file}{Style.RESET_ALL}")
        return 0, 0, 0
    
    # Filter for unclassified items
    df_to_process = df_filtered[df_filtered.apply(needs_classification, axis=1)]
    already_classified = len(df_filtered) - len(df_to_process)
    
    safe_print(f"Found {len(df_filtered)} items from target brands")
    safe_print(f"Already classified: {already_classified}")
    safe_print(f"To be processed: {len(df_to_process)}")
    
    if df_to_process.empty:
        safe_print(f"{Fore.GREEN}All items already classified in {csv_file}{Style.RESET_ALL}")
        return 0, 0, already_classified
        
    # Create a thread-safe lock for DataFrame operations
    df_lock = threading.Lock()
    
    processed = 0
    skipped = 0
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(process_row, row, image_dirs, csv_file, df_lock)
            for _, row in df_to_process.iterrows()
        ]
        
        with tqdm(total=len(futures), desc=f"Processing {os.path.basename(csv_file)}") as pbar:
            for future in as_completed(futures):
                success, _ = future.result()
                if success:
                    processed += 1
                else:
                    skipped += 1
                pbar.update(1)
    
    return processed, skipped, already_classified

def process_dataset():
    """Process all CSV files concurrently."""
    csv_files = glob.glob("backend/dataset/*.csv")
    
    image_dirs = [
        "backend/dataset/images",
        "backend/dataset/images_between",
        "backend/dataset/images_rest"
    ]
    
    total_processed = 0
    total_skipped = 0
    total_already_classified = 0
    
    # Process all CSV files concurrently with 2 workers per file
    with ThreadPoolExecutor(max_workers=len(csv_files)) as executor:
        # Submit all CSV files for processing
        future_to_csv = {
            executor.submit(process_csv_file, csv_file, image_dirs): csv_file 
            for csv_file in csv_files
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_csv):
            csv_file = future_to_csv[future]
            try:
                processed, skipped, already_classified = future.result()
                total_processed += processed
                total_skipped += skipped
                total_already_classified += already_classified
            except Exception as e:
                safe_print(f"{Fore.RED}Error processing {csv_file}: {str(e)}{Style.RESET_ALL}")
    
    # Print final statistics
    safe_print(f"\n{Fore.CYAN}=== Final Statistics ==={Style.RESET_ALL}")
    safe_print(f"Total items already classified: {total_already_classified}")
    safe_print(f"Total items processed: {total_processed}")
    safe_print(f"Total items skipped: {total_skipped}")
    if total_processed + total_skipped > 0:
        safe_print(f"Success rate: {(total_processed/(total_processed+total_skipped))*100:.2f}%")

def find_image(image_id: str, directories: list) -> str:
    """Find image file in multiple directories."""
    image_filename = f"{image_id}.jpeg"
    
    for directory in directories:
        image_path = os.path.join(directory, image_filename)
        if os.path.exists(image_path):
            return image_path
    
    return None

if __name__ == "__main__":
    print(f"{Fore.CYAN}Starting concurrent dataset classification...{Style.RESET_ALL}")
    process_dataset()
    print(f"{Fore.GREEN}Classification complete!{Style.RESET_ALL}")