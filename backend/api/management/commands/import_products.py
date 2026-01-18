from django.core.management.base import BaseCommand
from api.models import Product
from decimal import Decimal

class Command(BaseCommand):
    help = 'Import products with real images and nutrition data'

    def handle(self, *args, **options):
        self.stdout.write("🍎 Starting product import...\n")
        
        # Delete existing products
        Product.objects.all().delete()
        self.stdout.write("✅ Deleted existing products\n")
        
        # Real products with images from Wikimedia Commons and nutritional data
        products = [
            # Fruits & Vegetables
            {
                'name': 'Fuji Apple',
                'brand': 'FreshFarm',
                'category': 'Fruits & Vegetables',
                'price': 3.99,
                'nutrition_score': 'A',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Red_Apple.jpg/800px-Red_Apple.jpg',
                'nutritional_info': {
                    'energy': 52,
                    'carbohydrates': 13.8,
                    'protein': 0.3,
                    'fat': 0.2,
                    'fiber': 2.4,
                    'sugar': 10.4,
                    'salt': 0.002
                }
            },
            {
                'name': 'Fresh Bananas',
                'brand': 'Tropical Fresh',
                'category': 'Fruits & Vegetables',
                'price': 2.49,
                'nutrition_score': 'A',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Banana-Chocolate-Chip-Cookies-Recipe.jpg/800px-Banana-Chocolate-Chip-Cookies-Recipe.jpg',
                'nutritional_info': {
                    'energy': 89,
                    'carbohydrates': 23,
                    'protein': 1.1,
                    'fat': 0.3,
                    'fiber': 2.6,
                    'sugar': 12,
                    'potassium': 358
                }
            },
            {
                'name': 'Organic Carrots',
                'brand': 'FarmFresh',
                'category': 'Fruits & Vegetables',
                'price': 2.99,
                'nutrition_score': 'A',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Camponotus_flavomarginatus_ant.jpg/440px-Camponotus_flavomarginatus_ant.jpg',
                'nutritional_info': {
                    'energy': 41,
                    'carbohydrates': 9.6,
                    'protein': 0.9,
                    'fat': 0.2,
                    'fiber': 2.8,
                    'sugar': 4.7
                }
            },
            # Grains & Cereals
            {
                'name': 'Whole Wheat Bread',
                'brand': 'BakerBest',
                'category': 'Grains & Cereals',
                'price': 2.99,
                'nutrition_score': 'B',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Whole_wheat_bread.jpg/800px-Whole_wheat_bread.jpg',
                'nutritional_info': {
                    'energy': 247,
                    'carbohydrates': 43,
                    'protein': 9,
                    'fat': 4,
                    'fiber': 7,
                    'sugar': 4,
                    'salt': 1.5
                }
            },
            {
                'name': 'Brown Rice (1kg)',
                'brand': 'GrainMill',
                'category': 'Grains & Cereals',
                'price': 5.99,
                'nutrition_score': 'A',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Brown_Rice.jpg/800px-Brown_Rice.jpg',
                'nutritional_info': {
                    'energy': 112,
                    'carbohydrates': 24,
                    'protein': 2.6,
                    'fat': 0.9,
                    'fiber': 1.8,
                    'sugar': 0.2
                }
            },
            {
                'name': 'Rolled Oats Cereal',
                'brand': 'BreakfastBest',
                'category': 'Grains & Cereals',
                'price': 4.49,
                'nutrition_score': 'A',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Rolled_oats.jpg/800px-Rolled_oats.jpg',
                'nutritional_info': {
                    'energy': 389,
                    'carbohydrates': 66,
                    'protein': 17,
                    'fat': 6.9,
                    'fiber': 10.6,
                    'sugar': 0.8
                }
            },
            # Meat & Poultry
            {
                'name': 'Chicken Breast (500g)',
                'brand': 'FreshPoultry',
                'category': 'Meat & Poultry',
                'price': 7.99,
                'nutrition_score': 'A',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Chicken_breast.jpg/800px-Chicken_breast.jpg',
                'nutritional_info': {
                    'energy': 165,
                    'carbohydrates': 0,
                    'protein': 31,
                    'fat': 3.6,
                    'cholesterol': 85,
                    'sodium': 74
                }
            },
            {
                'name': 'Ground Beef (500g)',
                'brand': 'PrimeBeef',
                'category': 'Meat & Poultry',
                'price': 8.99,
                'nutrition_score': 'B',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Ground_beef.jpg/800px-Ground_beef.jpg',
                'nutritional_info': {
                    'energy': 215,
                    'carbohydrates': 0,
                    'protein': 22,
                    'fat': 13,
                    'cholesterol': 80,
                    'iron': 2.8
                }
            },
            {
                'name': 'Pork Chops (500g)',
                'brand': 'MeatMasters',
                'category': 'Meat & Poultry',
                'price': 9.99,
                'nutrition_score': 'B',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Pork_chops.jpg/800px-Pork_chops.jpg',
                'nutritional_info': {
                    'energy': 242,
                    'carbohydrates': 0,
                    'protein': 27,
                    'fat': 14,
                    'cholesterol': 82
                }
            },
            # Fish & Seafood
            {
                'name': 'Salmon Fillet (400g)',
                'brand': 'OceanFresh',
                'category': 'Fish & Seafood',
                'price': 15.99,
                'nutrition_score': 'A',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Salmon.jpg/800px-Salmon.jpg',
                'nutritional_info': {
                    'energy': 206,
                    'carbohydrates': 0,
                    'protein': 22,
                    'fat': 13,
                    'omega3': 2.3,
                    'vitamin_d': 570
                }
            },
            {
                'name': 'Fresh Cod Fillet',
                'brand': 'SeaFish',
                'category': 'Fish & Seafood',
                'price': 11.99,
                'nutrition_score': 'A',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Atlantic_cod.jpg/800px-Atlantic_cod.jpg',
                'nutritional_info': {
                    'energy': 82,
                    'carbohydrates': 0,
                    'protein': 17.7,
                    'fat': 0.7,
                    'selenium': 32
                }
            },
            {
                'name': 'Shrimp (500g)',
                'brand': 'OceanPrawn',
                'category': 'Fish & Seafood',
                'price': 12.99,
                'nutrition_score': 'A',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Shrimp_in_the_Seychelles.jpg/800px-Shrimp_in_the_Seychelles.jpg',
                'nutritional_info': {
                    'energy': 99,
                    'carbohydrates': 0.2,
                    'protein': 24,
                    'fat': 0.3,
                    'cholesterol': 189
                }
            },
            # Dairy
            {
                'name': 'Fresh Milk (1L)',
                'brand': 'DairyBest',
                'category': 'Dairy',
                'price': 2.99,
                'nutrition_score': 'A',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat_2_no_copyright.jpg/440px-Cat_2_no_copyright.jpg',
                'nutritional_info': {
                    'energy': 61,
                    'carbohydrates': 4.8,
                    'protein': 3.2,
                    'fat': 3.3,
                    'calcium': 113,
                    'vitamin_d': 0.05
                }
            },
            {
                'name': 'Cheddar Cheese (400g)',
                'brand': 'CheeseHouse',
                'category': 'Dairy',
                'price': 5.99,
                'nutrition_score': 'B',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Cheddar_cheese.jpg/800px-Cheddar_cheese.jpg',
                'nutritional_info': {
                    'energy': 403,
                    'carbohydrates': 1.3,
                    'protein': 23,
                    'fat': 33,
                    'calcium': 721,
                    'sodium': 630
                }
            },
            {
                'name': 'Greek Yogurt (500g)',
                'brand': 'YogurtPro',
                'category': 'Dairy',
                'price': 3.49,
                'nutrition_score': 'A',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Greek_yogurt_-_stonesoup.jpg/800px-Greek_yogurt_-_stonesoup.jpg',
                'nutritional_info': {
                    'energy': 59,
                    'carbohydrates': 3.3,
                    'protein': 10,
                    'fat': 0.4,
                    'calcium': 100,
                    'probiotics': 'present'
                }
            },
            # Fats & Oils
            {
                'name': 'Extra Virgin Olive Oil (500ml)',
                'brand': 'OliveGold',
                'category': 'Fats & Oils',
                'price': 8.99,
                'nutrition_score': 'A',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Olive_oil.jpg/800px-Olive_oil.jpg',
                'nutritional_info': {
                    'energy': 884,
                    'carbohydrates': 0,
                    'protein': 0,
                    'fat': 100,
                    'monounsaturated_fat': 73,
                    'polyphenols': 'high'
                }
            },
            {
                'name': 'Sunflower Oil (1L)',
                'brand': 'SunOil',
                'category': 'Fats & Oils',
                'price': 4.99,
                'nutrition_score': 'B',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Sunflower_oil.png/800px-Sunflower_oil.png',
                'nutritional_info': {
                    'energy': 884,
                    'carbohydrates': 0,
                    'protein': 0,
                    'fat': 100,
                    'vitamin_e': 41.08
                }
            },
            {
                'name': 'Coconut Oil (500ml)',
                'brand': 'CocoMiles',
                'category': 'Fats & Oils',
                'price': 7.99,
                'nutrition_score': 'B',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Coconut_oil.jpg/800px-Coconut_oil.jpg',
                'nutritional_info': {
                    'energy': 892,
                    'carbohydrates': 0,
                    'protein': 0,
                    'fat': 99.1,
                    'saturated_fat': 82.5
                }
            },
            # Sugars & Confectionery
            {
                'name': 'Raw Honey (500ml)',
                'brand': 'PureHoney',
                'category': 'Sugars & Confectionery',
                'price': 7.99,
                'nutrition_score': 'B',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Honey_glass.jpg/800px-Honey_glass.jpg',
                'nutritional_info': {
                    'energy': 304,
                    'carbohydrates': 82,
                    'protein': 0.3,
                    'fat': 0,
                    'sugar': 82,
                    'antioxidants': 'high'
                }
            },
            {
                'name': 'White Sugar (1kg)',
                'brand': 'SweetGrain',
                'category': 'Sugars & Confectionery',
                'price': 2.49,
                'nutrition_score': 'E',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/White_sugar.jpg/800px-White_sugar.jpg',
                'nutritional_info': {
                    'energy': 387,
                    'carbohydrates': 100,
                    'protein': 0,
                    'fat': 0,
                    'sugar': 100
                }
            },
            {
                'name': 'Dark Chocolate Bar (100g)',
                'brand': 'ChocoBrand',
                'category': 'Sugars & Confectionery',
                'price': 2.99,
                'nutrition_score': 'D',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Chocolate.jpg/800px-Chocolate.jpg',
                'nutritional_info': {
                    'energy': 598,
                    'carbohydrates': 46,
                    'protein': 12,
                    'fat': 43,
                    'iron': 11.9,
                    'magnesium': 176
                }
            },
            # Beverages
            {
                'name': 'Fresh Orange Juice (1L)',
                'brand': 'FreshJuice',
                'category': 'Beverages',
                'price': 3.99,
                'nutrition_score': 'B',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Orange_juice_glass.jpg/800px-Orange_juice_glass.jpg',
                'nutritional_info': {
                    'energy': 47,
                    'carbohydrates': 11,
                    'protein': 0.7,
                    'fat': 0.3,
                    'vitamin_c': 50,
                    'sugar': 9.3
                }
            },
            {
                'name': 'Premium Coffee Beans (500g)',
                'brand': 'BeanBrew',
                'category': 'Beverages',
                'price': 7.99,
                'nutrition_score': 'A',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Coffee_beans_-_Ethiopian_Yirgacheffe.jpg/800px-Coffee_beans_-_Ethiopian_Yirgacheffe.jpg',
                'nutritional_info': {
                    'energy': 0,
                    'carbohydrates': 3.6,
                    'protein': 0.2,
                    'fat': 0.3,
                    'caffeine': 95
                }
            },
            {
                'name': 'Green Tea (20 bags)',
                'brand': 'TeaLeaf',
                'category': 'Beverages',
                'price': 4.99,
                'nutrition_score': 'A',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Green_tea_04.jpg/800px-Green_tea_04.jpg',
                'nutritional_info': {
                    'energy': 0,
                    'carbohydrates': 0,
                    'protein': 0,
                    'fat': 0,
                    'caffeine': 25,
                    'antioxidants': 'high'
                }
            },
            # Ready-to-eat
            {
                'name': 'Frozen Margherita Pizza',
                'brand': 'FrozenPizza',
                'category': 'Ready-to-eat',
                'price': 8.99,
                'nutrition_score': 'C',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Pizza.jpg/800px-Pizza.jpg',
                'nutritional_info': {
                    'energy': 270,
                    'carbohydrates': 36,
                    'protein': 11,
                    'fat': 8,
                    'sodium': 650,
                    'calcium': 250
                }
            },
            {
                'name': 'Prepared Garden Salad (200g)',
                'brand': 'HealthySalad',
                'category': 'Ready-to-eat',
                'price': 6.99,
                'nutrition_score': 'A',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Mixed_green_salad.jpg/800px-Mixed_green_salad.jpg',
                'nutritional_info': {
                    'energy': 15,
                    'carbohydrates': 3,
                    'protein': 1.2,
                    'fat': 0.2,
                    'fiber': 0.7,
                    'vitamins': 'A,C,K'
                }
            },
            {
                'name': 'Grilled Chicken Sandwich',
                'brand': 'QuickMeal',
                'category': 'Ready-to-eat',
                'price': 7.99,
                'nutrition_score': 'B',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Chicken_sandwich.jpg/800px-Chicken_sandwich.jpg',
                'nutritional_info': {
                    'energy': 320,
                    'carbohydrates': 38,
                    'protein': 28,
                    'fat': 8,
                    'sodium': 720
                }
            },
            # Condiments/Sauces/Spices
            {
                'name': 'Organic Tomato Sauce (500ml)',
                'brand': 'SaucePerfect',
                'category': 'Condiments/Sauces/Spices',
                'price': 2.99,
                'nutrition_score': 'B',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Tomato_sauce.jpg/800px-Tomato_sauce.jpg',
                'nutritional_info': {
                    'energy': 31,
                    'carbohydrates': 6,
                    'protein': 1.3,
                    'fat': 0.2,
                    'lycopene': 'high',
                    'sodium': 590
                }
            },
            {
                'name': 'Premium Soy Sauce (250ml)',
                'brand': 'AsianFlavor',
                'category': 'Condiments/Sauces/Spices',
                'price': 3.49,
                'nutrition_score': 'A',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Soy_sauce.jpg/800px-Soy_sauce.jpg',
                'nutritional_info': {
                    'energy': 60,
                    'carbohydrates': 5.5,
                    'protein': 8.1,
                    'fat': 0.5,
                    'sodium': 5586
                }
            },
            {
                'name': 'Tomato Ketchup (500ml)',
                'brand': 'TomatoKetchup',
                'category': 'Condiments/Sauces/Spices',
                'price': 2.49,
                'nutrition_score': 'D',
                'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Ketchup.jpg/800px-Ketchup.jpg',
                'nutritional_info': {
                    'energy': 100,
                    'carbohydrates': 24,
                    'protein': 1.7,
                    'fat': 0.1,
                    'sugar': 22,
                    'sodium': 1110
                }
            },
        ]
        
        # Create products
        for product_data in products:
            barcode = f'EAN-{product_data["name"][:10].upper()}'
            Product.objects.create(
                name=product_data['name'],
                brand=product_data['brand'],
                category=product_data['category'],
                price=Decimal(str(product_data['price'])),
                nutrition_score=product_data['nutrition_score'],
                picture=product_data['picture'],
                nutritional_info=product_data['nutritional_info'],
                barcode=barcode,
                quantity=50
            )
            self.stdout.write(f"✅ {product_data['name']}")
        
        self.stdout.write(self.style.SUCCESS(f"\n✅ Import completed! Created {len(products)} products"))
