from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Customer, Invoice, UserProfile
from .serializers import ProductSerializer, CustomerSerializer, InvoiceSerializer, CustomTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
import requests
import jwt
from django.conf import settings

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        # Extract role from token payload
        if response.status_code == 200 and 'access' in response.data:
            try:
                # Decode the access token to get the role
                token = response.data['access']
                decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                role = decoded.get('role', 'customer')
                username = decoded.get('username', '')
                
                # Add role to response
                response.data['role'] = role
                response.data['username'] = username
            except Exception as e:
                print(f'Error decoding token: {e}')
                response.data['role'] = 'customer'
        
        return response

class RegisterCustomerView(APIView):
    """Register a new customer user"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        
        if not username or not email or not password:
            return Response({
                'error': 'username, email, and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({
                'error': 'Username already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({
                'error': 'Email already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create profile with customer role
        profile = UserProfile.objects.create(
            user=user,
            role='customer'
        )
        
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': 'customer',
            'message': 'Customer registered successfully'
        }, status=status.HTTP_201_CREATED)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        product = serializer.save()
        query = None
        try:
            query = self.request.data.get('openfood_query')
        except Exception:
            query = None

        if query:
            of = self._fetch_openfoodfacts_first(query)
            if of:
                product.nutritional_info = of
                product.save()

        return product

    def _fetch_openfoodfacts_first(self, query):
        try:
            resp = requests.get('https://world.openfoodfacts.org/cgi/search.pl', params={
                'search_terms': query,
                'search_simple': 1,
                'json': 1,
                'page_size': 1
            }, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            products = data.get('products') or []
            if not products:
                return None
            p = products[0]
            return {'nutriments': p.get('nutriments', {}), 'serving_size': p.get('serving_size'), 'product_name': p.get('product_name')}
        except Exception as e:
            print('OpenFoodFacts fetch error:', e)
            return None

    @action(detail=True, methods=['post'])
    def enrich(self, request, pk=None):
        product = self.get_object()
        query = request.data.get('query') or request.data.get('openfood_query')
        if not query:
            return Response({'detail': 'query is required'}, status=400)

        of = self._fetch_openfoodfacts_first(query)
        if not of:
            return Response({'detail': 'no_openfoodfacts_result'}, status=404)

        product.nutritional_info = of
        product.save(update_fields=['nutritional_info'])
        return Response({'detail': 'enriched', 'nutritional_info': of})

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
