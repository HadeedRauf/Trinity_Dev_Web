import requests
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from api.models import Product

class Command(BaseCommand):
    help = 'Fetch products from Open Food Facts API and add them to database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=20,
            help='Number of products to fetch (default: 20)',
        )
        parser.add_argument(
            '--category',
            type=str,
            default='',
            help='Category to search for (e.g., yogurt, cheese, bread)',
        )

    def handle(self, *args, **options):
        count = options['count']
        category = options['category'] or 'food'
        
        self.stdout.write(self.style.SUCCESS(f'🔍 Fetching {count} products from Open Food Facts API...'))
        self.stdout.write(f'📂 Category: {category}\n')
        
        base_url = 'https://world.openfoodfacts.org/cgi/search.pl'
        
        params = {
            'search_terms': category,
            'page_size': count,
            'json': 1,
            'fields': 'code,product_name,brands,image_url,categories,nutrition_grade_fr,nutriments'
        }
        
        try:
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'❌ Error fetching from API: {e}'))
            return
        
        products = data.get('products', [])
        
        if not products:
            self.stdout.write(self.style.WARNING('⚠️  No products found for this search'))
            return
        
        added_count = 0
        skipped_count = 0
        
        for idx, product_data in enumerate(products[:count], 1):
            try:
                # Extract required fields
                barcode = product_data.get('code', '').strip()
                name = product_data.get('product_name', '').strip()
                brand = product_data.get('brands', '').strip()
                image = product_data.get('image_url', '').strip()
                category_str = product_data.get('categories', '').strip()
                nutrition_grade = product_data.get('nutrition_grade_fr', '').upper().strip()
                nutriments = product_data.get('nutriments', {})
                
                # Skip if missing essential fields
                if not name or not barcode:
                    skipped_count += 1
                    continue
                
                # Validate nutrition grade
                if nutrition_grade not in ['A', 'B', 'C', 'D', 'E']:
                    nutrition_grade = ''
                
                # Generate random price between 2 and 15 USD
                price = Decimal(str(round(random.uniform(2, 15), 2)))
                
                # Build nutritional info
                nutritional_info = {
                    'energy_kcal': nutriments.get('energy-kcal_100g'),
                    'protein_g': nutriments.get('proteins_100g'),
                    'fat_g': nutriments.get('fat_100g'),
                    'carbs_g': nutriments.get('carbohydrates_100g'),
                    'fiber_g': nutriments.get('fiber_100g'),
                    'salt_g': nutriments.get('salt_100g'),
                }
                
                # Create or update product
                product, created = Product.objects.get_or_create(
                    barcode=barcode,
                    defaults={
                        'name': name,
                        'brand': brand,
                        'picture': image,
                        'category': category_str[:255],  # Limit to 255 chars
                        'nutrition_score': nutrition_grade,
                        'price': price,
                        'quantity': random.randint(10, 100),
                        'nutritional_info': nutritional_info,
                    }
                )
                
                if created:
                    added_count += 1
                    status = '✅'
                    self.stdout.write(f'{status} [{idx}/{len(products[:count])}] {name}')
                    self.stdout.write(f'   Brand: {brand}')
                    self.stdout.write(f'   Score: {nutrition_grade or "N/A"} | Price: ${price} | Qty: {product.quantity}')
                    if nutriments:
                        self.stdout.write(f'   Nutrition: {nutriments.get("energy-kcal_100g", "N/A")} kcal, '
                                        f'{nutriments.get("proteins_100g", "N/A")}g protein')
                    self.stdout.write('')
                else:
                    skipped_count += 1
            
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'⚠️  Error processing product: {e}'))
                skipped_count += 1
                continue
        
        self.stdout.write(self.style.SUCCESS(f'\n✨ Process Complete!'))
        self.stdout.write(self.style.SUCCESS(f'✅ Added: {added_count} products'))
        self.stdout.write(self.style.WARNING(f'⏭️  Skipped: {skipped_count} products'))
        self.stdout.write(self.style.SUCCESS(f'📊 Total in database: {Product.objects.count()} products'))
