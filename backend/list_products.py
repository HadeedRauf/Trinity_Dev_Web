import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Product

# Get all products with nutrition scores
products = Product.objects.all().order_by('nutrition_score', '-created_at')

print("\n" + "="*100)
print("                    PRODUCTS SUMMARY BY NUTRITION SCORE")
print("="*100 + "\n")

# Group by nutrition score
scores = {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], '': []}
for product in products:
    score = product.nutrition_score or ''
    if score in scores:
        scores[score].append(product)

score_names = {
    'A': 'Excellent',
    'B': 'Good',
    'C': 'Fair',
    'D': 'Poor',
    'E': 'Very Poor',
    '': 'Not Rated'
}

total = 0
for score in ['A', 'B', 'C', 'D', 'E', '']:
    products_in_score = scores[score]
    count = len(products_in_score)
    total += count
    
    if count > 0:
        name = score_names[score]
        print(f"\n📊 Score {score} - {name} ({count} products)")
        print("-" * 100)
        for idx, p in enumerate(products_in_score, 1):
            nutrition = ""
            if p.nutritional_info:
                kcal = p.nutritional_info.get('energy_kcal')
                protein = p.nutritional_info.get('protein_g')
                if kcal and protein:
                    nutrition = f" | {kcal} kcal, {protein}g protein"
            print(f"  {idx}. {p.name}")
            print(f"     Brand: {p.brand:30} | Category: {p.category:25} | Price: ${p.price:6}{nutrition}")

print("\n" + "="*100)
print(f"✨ TOTAL PRODUCTS IN DATABASE: {total}")
print("="*100 + "\n")
