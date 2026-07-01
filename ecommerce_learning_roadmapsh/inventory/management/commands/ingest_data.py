import os
import pandas as pd
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand
from inventory.models import RawProduct

class Command(BaseCommand):
    help = 'Ingest Amazon Data into RawProduct model'

    def handle(self, *args, **kwargs):
        # 1. SETUP
        folder_path = r"G:\The Field of Programming\ecommerce_learning_roadmapsh\amazon_product_data"
        
        if not os.path.exists(folder_path):
            self.stdout.write(self.style.ERROR(f"Folder path does not exist: {folder_path}"))
            return
        
        batch_size = 1000
        buffer = []
        
        # This maps CSV headers (keys) to Your Model Fields (values)
        # CHECK THESE KEYS: Make sure they match your CSV headers exactly!
        column_map = {
            'name': 'name',
            'main_category': 'main_category',
            'sub_category': 'sub_category',
            'image': 'image',
            'link': 'link',
            'ratings': 'ratings',
            'no_of_ratings': 'no_of_ratings',
            'discount_price': 'discount_price',
            'actual_price': 'actual_price'
        }

        print("--- Starting Safe Ingestion ---")

        for filename in os.listdir(folder_path):
            if not filename.endswith('.csv'): continue
            
            f_path = os.path.join(folder_path, filename)
            print(f"Reading: {filename}")

            try:
                # Read CSV
                df = pd.read_csv(f_path)
                
                # 2. THE LOOP
                for _, row in df.iterrows():
                    
                    # 3. SAFETY CLEANING (The most important part)
                    # We extract values safely to prevent database crashes
                    
                    product_data = {
                        # Text Fields (Truncate to 255 to fit your CharField)
                        'name': str(row.get('name', ''))[:255],
                        'main_category': str(row.get('main_category', ''))[:255],
                        'sub_category': str(row.get('sub_category', ''))[:255],
                        'image': str(row.get('image', ''))[:500],
                        'link': str(row.get('link', ''))[:500],
                        
                        # Number Fields (Must use helper functions)
                        'ratings': self.clean_float(row.get('ratings')),
                        'no_of_ratings': self.clean_int(row.get('no_of_ratings')),
                        'discount_price': self.clean_money(row.get('discount_price')),
                        'actual_price': self.clean_money(row.get('actual_price')),
                    }

                    buffer.append(RawProduct(**product_data))

                    # 4. BATCH SAVING
                    if len(buffer) >= batch_size:
                        RawProduct.objects.bulk_create(buffer, ignore_conflicts=True)
                        buffer = []
                        print(f"  > Saved {batch_size} products...")

            except Exception as e:
                print(f"  [ERROR] Failed on {filename}: {e}")

        # Final flush
        if buffer:
            RawProduct.objects.bulk_create(buffer, ignore_conflicts=True)
            print(f"Done. Final batch: {len(buffer)}")


    # --- HELPER FUNCTIONS (The Armor) ---

    def clean_money(self, value):
        """Converts '₹1,299.00' -> Decimal('1299.00')"""
        if pd.isna(value) or str(value).strip() == '':
            return None
        
        # Remove currency symbols and commas
        clean_str = str(value).replace('₹', '').replace('$', '').replace(',', '').strip()
        
        try:
            return Decimal(clean_str)
        except InvalidOperation:
            return None

    def clean_float(self, value):
        """Safely returns a float or None"""
        if pd.isna(value) or value == '':
            return None
        try:
            return float(value)
        except ValueError:
            return None

    def clean_int(self, value):
        """Safely returns an int or None"""
        if pd.isna(value) or value == '':
            return None
        try:
            # Handle "1,000" string or 1000.0 float
            clean_str = str(value).replace(',', '').split('.')[0] 
            return int(clean_str)
        except ValueError:
            return None