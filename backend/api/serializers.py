from rest_framework import serializers
from .models import Product, Customer, Invoice, InvoiceItem, UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add user role to token payload
        try:
            profile = UserProfile.objects.get(user=user)
            token['role'] = profile.role
        except UserProfile.DoesNotExist:
            token['role'] = 'customer'  # default
        
        token['username'] = user.username
        return token

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
    
    def get_role(self, obj):
        try:
            return obj.profile.role
        except UserProfile.DoesNotExist:
            return 'customer'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class InvoiceItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = InvoiceItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price']

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True, source='items')
    customer_name = serializers.CharField(source='customer.first_name', read_only=True)
    
    class Meta:
        model = Invoice
        fields = ['id', 'customer', 'customer_name', 'total', 'status', 'created_at', 'updated_at', 'items']
