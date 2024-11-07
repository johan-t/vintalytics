import csv
from datetime import datetime, timedelta
import time
from pyVinted import Vinted
import os
import requests
from urllib.parse import urlparse
import argparse
import calendar

vinted = Vinted()

def download_image(url, item_id):
    # Create images directory if it doesn't exist
    if not os.path.exists("images"):
        os.makedirs("images")

    # Get file extension from URL
    ext = os.path.splitext(urlparse(url).path)[1] or ".jpg"
    filepath = f"images/{item_id}{ext}"

    # Skip if image already exists
    if os.path.exists(filepath):
        return

    # Download and save image
    response = requests.get(url)
    if response.status_code == 200:
        with open(filepath, "wb") as f:
            f.write(response.content)

def fetch_and_save_items(start_date: datetime, end_date: datetime):
    """Fetch items for a specific date range"""
    
    # Create filename with date range and current timestamp
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Ensure analytics/data directory exists
    data_dir = "analytics/vintalytics/data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Format filename with start and end dates
    filename = os.path.join(
        data_dir, 
        f"{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}_{current_time}.csv"
    )
    
    print(f"\n🔍 Scraping data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Create images directory if it doesn't exist
    images_dir = os.path.join(data_dir, "images")
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    
    # Update download_image function to use the new path
    def download_image(url, item_id):
        # Get file extension from URL
        ext = os.path.splitext(urlparse(url).path)[1] or ".jpg"
        filepath = os.path.join(images_dir, f"{item_id}{ext}")

        # Skip if image already exists
        if os.path.exists(filepath):
            return

        # Download and save image
        response = requests.get(url)
        if response.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(response.content)
    
    # Open file in write mode (not append since it's a new file)
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Updated header with new columns
        writer.writerow([
            "ID", "Photo", "Title", "Brand", "Price", "URL", 
            "Currency", "Item_Date", "Colors", "Materials", 
            "Styles", "Categories"
        ])

        current_date = end_date
        total_items = 0

        # Iterate through each day backwards
        while current_date >= start_date:
            try:
                timestamp = int(current_date.timestamp())
                page = 1
                items_found = True
                daily_items = 0

                print(f"\n📆 Processing {current_date.strftime('%Y-%m-%d')}...")

                # Iterate through all pages for current day
                while items_found and page <= 100:  # Page limit for safety
                    try:
                        print(f"  📄 Fetching page {page}...", end='\r')

                        # Fetch items for current day and page
                        search_result = vinted.items.search(
                            "https://www.vinted.de/vetement?order=newest_first&price_to=100&currency=EUR",
                            100,  # Maximum items per page
                            page,
                            time=timestamp,
                        )

                        # Check if search_result is None or empty
                        if not search_result or len(search_result) == 0:
                            items_found = False
                            break

                        # Process items
                        for item in search_result:
                            try:
                                # Download image
                                if hasattr(item, "photo") and item.photo:
                                    download_image(item.photo, item.id)

                                # Updated row with new columns
                                writer.writerow([
                                    getattr(item, "id", ""),
                                    getattr(item, "photo", ""),
                                    getattr(item, "title", ""),
                                    getattr(item, "brand_title", ""),
                                    getattr(item, "price", ""),
                                    getattr(item, "url", ""),
                                    getattr(item, "currency", ""),
                                    current_date.strftime("%Y-%m-%d"),
                                    # New columns - extract from item attributes if available
                                    getattr(item, "color", ""),  # or color_title
                                    getattr(item, "materials", ""),  # Might be a list
                                    getattr(item, "style", ""),  # or style_title
                                    getattr(item, "categories", "")  # Might be a list
                                ])
                                daily_items += 1
                                total_items += 1
                            except Exception as item_error:
                                print(f"    ⚠️ Error processing item: {str(item_error)}")
                                continue

                        page += 1
                        time.sleep(2)  # Rate limiting

                    except Exception as page_error:
                        print(f"    ⚠️ Error on page {page}: {str(page_error)}")
                        items_found = False
                        break

                print(f"  ✅ Found {daily_items} items for {current_date.strftime('%Y-%m-%d')}")
                current_date -= timedelta(days=1)

            except Exception as date_error:
                print(f"    ⚠️ Error processing date: {str(date_error)}")
                current_date -= timedelta(days=1)
                continue

    print(f"\n✨ Completed scraping for {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"📊 Total items collected: {total_items}")
    print(f"💾 Data saved to: {filename}\n")

def main():
    parser = argparse.ArgumentParser(description='Scrape Vinted data for a specific date range')
    parser.add_argument('start_date', type=str, help='Start date (YYYY-MM-DD)')
    parser.add_argument('end_date', type=str, help='End date (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    try:
        # Parse dates
        start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
        
        # Validate dates
        current_date = datetime.now()
        if start_date > end_date:
            print("❌ Error: Start date must be before end date")
            return
        if start_date > current_date or end_date > current_date:
            print("❌ Error: Dates cannot be in the future")
            return
        if start_date.year < 2010:
            print("❌ Error: Dates before 2010 are not supported")
            return
            
        # Calculate date range
        date_range = (end_date - start_date).days
        print(f"📅 Scraping {date_range + 1} days of data")
        
        fetch_and_save_items(start_date, end_date)
        
    except ValueError:
        print("❌ Error: Invalid date format. Please use YYYY-MM-DD")
        return

if __name__ == "__main__":
    main()