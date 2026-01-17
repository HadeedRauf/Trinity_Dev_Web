from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import ProductViewSet, CustomerViewSet, InvoiceViewSet, CustomTokenObtainPairView, RegisterCustomerView
from django.views.decorators.csrf import csrf_exempt

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'invoices', InvoiceViewSet, basename='invoice')

urlpatterns = [
    path('token/', csrf_exempt(CustomTokenObtainPairView.as_view()), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', csrf_exempt(RegisterCustomerView.as_view()), name='register_customer'),
] + router.urls
