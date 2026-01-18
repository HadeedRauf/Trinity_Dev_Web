from django.core.management.base import BaseCommand
from api.models import Product
import requests
from decimal import Decimal
import time

class Command(BaseCommand):
    help = 'Import real food products from Open Food Facts API'

    def handle(self, *args, **options):
        self.stdout.write("🍎 Starting Open Food Facts import...\n")
        
        # First, delete all existing products
        count = Product.objects.count()
        self.stdout.write(f"🗑️  Deleting {count} existing products...")
        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("✅ All products deleted"))
        
        # Categories and search terms
        categories = {
            'Fruits & Vegetables': ['apple', 'banana', 'carrot', 'tomato', 'lettuce'],
            'Grains & Cereals': ['bread', 'rice', 'oatmeal', 'pasta', 'cereal'],
            'Meat & Poultry': ['chicken', 'beef', 'pork', 'turkey'],
            'Fish & Seafood': ['salmon', 'tuna', 'cod', 'shrimp'],
            'Dairy': ['milk', 'cheese', 'yogurt', 'butter'],
            'Fats & Oils': ['olive oil', 'sunflower oil', 'butter', 'coconut oil'],
            'Sugars & Confectionery': ['honey', 'chocolate', 'sugar', 'candy'],
            'Beverages': ['orange juice', 'coffee', 'tea', 'water'],
            'Ready-to-eat': ['pizza', 'sandwich', 'salad', 'burger'],
            'Condiments/Sauces/Spices': ['tomato sauce', 'soy sauce', 'salt', 'pepper'],
        }
        
        products_created = 0
        
        for category, search_terms in categories.items():
            self.stdout.write(f"\n📦 Category: {category}")
            
            for search_term in search_terms:
                try:
                    products = self._fetch_from_openfoodfacts(search_term)
                    
                    for product_data in products[:2]:  # Get 2 products per search term
                        created = self._create_product(product_data, category)
                        if created:
                            products_created += 1
                            self.stdout.write(f"  ✅ {product_data['name']}")
                        
                        time.sleep(0.5)  # Rate limiting
                    
                except Exception as e:
                    self.stdout.write(f"  ⚠️  Error fetching {search_term}: {str(e)}")
                    continue
        
        self.stdout.write(self.style.SUCCESS(f"\n✅ Import completed! Created {products_created} products"))

    def _fetch_from_openfoodfacts(self, search_term):
        """Fetch products from Open Food Facts API"""
        url = 'https://world.openfoodfacts.org/cgi/search.pl'
        params = {
            'search_terms': search_term,
            'search_simple': 1,
            'json': 1,
            'page_size': 20,
            'fields': 'code,name,brands,image_front_url,nutriscore_grade,nutriments,quantity'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            products = data.get('products', [])
            
            # Filter products that have necessary data
            filtered = []
            for p in products:
                if p.get('name') and p.get('image_front_url'):
                    filtered.append(p)
            
            return filtered
        except Exception as e:
            print(f'Error fetching from OpenFoodFacts: {e}')
            return []

    def _create_product(self, product_data, category):
        """Create a product from OpenFoodFacts data"""
        try:
            name = product_data.get('name', '').strip()
            if not name or len(name) > 255:
                return False
            
            barcode = product_data.get('code', '')
            
            # Check if product already exists
            if barcode and Product.objects.filter(barcode=barcode).exists():
                return False
            
            brand = product_data.get('brands', '').strip()
            if len(brand) > 255:
                brand = brand[:255]
            
            image_url = product_data.get('image_front_url', '')
            
            # Nutrition score (A-E)
            nutrition_score = product_data.get('nutriscore_grade', 'C').upper()
            if nutrition_score not in ['A', 'B', 'C', 'D', 'E']:
                nutrition_score = 'C'
            
            # Get nutritional info
            nutriments = product_data.get('nutriments', {})
            
            # Generate a realistic price based on category
            price = self._generate_price(category)
            
            product = Product.objects.create(
                name=name,
                price=price,
                brand=brand,
                picture=image_url,
                category=category,
                nutrition_score=nutrition_score,
                barcode=barcode if barcode else f'OFF-{name[:10].upper()}',
                quantity=50,  # Default quantity
                nutritional_info={
                    'energy': nutriments.get('energy_kcal', 0),
                    'fat': nutriments.get('fat', 0),
                    'carbohydrates': nutriments.get('carbohydrates', 0),
                    'protein': nutriments.get('protein', 0),
                    'salt': nutriments.get('salt', 0),
                    'sugar': nutriments.get('sugars', 0)
                }
            )
            
            return True
        except Exception as e:
            print(f'Error creating product: {e}')
            return False

    def _generate_price(self, category):
        """Generate realistic prices based on category"""
        price_ranges = {
            'Fruits & Vegetables': (2.0, 5.0),
            'Grains & Cereals': (2.0, 7.0),
            'Meat & Poultry': (7.0, 15.0),
            'Fish & Seafood': (10.0, 20.0),
            'Dairy': (2.0, 8.0),
            'Fats & Oils': (5.0, 12.0),
            'Sugars & Confectionery': (2.0, 8.0),
            'Beverages': (2.0, 8.0),
            'Ready-to-eat': (5.0, 15.0),
            'Condiments/Sauces/Spices': (2.0, 10.0),
        }
        
        min_price, max_price = price_ranges.get(category, (3.0, 10.0))
        # Use a simple hash-based deterministic price
        price = (min_price + max_price) / 2
        return Decimal(str(round(price, 2)))
