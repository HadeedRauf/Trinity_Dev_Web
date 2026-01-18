from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Product, Customer, Invoice, InvoiceItem, UserProfile
import uuid
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seeds the database with initial data (admin user, test customers, and products)'

    def handle(self, *args, **options):
        self.stdout.write("🌱 Starting data seeding...\n")

        # Create admin user
        self.create_admin_user()

        # Create test customers
        self.create_test_customers()

        # Create products
        self.create_products()

        # Create sample invoices
        self.create_sample_invoices()

        self.stdout.write(self.style.SUCCESS("\n✅ Data seeding completed successfully!"))

    def create_admin_user(self):
        """Create or update admin user"""
        if User.objects.filter(username='admin').exists():
            self.stdout.write("ℹ️  Admin user already exists, skipping...")
            return

        admin = User.objects.create_superuser(
            username='admin',
            email='admin@trinity.com',
            password='admin'
        )

        UserProfile.objects.create(
            user=admin,
            role='admin'
        )

        self.stdout.write(self.style.SUCCESS("✅ Admin user created: admin / admin"))

    def create_test_customers(self):
        """Create test customer users"""
        test_customers = [
            {
                'username': 'john_doe',
                'password': 'john123',
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'customer_data': {
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'phone': '+1 555-0101',
                    'address': '123 Main Street',
                    'city': 'New York',
                    'zip_code': '10001',
                    'country': 'USA'
                }
            },
            {
                'username': 'jane_smith',
                'password': 'jane123',
                'email': 'jane@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'customer_data': {
                    'first_name': 'Jane',
                    'last_name': 'Smith',
                    'phone': '+1 555-0102',
                    'address': '456 Oak Avenue',
                    'city': 'Los Angeles',
                    'zip_code': '90001',
                    'country': 'USA'
                }
            },
            {
                'username': 'bob_wilson',
                'password': 'bob123',
                'email': 'bob@example.com',
                'first_name': 'Bob',
                'last_name': 'Wilson',
                'customer_data': {
                    'first_name': 'Bob',
                    'last_name': 'Wilson',
                    'phone': '+1 555-0103',
                    'address': '789 Pine Road',
                    'city': 'Chicago',
                    'zip_code': '60601',
                    'country': 'USA'
                }
            },
            {
                'username': 'alice_jones',
                'password': 'alice123',
                'email': 'alice@example.com',
                'first_name': 'Alice',
                'last_name': 'Jones',
                'customer_data': {
                    'first_name': 'Alice',
                    'last_name': 'Jones',
                    'phone': '+1 555-0104',
                    'address': '321 Elm Street',
                    'city': 'Houston',
                    'zip_code': '77001',
                    'country': 'USA'
                }
            }
        ]

        created_count = 0
        for cust in test_customers:
            if User.objects.filter(username=cust['username']).exists():
                continue

            # Create user
            user = User.objects.create_user(
                username=cust['username'],
                password=cust['password'],
                email=cust['email'],
                first_name=cust['first_name'],
                last_name=cust['last_name']
            )

            # Create user profile
            UserProfile.objects.create(
                user=user,
                role='customer'
            )

            # Create customer record
            Customer.objects.create(**cust['customer_data'])

            created_count += 1

        if created_count > 0:
            self.stdout.write(self.style.SUCCESS(f"✅ Created {created_count} test customers"))
        else:
            self.stdout.write("ℹ️  Test customers already exist, skipping...")

    def create_products(self):
        """Create products across all categories"""
        if Product.objects.count() > 0:
            self.stdout.write("ℹ️  Products already exist, skipping...")
            return

        products_data = [
            # Fruits & Vegetables (3)
            {"name": "Organic Apples", "price": 3.99, "brand": "FreshFarm", "category": "Fruits & Vegetables", "nutrition_score": "A", "quantity": 50},
            {"name": "Bananas", "price": 2.49, "brand": "Tropical", "category": "Fruits & Vegetables", "nutrition_score": "A", "quantity": 100},
            {"name": "Carrots (1kg)", "price": 2.99, "brand": "FarmFresh", "category": "Fruits & Vegetables", "nutrition_score": "A", "quantity": 75},

            # Grains & Cereals (3)
            {"name": "Whole Wheat Bread", "price": 2.99, "brand": "BakerBest", "category": "Grains & Cereals", "nutrition_score": "B", "quantity": 45},
            {"name": "Brown Rice (1kg)", "price": 5.99, "brand": "GrainMill", "category": "Grains & Cereals", "nutrition_score": "A", "quantity": 60},
            {"name": "Oatmeal", "price": 4.49, "brand": "BreakfastBest", "category": "Grains & Cereals", "nutrition_score": "A", "quantity": 50},

            # Meat & Poultry (3)
            {"name": "Chicken Breast (500g)", "price": 7.99, "brand": "FreshPoultry", "category": "Meat & Poultry", "nutrition_score": "A", "quantity": 60},
            {"name": "Ground Beef (500g)", "price": 8.99, "brand": "PrimeBeef", "category": "Meat & Poultry", "nutrition_score": "B", "quantity": 50},
            {"name": "Pork Chops", "price": 9.99, "brand": "MeatMasters", "category": "Meat & Poultry", "nutrition_score": "B", "quantity": 30},

            # Fish & Seafood (3)
            {"name": "Salmon Fillet", "price": 15.99, "brand": "OceanFresh", "category": "Fish & Seafood", "nutrition_score": "A", "quantity": 25},
            {"name": "Cod", "price": 11.99, "brand": "SeaFish", "category": "Fish & Seafood", "nutrition_score": "A", "quantity": 20},
            {"name": "Shrimp (500g)", "price": 12.99, "brand": "OceanPrawn", "category": "Fish & Seafood", "nutrition_score": "A", "quantity": 30},

            # Dairy (3)
            {"name": "Milk (1L)", "price": 2.99, "brand": "DairyBest", "category": "Dairy", "nutrition_score": "A", "quantity": 80},
            {"name": "Cheese (500g)", "price": 5.99, "brand": "CheeseHouse", "category": "Dairy", "nutrition_score": "B", "quantity": 40},
            {"name": "Yogurt (500g)", "price": 3.49, "brand": "YogurtPro", "category": "Dairy", "nutrition_score": "A", "quantity": 60},

            # Fats & Oils (3)
            {"name": "Olive Oil (500ml)", "price": 8.99, "brand": "OliveGold", "category": "Fats & Oils", "nutrition_score": "A", "quantity": 40},
            {"name": "Sunflower Oil (1L)", "price": 4.99, "brand": "SunOil", "category": "Fats & Oils", "nutrition_score": "B", "quantity": 50},
            {"name": "Vegetable Oil (1L)", "price": 3.99, "brand": "VegOil", "category": "Fats & Oils", "nutrition_score": "B", "quantity": 45},

            # Sugars & Confectionery (3)
            {"name": "Honey (500ml)", "price": 7.99, "brand": "PureHoney", "category": "Sugars & Confectionery", "nutrition_score": "B", "quantity": 35},
            {"name": "Sugar (1kg)", "price": 2.49, "brand": "SweetGrain", "category": "Sugars & Confectionery", "nutrition_score": "E", "quantity": 80},
            {"name": "Chocolate Bar", "price": 2.99, "brand": "ChocoBrand", "category": "Sugars & Confectionery", "nutrition_score": "D", "quantity": 100},

            # Beverages (3)
            {"name": "Orange Juice (1L)", "price": 3.99, "brand": "FreshJuice", "category": "Beverages", "nutrition_score": "B", "quantity": 50},
            {"name": "Coffee (500g)", "price": 7.99, "brand": "BeanBrew", "category": "Beverages", "nutrition_score": "A", "quantity": 30},
            {"name": "Tea (20 bags)", "price": 4.99, "brand": "TeaLeaf", "category": "Beverages", "nutrition_score": "A", "quantity": 40},

            # Ready-to-eat (3)
            {"name": "Pizza (Frozen)", "price": 8.99, "brand": "FrozenPizza", "category": "Ready-to-eat", "nutrition_score": "C", "quantity": 35},
            {"name": "Prepared Salad", "price": 6.99, "brand": "HealthySalad", "category": "Ready-to-eat", "nutrition_score": "A", "quantity": 25},
            {"name": "Sandwich", "price": 7.99, "brand": "QuickMeal", "category": "Ready-to-eat", "nutrition_score": "B", "quantity": 20},

            # Condiments/Sauces/Spices (3)
            {"name": "Tomato Sauce (500ml)", "price": 2.99, "brand": "SaucePerfect", "category": "Condiments/Sauces/Spices", "nutrition_score": "B", "quantity": 50},
            {"name": "Soy Sauce (250ml)", "price": 3.49, "brand": "AsianFlavor", "category": "Condiments/Sauces/Spices", "nutrition_score": "A", "quantity": 40},
            {"name": "Ketchup (500ml)", "price": 2.49, "brand": "TomatoKetchup", "category": "Condiments/Sauces/Spices", "nutrition_score": "D", "quantity": 60},
        ]

        for product_data in products_data:
            Product.objects.create(
                **product_data,
                barcode=str(uuid.uuid4())[:12]
            )

        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(products_data)} products across all categories"))

    def create_sample_invoices(self):
        """Create sample invoices for customers"""
        customers = Customer.objects.all()
        products = Product.objects.all()

        if not customers.exists() or not products.exists():
            self.stdout.write("⚠️  No customers or products found, skipping invoice creation...")
            return

        invoices_created = 0
        for customer in customers:
            # Create 2-3 invoices per customer
            num_invoices = 2 if invoices_created % 2 == 0 else 3
            
            for _ in range(num_invoices):
                # Pick 2-4 random products
                selected_products = products.order_by('?')[:3]
                total = Decimal('0.00')

                invoice = Invoice.objects.create(
                    customer=customer,
                    total=Decimal('0.00'),
                    status='completed'
                )

                # Add items to invoice
                for product in selected_products:
                    quantity = 1 if product.price > 10 else (2 if product.price > 5 else 3)
                    item_total = Decimal(str(product.price)) * quantity

                    InvoiceItem.objects.create(
                        invoice=invoice,
                        product=product,
                        quantity=quantity,
                        price=product.price
                    )

                    total += item_total

                # Update invoice total
                invoice.total = total
                invoice.save()

                invoices_created += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Created {invoices_created} sample invoices"))
