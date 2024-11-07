import pandas as pd
import glob
import os
from image_classifier import classify_image
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

def process_dataset():
    """Process all CSV files and classify their images."""
    # Get all CSV files
    csv_files = glob.glob("backend/dataset/*.csv")
    
    # Image directories to search
    image_dirs = [
        "backend/dataset/images",
        "backend/dataset/images_between",
        "backend/dataset/images_rest"
    ]
    
    total_processed = 0
    total_skipped = 0
    
    for csv_file in csv_files:
        print(f"\n{Fore.CYAN}Processing {csv_file}...{Style.RESET_ALL}")
        df = pd.read_csv(csv_file)
        
        file_processed = 0
        file_skipped = 0
        
        # Process each row
        for index, row in df.iterrows():
            try:
                # Find image file
                image_path = find_image(str(row['ID']), image_dirs)
                if not image_path:
                    print(f"{Fore.YELLOW}Image not found for ID: {row['ID']}{Style.RESET_ALL}")
                    file_skipped += 1
                    continue
                
                # Classify image
                classification = classify_image(row['Title'], image_path)
                
                # Update DataFrame with classifications
                categories = ' '.join(str(classification['categories']).split(','))
                colors = ' '.join(classification['colors'])
                materials = ' '.join(classification['materials'])
                styles = ' '.join(classification['styles'])
                
                df.at[index, 'Categories'] = categories
                df.at[index, 'Colors'] = colors
                df.at[index, 'Materials'] = materials
                df.at[index, 'Styles'] = styles
                
                # Save CSV after each classification
                df.to_csv(csv_file, index=False)
                
                # Print classification results
                print(f"\n{Fore.GREEN}Processed ID: {row['ID']}{Style.RESET_ALL}")
                print(f"Title: {row['Title']}")
                print(f"Categories: {Fore.CYAN}{categories}{Style.RESET_ALL}")
                print(f"Colors: {Fore.CYAN}{colors}{Style.RESET_ALL}")
                print(f"Materials: {Fore.CYAN}{materials}{Style.RESET_ALL}")
                print(f"Styles: {Fore.CYAN}{styles}{Style.RESET_ALL}")
                print("-" * 80)
                
                file_processed += 1
                
            except Exception as e:
                print(f"{Fore.RED}Error processing ID {row['ID']}: {str(e)}{Style.RESET_ALL}")
                file_skipped += 1
        
        total_processed += file_processed
        total_skipped += file_skipped
        
        print(f"\n{Fore.GREEN}Completed processing {csv_file}{Style.RESET_ALL}")
        print(f"File Statistics:")
        print(f"- Processed: {file_processed}")
        print(f"- Skipped: {file_skipped}")
    
    # Print final statistics
    print(f"\n{Fore.CYAN}=== Final Statistics ==={Style.RESET_ALL}")
    print(f"Total items processed: {total_processed}")
    print(f"Total items skipped: {total_skipped}")
    print(f"Success rate: {(total_processed/(total_processed+total_skipped))*100:.2f}%")

def find_image(image_id: str, directories: list) -> str:
    """Find image file in multiple directories."""
    image_filename = f"{image_id}.jpeg"
    
    for directory in directories:
        image_path = os.path.join(directory, image_filename)
        if os.path.exists(image_path):
            return image_path
    
    return None

if __name__ == "__main__":
    print(f"{Fore.CYAN}Starting dataset classification...{Style.RESET_ALL}")
    process_dataset()
    print(f"{Fore.GREEN}Classification complete!{Style.RESET_ALL}")