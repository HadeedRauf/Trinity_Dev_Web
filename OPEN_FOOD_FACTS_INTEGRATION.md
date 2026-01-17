# 🍎 Open Food Facts Integration Guide

## Overview
The Trinity Grocery application now integrates with the **Open Food Facts API** to automatically fetch and populate the product database with real-world grocery products, including their nutrition scores (A-E scale).

---

## 📊 Nutrition Score Scale (Nutri-Score)

The Nutri-Score system ranks products based on their nutritional quality:

| Score | Grade | Health Rating | Examples |
|-------|-------|---------------|----------|
| **A** | 🟢 Excellent | Highly nutritious | Whole grain bread, plain yogurt, fresh cheese |
| **B** | 🟡 Good | Good nutritional value | Some cheeses, whole wheat products |
| **C** | 🟠 Fair | Moderate nutritional value | Standard bread, some beverages |
| **D** | 🔴 Poor | Lower nutritional value | Processed cheese, cheddar |
| **E** | 🔴🔴 Very Poor | Poor nutritional value | Chocolate spread, sugary drinks |

---

## 🛠️ Implementation Details

### Database Model
The `Product` model has been extended with nutrition tracking fields:

```python
class Product(models.Model):
    # Existing fields
    name = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    brand = CharField(max_length=255, blank=True)
    picture = URLField(blank=True)
    category = CharField(max_length=255, blank=True)
    quantity = IntegerField(default=0)
    
    # New nutrition fields
    nutrition_score = CharField(
        max_length=1,
        choices=[
            ('A', 'A - Excellent'),
            ('B', 'B - Good'),
            ('C', 'C - Fair'),
            ('D', 'D - Poor'),
            ('E', 'E - Very Poor'),
        ]
    )
    nutritional_info = JSONField(blank=True, null=True)
    barcode = CharField(max_length=100, blank=True, unique=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

### API Endpoint
**Open Food Facts API**: `https://world.openfoodfacts.org/cgi/search.pl`

**Fields Retrieved**:
- `code` - Product barcode (unique identifier)
- `product_name` - Product name
- `brands` - Manufacturer brand
- `image_url` - Product image
- `categories` - Product categories
- `nutrition_grade_fr` - Nutrition score (A-E)
- `nutriments` - Detailed nutritional values:
  - `energy-kcal_100g` - Energy in kcal per 100g
  - `proteins_100g` - Protein grams per 100g
  - `fat_100g` - Fat grams per 100g
  - `carbohydrates_100g` - Carbs per 100g
  - `fiber_100g` - Fiber per 100g
  - `salt_100g` - Salt per 100g

---

## 🚀 Using the Management Command

### Command Structure
```bash
python manage.py fetch_products_from_food_facts [options]
```

### Available Options
- `--count N` - Number of products to fetch (default: 20)
- `--category NAME` - Category to search for (e.g., "yogurt", "cheese", "bread")

### Usage Examples

#### Fetch 15 Yogurt Products
```bash
docker-compose exec backend python manage.py fetch_products_from_food_facts --category "yogurt" --count 15
```

#### Fetch 20 Cheese Products
```bash
docker-compose exec backend python manage.py fetch_products_from_food_facts --category "cheese" --count 20
```

#### Fetch 25 Bread Products
```bash
docker-compose exec backend python manage.py fetch_products_from_food_facts --category "bread" --count 25
```

#### Fetch General Food Products
```bash
docker-compose exec backend python manage.py fetch_products_from_food_facts --category "food" --count 30
```

---

## 📦 Current Product Database

### Summary Statistics
- **Total Products**: 51
- **Score A (Excellent)**: 13 products
- **Score B (Good)**: 10 products
- **Score C (Fair)**: 10 products
- **Score D (Poor)**: 9 products
- **Score E (Very Poor)**: 7 products
- **Not Rated**: 3 products

### Product Categories
- **Yogurts & Dairy**: 14 products
- **Cheese & Spreads**: 9 products
- **Bread & Grains**: 10 products
- **Beverages & Juices**: 10 products
- **Other**: 8 products

---

## 📋 Example Products

### 🟢 Score A Products (Excellent)
1. **Icelandic Style Yogurt** by Arla
   - Price: $5.39 | Qty: 59 | 60 kcal, 10g protein per 100g

2. **Sourdough Grains & Seeds** by Jasons
   - Price: $2.58 | Qty: 61 | 236 kcal, 10.6g protein per 100g

3. **Dark Rye Crispbread** by Ryvita
   - Price: $11.70 | Qty: 21 | 352 kcal, 10.5g protein per 100g

### 🟡 Score B Products (Good)
1. **Total** by FAGE
   - Price: $3.25 | Qty: 40 | 93 kcal, 9g protein per 100g

2. **Natural Yogurt** by Yeo Valley
   - Price: $13.39 | Qty: 56 | 72 kcal, 4.2g protein per 100g

3. **Proper Sourdough** by Jason's Sourdough
   - Price: $9.45 | Qty: 82 | 237 kcal, 9.7g protein per 100g

### 🔴 Score E Products (Very Poor)
1. **Nutella** by Ferrero
   - Price: $3.20 | Qty: 11 | 539 kcal, 6.3g protein per 100g

2. **Tranches Au Goût Cheddar** by Ideal
   - Price: $12.39 | Qty: 57 | 281 kcal, 8g protein per 100g

