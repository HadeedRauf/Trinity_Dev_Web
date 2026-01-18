from django.core.management.base import BaseCommand
from api.models import Product
import requests
from decimal import Decimal
import time
import json

class Command(BaseCommand):
    help = 'Import real food products from Open Food Facts API with complete nutrition data'

    def handle(self, *args, **options):
        self.stdout.write("🍎 Importing products from Open Food Facts...\n")
        
        # Delete all existing products first
        Product.objects.all().delete()
        self.stdout.write("✅ Cleared existing products\n")
        
        # Search queries for each category
        searches = {
            'Fruits & Vegetables': ['apple', 'banana', 'carrot', 'tomato', 'lettuce', 'orange'],
            'Grains & Cereals': ['bread', 'rice', 'oatmeal', 'pasta', 'cereal', 'wheat'],
            'Meat & Poultry': ['chicken', 'beef', 'pork', 'turkey', 'lamb'],
            'Fish & Seafood': ['salmon', 'tuna', 'cod', 'shrimp', 'mackerel'],
            'Dairy': ['milk', 'cheese', 'yogurt', 'butter', 'cream'],
            'Fats & Oils': ['olive oil', 'sunflower oil', 'coconut oil', 'vegetable oil'],
            'Sugars & Confectionery': ['honey', 'chocolate', 'sugar', 'candy', 'jam'],
            'Beverages': ['orange juice', 'coffee', 'tea', 'water', 'apple juice'],
            'Ready-to-eat': ['pizza', 'sandwich', 'salad', 'burger', 'soup'],
            'Condiments/Sauces/Spices': ['tomato sauce', 'soy sauce', 'salt', 'pepper', 'mustard'],
        }
        
        products_created = 0
        
        for category, search_terms in searches.items():
            self.stdout.write(f"\n📦 Category: {category}")
            
            for search_term in search_terms:
                try:
                    products = self._fetch_products(search_term)
                    
                    for product_data in products[:1]:  # Get 1 product per search term
                        if self._create_product(product_data, category):
                            products_created += 1
                            self.stdout.write(f"  ✅ {product_data['name']}")
                        
                        time.sleep(0.3)  # Rate limiting
                        
                except Exception as e:
                    self.stdout.write(f"  ⚠️  Error with {search_term}: {str(e)}")
                    continue
        
        self.stdout.write(self.style.SUCCESS(f"\n✅ Import complete! Created {products_created} products"))

    def _fetch_products(self, search_term):
        """Fetch products from Open Food Facts API"""
        url = 'https://world.openfoodfacts.org/cgi/search.pl'
        params = {
            'search_terms': search_term,
            'search_simple': 1,
            'json': 1,
            'page_size': 5,
            'action': 'process',
            'fields': 'code,name,brands,image_front_url,image_front_small_url,nutriscore_grade,nutriments,quantity,energy-kcal_100g,fat_100g,carbohydrates_100g,sugars_100g,proteins_100g,salt_100g,fiber_100g'
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            products = data.get('products', [])
            
            # Filter to ensure we have necessary data
            filtered = []
            for p in products:
                name = p.get('name', '').strip()
                image = p.get('image_front_url') or p.get('image_front_small_url')
                nutriments = p.get('nutriments', {})
                
                # Must have name, image, and some nutrition data
                if name and image and nutriments:
                    filtered.append(p)
            
            return filtered[:3]  # Return top 3 results
            
        except Exception as e:
            print(f'Error fetching: {e}')
            return []

    def _create_product(self, product_data, category):
        """Create product with complete nutrition data per 100g"""
        try:
            name = product_data.get('name', '').strip()
            if not name or len(name) > 255:
                return False
            
            barcode = product_data.get('code', '')
            
            # Check if already exists
            if barcode and Product.objects.filter(barcode=barcode).exists():
                return False
            
            brand = product_data.get('brands', '').strip()
            if len(brand) > 255:
                brand = brand[:150]
            
            # Get image (prefer larger version)
            image_url = product_data.get('image_front_url', '')
            if not image_url:
                image_url = product_data.get('image_front_small_url', '')
            
            # Get nutrition score (A-E)
            nutrition_score = product_data.get('nutriscore_grade', 'C').upper()
            if nutrition_score not in ['A', 'B', 'C', 'D', 'E']:
                nutrition_score = 'C'
            
            nutriments = product_data.get('nutriments', {})
            
            # Extract per 100g nutrition values
            nutritional_info = {
                'energy_kcal_100g': nutriments.get('energy-kcal_100g') or nutriments.get('energy_kcal_100g') or 0,
                'energy_kj_100g': nutriments.get('energy-kj_100g') or nutriments.get('energy_kj_100g') or 0,
                'fat_100g': nutriments.get('fat_100g') or 0,
                'carbohydrates_100g': nutriments.get('carbohydrates_100g') or 0,
                'sugars_100g': nutriments.get('sugars_100g') or 0,
                'proteins_100g': nutriments.get('proteins_100g') or 0,
                'salt_100g': nutriments.get('salt_100g') or 0,
                'fiber_100g': nutriments.get('fiber_100g') or 0,
                'sodium_100g': nutriments.get('sodium_100g') or 0,
            }
            
            # Determine price based on category
            price = self._get_price(category)
            
            # Create product
            Product.objects.create(
                name=name,
                price=price,
                brand=brand,
                picture=image_url,
                category=category,
                nutrition_score=nutrition_score,
                barcode=barcode if barcode else f'EAN-{name[:20].upper()}',
                quantity=50,
                nutritional_info=nutritional_info
            )
            
            return True
            
        except Exception as e:
            print(f'Error creating product: {e}')
            return False

    def _get_price(self, category):
        """Get realistic price for category"""
        prices = {
            'Fruits & Vegetables': Decimal('2.99'),
            'Grains & Cereals': Decimal('4.99'),
            'Meat & Poultry': Decimal('8.99'),
            'Fish & Seafood': Decimal('12.99'),
            'Dairy': Decimal('3.99'),
            'Fats & Oils': Decimal('6.99'),
            'Sugars & Confectionery': Decimal('3.49'),
            'Beverages': Decimal('4.49'),
            'Ready-to-eat': Decimal('7.99'),
            'Condiments/Sauces/Spices': Decimal('2.99'),
        }
        return prices.get(category, Decimal('5.99'))
