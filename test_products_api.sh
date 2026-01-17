#!/bin/bash

echo "=========================================="
echo "  Trinity Grocery - Products API Test"
echo "=========================================="
echo ""

# Get auth token
echo "🔐 Getting authentication token..."
TOKEN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}')

TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"access":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo "❌ Failed to get token"
  exit 1
fi

echo "✅ Token obtained (${#TOKEN} chars)"
echo ""

# Get all products
echo "📦 Fetching all products..."
PRODUCTS=$(curl -s -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/products/)

COUNT=$(echo $PRODUCTS | grep -o '"id"' | wc -l)

echo "✅ Total products: $COUNT"
echo ""

# Show sample of products
echo "📋 Sample products:"
echo $PRODUCTS | python3 -m json.tool | head -50

echo ""
echo "=========================================="
echo "  API Test Complete!"
echo "=========================================="