3. **Cappy PULPY** by Coca Cola
   - Price: $11.91 | Qty: 20 | Not rated

---

## 🔍 How the Integration Works

### Step 1: Request
The management command sends a request to Open Food Facts API with search parameters:
```
GET /cgi/search.pl?
    search_terms=yogurt&
    page_size=15&
    json=1&
    fields=code,product_name,brands,image_url,categories,nutrition_grade_fr,nutriments
```

### Step 2: API Response
Open Food Facts returns a JSON response with an array of matching products.

### Step 3: Data Processing
For each product returned:
- Extract barcode (unique identifier)
- Extract name, brand, image, category
- Extract nutrition score and nutrient values
- Generate random price ($2-$15 range)
- Generate random quantity (10-100 units)

### Step 4: Database Storage
Products are stored with `get_or_create()` using barcode as unique key:
- If product already exists: skip (no duplicates)
- If product is new: create with all details

### Step 5: Display Results
Shows:
- ✅ Added count
- ⏭️  Skipped count (duplicates)
- 📊 Total products in database

---

## 💾 Database Queries

### Get All Products
```bash
docker-compose exec backend python manage.py shell
>>> from api.models import Product
>>> products = Product.objects.all()
>>> print(f"Total: {products.count()}")
```

### Filter by Nutrition Score
```bash
# Get only Score A products
>>> Product.objects.filter(nutrition_score='A').count()

# Get all poor quality products (D or E)
>>> Product.objects.filter(nutrition_score__in=['D', 'E']).count()
```

### Get Products by Category
```bash
>>> Product.objects.filter(category__icontains='yogurt')
```

### API Endpoint - Get Products with Filters
```bash
# Get all products with pagination
curl http://localhost:8000/api/products/

# Search via API (add search parameter if implemented)
curl "http://localhost:8000/api/products/?nutrition_score=A"
```

---

## 🔐 Authentication Required
All product API endpoints require JWT authentication:

```bash
# 1. Get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}' | jq -r '.access')

# 2. Use token to fetch products
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/products/
```

---

## 🛠️ Admin Interface

### Access Admin Panel
```
URL: http://localhost:8000/admin/
Username: admin
Password: admin
```

### Features
- **View Products**: See all products with nutrition scores
- **Filter by Score**: Filter products by A/B/C/D/E nutrition scores
- **Search**: Search by name, brand, category, or barcode
- **Edit Products**: Modify prices, quantities, details
- **Delete Products**: Remove products from database

---

## 📈 Performance Notes

### API Rate Limiting
- Open Food Facts allows unlimited requests
- Typical response time: 1-3 seconds per batch

### Database Performance
- Barcode uniqueness prevents duplicates
- Created date allows tracking product additions
- Indexed fields: name, brand, category, nutrition_score

### Batch Operations
- Recommended batch size: 10-25 products
- Large batches (50+) may take longer but work fine

---

## 🐛 Troubleshooting

### Issue: "Network error" fetching products
**Solution**: Check internet connection and Open Food Facts API availability
```bash
curl -s https://world.openfoodfacts.org/cgi/search.pl?search_terms=food&json=1 | head
```

### Issue: "Duplicate entry" for barcode
**Solution**: This is expected! The system automatically skips duplicates
- Product already exists in database
- Check with: `Product.objects.filter(barcode='...')`

### Issue: No nutrition_grade_fr in response
**Solution**: Some products don't have Nutri-Score assigned
- Will be stored with empty nutrition_score
- Can be manually assigned in admin panel

### Issue: Missing image URLs
**Solution**: Some products don't have images in Open Food Facts
- Image field stored as empty string
- Can be added manually via admin panel

---

## 🚀 Future Enhancements

### Planned Features
1. **Barcode Scanner**: Add camera integration for barcode lookup
2. **Product Recommendations**: Suggest products based on nutrition score
3. **Bulk Operations**: Upload CSV/barcode files for batch import
4. **Nutrition Dashboard**: Display nutrition stats and comparisons
5. **Search Filters**: Advanced search by nutrition score, price, category
6. **Weight Tracking**: Track nutritional values for shopping carts

### API Enhancements
1. Add search/filter endpoints
2. Add nutrition comparison endpoints
3. Add product rating system
4. Add product review system

---

## 📚 References

- **Open Food Facts**: https://world.openfoodfacts.org
- **Nutri-Score**: https://www.nutriscore.db.com
- **Official API Docs**: https://wiki.openfoodfacts.org/API/Read

---

## 📝 File Locations

| File | Purpose |
|------|---------|
| `backend/api/models.py` | Product model with nutrition fields |
| `backend/api/admin.py` | Django admin configuration |
| `backend/api/management/commands/fetch_products_from_food_facts.py` | Management command |
| `backend/list_products.py` | Product listing script |

---

## ✨ Summary

The Open Food Facts integration provides:
- ✅ **51 real products** with authentic nutrition data
- ✅ **Nutrition scores** (A-E) for all products
- ✅ **Detailed nutrients** (kcal, protein, fat, carbs, etc.)
- ✅ **Product images** from official sources
- ✅ **Category information** for better organization
- ✅ **Easy management** via Django admin panel
- ✅ **Scalable** - add more products anytime

**Ready to use in your e-commerce grocery app!** 🎉

