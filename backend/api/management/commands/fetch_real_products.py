from django.core.management.base import BaseCommand
from api.models import Product
import requests
from decimal import Decimal
import time

class Command(BaseCommand):
    help = 'Fetch real products from Open Food Facts with complete nutrition data per 100g'

    def handle(self, *args, **options):
        self.stdout.write("🍎 Fetching real products from Open Food Facts...\n")
        
        # Delete existing products
        Product.objects.all().delete()
        self.stdout.write("✅ Cleared database\n")
        
        # Fixed list of search terms that work well
        searches = [
            ('Fruits & Vegetables', 'apple'),
            ('Fruits & Vegetables', 'banana'),
            ('Fruits & Vegetables', 'carrot'),
            ('Grains & Cereals', 'bread'),
            ('Grains & Cereals', 'rice'),
            ('Grains & Cereals', 'oats'),
            ('Meat & Poultry', 'chicken'),
            ('Meat & Poultry', 'beef'),
            ('Meat & Poultry', 'pork'),
            ('Fish & Seafood', 'salmon'),
            ('Fish & Seafood', 'tuna'),
            ('Fish & Seafood', 'cod'),
            ('Dairy', 'milk'),
            ('Dairy', 'cheese'),
            ('Dairy', 'yogurt'),
            ('Fats & Oils', 'olive oil'),
            ('Fats & Oils', 'sunflower oil'),
            ('Fats & Oils', 'coconut oil'),
            ('Sugars & Confectionery', 'honey'),
            ('Sugars & Confectionery', 'chocolate'),
            ('Sugars & Confectionery', 'sugar'),
            ('Beverages', 'orange juice'),
            ('Beverages', 'coffee'),
            ('Beverages', 'tea'),
            ('Ready-to-eat', 'pizza'),
            ('Ready-to-eat', 'sandwich'),
            ('Ready-to-eat', 'salad'),
            ('Condiments/Sauces/Spices', 'tomato sauce'),
            ('Condiments/Sauces/Spices', 'soy sauce'),
            ('Condiments/Sauces/Spices', 'ketchup'),
        ]
        
        products_created = 0
        
        for category, search_term in searches:
            try:
                self.stdout.write(f"  Searching: {search_term}...", ending='')
                product_data = self._fetch_product(search_term)
                
                if product_data:
                    if self._create_product(product_data, category):
                        products_created += 1
                        self.stdout.write(f" ✅ {product_data['name']}")
                    else:
                        self.stdout.write(f" ⚠️  Failed to create")
                else:
                    self.stdout.write(f" ❌ No data")
                
                time.sleep(0.5)  # Rate limiting
                    
            except Exception as e:
                self.stdout.write(f" ❌ Error: {str(e)}")
                continue
        
        self.stdout.write(self.style.SUCCESS(f"\n✅ Import complete! Created {products_created} products"))

    def _fetch_product(self, search_term):
        """Fetch ONE product from Open Food Facts"""
        url = 'https://world.openfoodfacts.org/cgi/search.pl'
        params = {
            'search_terms': search_term,
            'json': 1,
            'page_size': 1,
            'action': 'process',
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            products = data.get('products', [])
            if not products:
                return None
            
            p = products[0]
            
            # Check for required fields
            name = p.get('product_name', '').strip()
            image = p.get('image_front_url')
            nutriments = p.get('nutriments', {})
            
            if not name or not image:
                return None
            
            return {
                'name': name[:100],
                'brand': (p.get('brands', '') or '')[:100],
                'image': image,
                'nutriments': nutriments,
                'nutriscore': p.get('nutriscore_grade', 'C').upper(),
                'barcode': p.get('code', ''),
            }
            
        except Exception as e:
            print(f'\nError fetching: {e}')
            return None

    def _create_product(self, product_data, category):
        """Create product in database"""
        try:
            name = product_data.get('name', '').strip()
            if not name or len(name) > 255:
                return False
            
            barcode = product_data.get('barcode', f'EAN-{name[:15].upper()}')
            
            # Check if already exists
            if barcode and Product.objects.filter(barcode=barcode).exists():
                return False
            
            brand = product_data.get('brand', '')[:100]
            image = product_data.get('image', '')
            nutriscore = product_data.get('nutriscore', 'C')
            
            if nutriscore not in ['A', 'B', 'C', 'D', 'E']:
                nutriscore = 'C'
            
            nutriments = product_data.get('nutriments', {})
            
            # Extract nutrition data per 100g
            nutritional_info = {
                'energy_kcal_100g': float(nutriments.get('energy-kcal_100g', nutriments.get('energy_kcal_100g', 0)) or 0),
                'carbohydrates_100g': float(nutriments.get('carbohydrates_100g', 0) or 0),
                'fat_100g': float(nutriments.get('fat_100g', 0) or 0),
                'proteins_100g': float(nutriments.get('proteins_100g', 0) or 0),
                'sugars_100g': float(nutriments.get('sugars_100g', 0) or 0),
                'salt_100g': float(nutriments.get('salt_100g', 0) or 0),
                'fiber_100g': float(nutriments.get('fiber_100g', 0) or 0),
            }
            
            # Price based on category
            price_map = {
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
            price = price_map.get(category, Decimal('5.99'))
            
            Product.objects.create(
                name=name,
                brand=brand,
                price=price,
                picture=image,
                category=category,
                nutrition_score=nutriscore,
                barcode=barcode,
                quantity=50,
                nutritional_info=nutritional_info
            )
            
            return True
            
        except Exception as e:
            print(f'Error creating product: {e}')
            return False
