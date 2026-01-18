from django.core.management.base import BaseCommand
from api.models import Product, Customer, Invoice, InvoiceItem
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Create invoices for existing customers with current products'

    def handle(self, *args, **options):
        self.stdout.write("📄 Creating invoices...\n")
        
        # Delete existing invoices
        Invoice.objects.all().delete()
        self.stdout.write("✅ Deleted existing invoices\n")
        
        customers = Customer.objects.all()
        products = Product.objects.all()
        
        if not customers.exists() or not products.exists():
            self.stdout.write("❌ No customers or products found!")
            return
        
        invoices_created = 0
        
        for customer in customers:
            # Create 2-3 invoices per customer
            num_invoices = random.randint(2, 3)
            
            for i in range(num_invoices):
                # Pick 3-5 random products
                selected_products = list(products.order_by('?')[:random.randint(3, 5)])
                total = Decimal('0.00')
                
                invoice = Invoice.objects.create(
                    customer=customer,
                    total=Decimal('0.00'),
                    status='completed'
                )
                
                # Add items to invoice
                for product in selected_products:
                    quantity = random.randint(1, 3)
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
                
                self.stdout.write(f"✅ Invoice #{invoice.id} for {customer.first_name}: ${total}")
                invoices_created += 1
        
        self.stdout.write(self.style.SUCCESS(f"\n✅ Created {invoices_created} invoices!"))
