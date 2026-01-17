from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=255, blank=True)
    picture = models.URLField(blank=True)
    category = models.CharField(max_length=255, blank=True)
    nutritional_info = models.JSONField(blank=True, null=True)
    nutrition_score = models.CharField(max_length=1, blank=True, choices=[
        ('A', 'A - Excellent'),
        ('B', 'B - Good'),
        ('C', 'C - Fair'),
        ('D', 'D - Poor'),
        ('E', 'E - Very Poor'),
    ])
    barcode = models.CharField(max_length=100, blank=True, unique=True)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.nutrition_score or 'N/A'})"

    class Meta:
        ordering = ['-created_at']

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices')
    total = models.DecimalField(max_digits=10, decimal_places=2)
