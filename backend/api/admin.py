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


from django.contrib.auth.models import User
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'user__email')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')

# Inline profile in User admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    fields = ('role', 'created_at')
    readonly_fields = ('created_at',)

# Extend User admin
original_user_admin = admin.site._registry[User]

class ExtendedUserAdmin(original_user_admin.__class__):
    inlines = list(original_user_admin.inlines) + [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)
