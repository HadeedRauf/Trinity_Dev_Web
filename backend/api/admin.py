from django.contrib import admin
from .models import Product, Customer, Invoice

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'price', 'nutrition_score', 'quantity', 'created_at')
    search_fields = ('name', 'brand', 'category', 'barcode')
    list_filter = ('nutrition_score', 'category', 'created_at')
    readonly_fields = ('barcode', 'created_at', 'updated_at')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'city')
    search_fields = ('first_name', 'last_name', 'phone')
    list_filter = ('city', 'country')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total')
    search_fields = ('customer__first_name', 'customer__last_name')
    list_filter = ('total',)
