from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Product, Customer, Invoice, InvoiceItem, UserProfile
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate database with test users, products, and invoices'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Starting data population...\n')

        # ============= CREATE ADMIN USER =============
        self.stdout.write('👤 Creating admin user...')
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@trinity.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('✅ Admin user created: admin/admin'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Admin user already exists'))

        # Create admin profile
        admin_profile, _ = UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={'role': 'admin'}
        )
        self.stdout.write(self.style.SUCCESS(f'✅ Admin profile created with role: {admin_profile.role}\n'))

        # ============= CREATE TEST CUSTOMERS =============
        self.stdout.write('👥 Creating test customers...')
        customers_data = [
            {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe', 'password': 'john123'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith', 'password': 'jane123'},
            {'username': 'bob_wilson', 'email': 'bob@example.com', 'first_name': 'Bob', 'last_name': 'Wilson', 'password': 'bob123'},
            {'username': 'alice_jones', 'email': 'alice@example.com', 'first_name': 'Alice', 'last_name': 'Jones', 'password': 'alice123'},
        ]

        customers = []
        for cust_data in customers_data:
            user, created = User.objects.get_or_create(
                username=cust_data['username'],
                defaults={
                    'email': cust_data['email'],
                    'first_name': cust_data['first_name'],
                    'last_name': cust_data['last_name']
                }
            )
            if created:
                user.set_password(cust_data['password'])
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✅ Created user: {cust_data["username"]}/{cust_data["password"]}'))
            
            # Create customer profile
            customer_profile, _ = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'customer'}
            )
            
            # Create customer record
            customer, _ = Customer.objects.get_or_create(
                user=user,
                defaults={
                    'phone': f'555-{random.randint(1000, 9999)}',
                    'address': f'{random.randint(100, 999)} Main St'
                }
            )
            customers.append(customer)

        self.stdout.write(self.style.SUCCESS(f'\n✅ Created {len(customers)} test customers\n'))

        # ============= GET PRODUCTS =============
        self.stdout.write('📦 Checking products...')
        products = Product.objects.all()[:20]  # Use first 20 existing products
        
        if not products.exists():
            self.stdout.write(self.style.WARNING('⚠️ No products found in database!'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'✅ Found {products.count()} products\n'))

        # ============= CREATE INVOICES WITH ITEMS =============
        self.stdout.write('📄 Creating invoices with items...')
        invoices_created = 0

        for customer in customers:
            # Create 2-3 invoices per customer
            num_invoices = random.randint(2, 3)
            
            for invoice_num in range(num_invoices):
                # Create invoice
                days_ago = random.randint(1, 60)
                invoice_date = datetime.now() - timedelta(days=days_ago)
                
                invoice = Invoice.objects.create(
                    customer=customer,
                    total=0,  # Will calculate below
                    created_at=invoice_date,
                    updated_at=invoice_date,
                    status='completed'
                )

                # Add 3-6 items to invoice
                total = 0
                num_items = random.randint(3, 6)
                selected_products = random.sample(list(products), min(num_items, len(products)))

                for product in selected_products:
                    quantity = random.randint(1, 5)
                    price = float(product.price)
                    item_total = quantity * price

                    InvoiceItem.objects.create(
                        invoice=invoice,
                        product=product,
                        quantity=quantity,
                        price=price
                    )
                    total += item_total

                # Update invoice total
                invoice.total = total
                invoice.save()
                invoices_created += 1

        self.stdout.write(self.style.SUCCESS(f'✅ Created {invoices_created} invoices with items\n'))

        # ============= SUMMARY =============
        self.stdout.write('=' * 60)
        self.stdout.write(self.style.SUCCESS('✅ DATA POPULATION COMPLETE!\n'))
        
        self.stdout.write('📊 Summary:')
        self.stdout.write(f'  • Admin Users: 1 (admin/admin)')
        self.stdout.write(f'  • Customer Users: {len(customers)}')
        self.stdout.write(f'  • Products: {products.count()}')
        self.stdout.write(f'  • Invoices: {invoices_created}')
        
        self.stdout.write('\n🔐 Test Credentials:')
        self.stdout.write('  Admin:')
        self.stdout.write('    • Username: admin')
        self.stdout.write('    • Password: admin')
        
        self.stdout.write('\n  Customers:')
        for cust_data in customers_data:
            self.stdout.write(f'    • {cust_data["username"]} / {cust_data["password"]}')
        
        self.stdout.write('\n🌐 Access URLs:')
        self.stdout.write('  • Frontend: http://13.53.101.211:3000')
        self.stdout.write('  • Admin Dashboard: http://13.53.101.211:8000/admin/')
        self.stdout.write('  • API: http://13.53.101.211:8000/api/')
        
        self.stdout.write('\n✨ You can now login and test all functionality!')
        self.stdout.write('=' * 60)
