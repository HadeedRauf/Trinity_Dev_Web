import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getProducts } from '../services/api';
import '../styles/CustomerDashboard.css';

export default function CustomerDashboard() {
  const navigate = useNavigate();
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [showNutritionModal, setShowNutritionModal] = useState(false);

  const username = localStorage.getItem('username') || 'Customer';

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const response = await getProducts();
      setProducts(Array.isArray(response.data) ? response.data : []);
      setError('');
      filterProducts(response.data, '', 'All');
    } catch (err) {
      console.error('Load products error:', err);
      setError('Failed to load products');
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };

  const categorizeProduct = (product) => {
    const name = (product.name || '').toLowerCase();
    const category = (product.category || '').toLowerCase();
    const combined = `${name} ${category}`;

    const categories = {
      'Fruits and vegetables': ['apple', 'banana', 'orange', 'tomato', 'carrot', 'lettuce', 'broccoli', 'spinach', 'fruit', 'vegetable'],
      'Grains and cereals': ['bread', 'rice', 'pasta', 'cereal', 'oats', 'wheat', 'grain'],
      'Meat and poultry': ['chicken', 'beef', 'pork', 'turkey', 'meat', 'poultry'],
      'Fish and seafood': ['fish', 'salmon', 'tuna', 'shrimp', 'crab', 'seafood'],
      'Dairy and dairy alternatives': ['milk', 'cheese', 'yogurt', 'butter', 'dairy', 'cream'],
      'Fats and oils': ['oil', 'butter', 'ghee', 'fat', 'margarine'],
      'Sugars and confectionery': ['sugar', 'candy', 'chocolate', 'sweet', 'dessert'],
      'Beverages': ['juice', 'water', 'coffee', 'tea', 'drink', 'beverage'],
      'Ready-to-eat and convenience foods': ['ready', 'frozen', 'convenience', 'instant'],
      'Condiments, sauces, and spices': ['sauce', 'spice', 'condiment', 'seasoning', 'ketchup', 'mayo'],
    };

    for (const [cat, keywords] of Object.entries(categories)) {
      if (keywords.some(kw => combined.includes(kw))) {
        return cat;
      }
    }
    return 'Other';
  };

  const filterProducts = (productList, search, category) => {
    let result = productList.filter(p => {
      const matchesSearch = p.name.toLowerCase().includes(search.toLowerCase()) ||
        (p.brand && p.brand.toLowerCase().includes(search.toLowerCase())) ||
        (p.category && p.category.toLowerCase().includes(search.toLowerCase()));
      
      const productCategory = categorizeProduct(p);
      const matchesCategory = category === 'All' || productCategory === category;
      
      return matchesSearch && matchesCategory;
    });
    
    setFilteredProducts(result);
  };

  const handleSearch = (value) => {
    setSearchTerm(value);
    filterProducts(products, value, selectedCategory);
  };

  const handleCategoryFilter = (category) => {
    setSelectedCategory(category);
    filterProducts(products, searchTerm, category);
  };

  const openNutritionModal = (product) => {
    setSelectedProduct(product);
    setShowNutritionModal(true);
  };

  const closeNutritionModal = () => {
    setShowNutritionModal(false);
    setSelectedProduct(null);
  };

  const getNutritionScoreColor = (score) => {
    switch (score) {
      case 'A': return '#27ae60';
      case 'B': return '#f39c12';
      case 'C': return '#e67e22';
      case 'D': return '#e74c3c';
      case 'E': return '#c0392b';
      default: return '#95a5a6';
    }
  };

  const getNutritionScoreLabel = (score) => {
    switch (score) {
      case 'A': return 'Excellent';
      case 'B': return 'Good';
      case 'C': return 'Fair';
      case 'D': return 'Poor';
      case 'E': return 'Very Poor';
      default: return 'Not Rated';
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_role');
    localStorage.removeItem('username');
    navigate('/login');
  };

  const categories = ['All', 'Fruits and vegetables', 'Grains and cereals', 'Meat and poultry', 'Fish and seafood', 'Dairy and dairy alternatives', 'Fats and oils', 'Sugars and confectionery', 'Beverages', 'Ready-to-eat and convenience foods', 'Condiments, sauces, and spices'];

  return (
    <div className="customer-dashboard">
      <nav className="navbar">
        <div className="navbar-content">
          <h1 className="store-name">🏪 Trinity Store</h1>
          <div className="navbar-actions">
            <span className="welcome-user">Welcome, {username}!</span>
            <button className="btn-logout" onClick={handleLogout}>Logout</button>
          </div>
        </div>
      </nav>

      <div className="dashboard-container">
        {error && <div className="error-message">{error}</div>}

        {/* Search Bar */}
        <div className="search-container">
          <input
            type="text"
            placeholder="Search products by name, brand, or category..."
            value={searchTerm}
            onChange={(e) => handleSearch(e.target.value)}
            className="search-input"
          />
        </div>

        {/* Category Filter */}
        <div className="category-filter">
          <h3>Categories</h3>
          <div className="category-buttons">
            {categories.map(cat => (
              <button
                key={cat}
                className={`category-btn ${selectedCategory === cat ? 'active' : ''}`}
                onClick={() => handleCategoryFilter(cat)}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="loading">Loading products...</div>
        ) : filteredProducts.length === 0 ? (
          <div className="no-products">No products found</div>
        ) : (
          <>
            <div className="products-grid">
              {filteredProducts.map(product => (
                <div key={product.id} className="product-card">
                  <div className="product-info">
                    <h3>{product.name}</h3>
                    <p className="brand">{product.brand || 'Brand Unknown'}</p>
                    <p className="category-label">{categorizeProduct(product)}</p>
                    <div className="product-details">
                      <span className="price">${parseFloat(product.price || 0).toFixed(2)}</span>
                      <span className="quantity">{product.quantity || 0} pcs</span>
                    </div>
                    
                    <div className="nutrition-section">
                      <div 
                        className="nutrition-score-badge"
                        style={{ backgroundColor: getNutritionScoreColor(product.nutrition_score) }}
                      >
                        {product.nutrition_score || 'N'}
                      </div>
                      <button 
                        className="nutrition-btn"
                        onClick={() => openNutritionModal(product)}
                      >
                        Nutrition
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <div className="products-count">
              Showing {filteredProducts.length} product(s)
            </div>
          </>
        )}
      </div>

      {/* Nutrition Modal */}
      {showNutritionModal && selectedProduct && (
        <div className="modal-overlay" onClick={closeNutritionModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-btn" onClick={closeNutritionModal}>✕</button>
            
            <div className="modal-header">
              <h2>{selectedProduct.name}</h2>
              <p className="modal-brand">{selectedProduct.brand || 'Brand Unknown'}</p>
            </div>

            <div className="nutrition-details">
              <div className="nutrition-score-large">
                <div 
                  className="score-badge"
                  style={{ backgroundColor: getNutritionScoreColor(selectedProduct.nutrition_score) }}
                >
                  {selectedProduct.nutrition_score || 'N'}
                </div>
                <div className="score-info">
                  <h3>{getNutritionScoreLabel(selectedProduct.nutrition_score)}</h3>
                  <p className="score-label">Nutrition Score</p>
                  <div className="score-guide">
                    <span className="score-a">A = Excellent</span>
                    <span className="score-b">B = Good</span>
                    <span className="score-c">C = Fair</span>
                    <span className="score-d">D = Poor</span>
                    <span className="score-e">E = Very Poor</span>
                  </div>
                </div>
              </div>

              {selectedProduct.nutritional_info ? (
                <div className="nutritional-facts">
                  <h3>Nutritional Information (per 100g)</h3>
                  <div className="nutrition-grid">
                    {selectedProduct.nutritional_info.nutriments && (
                      <>
                        <div className="nutrition-item">
                          <span className="label">Energy</span>
                          <span className="value">{(selectedProduct.nutritional_info.nutriments.energy_kcal_100g || selectedProduct.nutritional_info.nutriments['energy-kcal_100g'] || 'N/A')} kcal</span>
                        </div>
                        <div className="nutrition-item">
                          <span className="label">Protein</span>
                          <span className="value">{(selectedProduct.nutritional_info.nutriments.proteins_100g || selectedProduct.nutritional_info.nutriments['proteins_100g'] || 'N/A')} g</span>
                        </div>
                        <div className="nutrition-item">
                          <span className="label">Fat</span>
                          <span className="value">{(selectedProduct.nutritional_info.nutriments.fat_100g || selectedProduct.nutritional_info.nutriments['fat_100g'] || 'N/A')} g</span>
                        </div>
                        <div className="nutrition-item">
                          <span className="label">Carbs</span>
                          <span className="value">{(selectedProduct.nutritional_info.nutriments.carbohydrates_100g || selectedProduct.nutritional_info.nutriments['carbohydrates_100g'] || 'N/A')} g</span>
                        </div>
                        <div className="nutrition-item">
                          <span className="label">Fiber</span>
                          <span className="value">{(selectedProduct.nutritional_info.nutriments.fiber_100g || selectedProduct.nutritional_info.nutriments['fiber_100g'] || 'N/A')} g</span>
                        </div>
                        <div className="nutrition-item">
                          <span className="label">Salt</span>
                          <span className="value">{(selectedProduct.nutritional_info.nutriments.salt_100g || selectedProduct.nutritional_info.nutriments['salt_100g'] || 'N/A')} g</span>
                        </div>
                      </>
                    )}
                  </div>
                </div>
              ) : (
                <div className="no-nutrition-data">No nutritional data available</div>
              )}

              <div className="product-details-modal">
                <h3>Product Details</h3>
                <div className="details-grid">
                  <div className="detail-item">
                    <span className="label">Price</span>
                    <span className="value">${parseFloat(selectedProduct.price || 0).toFixed(2)}</span>
                  </div>
                  <div className="detail-item">
                    <span className="label">Quantity</span>
                    <span className="value">{selectedProduct.quantity || 0} pcs</span>
                  </div>
                  <div className="detail-item">
                    <span className="label">Category</span>
                    <span className="value">{selectedProduct.category || 'Uncategorized'}</span>
                  </div>
                  <div className="detail-item">
                    <span className="label">Barcode</span>
                    <span className="value">{selectedProduct.barcode || 'N/A'}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="modal-footer">
              <button className="btn-close" onClick={closeNutritionModal}>Close</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
