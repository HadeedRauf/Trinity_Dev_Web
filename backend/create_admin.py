import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

# Create admin user
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
    print("✅ Admin user created: username=admin, password=admin")
else:
    print("✅ Admin user already exists")

# List all users
print("\nExisting users:")
for user in User.objects.all():
    print(f"  - {user.username} (staff={user.is_staff}, superuser={user.is_superuser})")
