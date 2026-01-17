import React, { useState, useEffect } from 'react';
import { getProducts, getCustomers, getInvoices } from '../services/api';
import './Dashboard.css';

export default function Dashboard() {
  const [kpis, setKpis] = useState({
    totalRevenue: 0,
    totalProducts: 0,
    totalCustomers: 0,
    totalInvoices: 0,
    averageInvoiceAmount: 0,
    inventoryValue: 0,
    recentInvoices: [],
    topProducts: []
  });
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [showNutritionModal, setShowNutritionModal] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Product categories
  const categories = [
    'All',
    'Fruits and vegetables',
    'Grains and cereals',
    'Meat and poultry',
    'Fish and seafood',
    'Dairy and dairy alternatives',
    'Fats and oils',
    'Sugars and confectionery',
    'Beverages',
    'Ready-to-eat and convenience foods',
    'Condiments, sauces, and spices'
  ];

  // Categorize products based on keywords
  const categorizeProduct = (product) => {
    const name = (product.name + ' ' + product.category).toLowerCase();
    
    if (name.includes('fruit') || name.includes('vegetable') || name.includes('orange') || name.includes('tomato')) {
      return 'Fruits and vegetables';
    } else if (name.includes('bread') || name.includes('cereal') || name.includes('grain') || name.includes('sourdough') || name.includes('crispbread')) {
      return 'Grains and cereals';
    } else if (name.includes('meat') || name.includes('poultry') || name.includes('chicken') || name.includes('beef')) {
      return 'Meat and poultry';
    } else if (name.includes('fish') || name.includes('seafood') || name.includes('salmon')) {
      return 'Fish and seafood';
    } else if (name.includes('dairy') || name.includes('yogurt') || name.includes('cheese') || name.includes('milk') || name.includes('kefir') || name.includes('cream')) {
      return 'Dairy and dairy alternatives';
    } else if (name.includes('oil') || name.includes('fat') || name.includes('butter') || name.includes('margarine')) {
      return 'Fats and oils';
    } else if (name.includes('sugar') || name.includes('candy') || name.includes('chocolate') || name.includes('nutella') || name.includes('confection')) {
      return 'Sugars and confectionery';
    } else if (name.includes('beverage') || name.includes('juice') || name.includes('drink') || name.includes('water') || name.includes('cola') || name.includes('pulpy')) {
      return 'Beverages';
    } else if (name.includes('ready') || name.includes('convenience') || name.includes('snack') || name.includes('pringles')) {
      return 'Ready-to-eat and convenience foods';
    } else if (name.includes('sauce') || name.includes('condiment') || name.includes('spice') || name.includes('bouillon')) {
      return 'Condiments, sauces, and spices';
    }
    
    return 'Other';
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  // Filter products based on search and category
  useEffect(() => {
    let filtered = products;

    // Category filter
    if (selectedCategory !== 'All') {
      filtered = filtered.filter(p => categorizeProduct(p) === selectedCategory);
    }

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(p =>
        p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        p.brand.toLowerCase().includes(searchTerm.toLowerCase()) ||
        p.category.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    setFilteredProducts(filtered);
  }, [searchTerm, selectedCategory, products]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      const [productsRes, customersRes, invoicesRes] = await Promise.all([
        getProducts(),
        getCustomers(),
        getInvoices()
      ]);

      const productsData = Array.isArray(productsRes.data) ? productsRes.data : [];
      const customers = Array.isArray(customersRes.data) ? customersRes.data : [];
      const invoices = Array.isArray(invoicesRes.data) ? invoicesRes.data : [];

      setProducts(productsData);
      setFilteredProducts(productsData);

      // Calculate KPIs
      const totalRevenue = invoices.reduce((sum, inv) => sum + parseFloat(inv.total), 0);
      const averageInvoiceAmount = invoices.length > 0 ? totalRevenue / invoices.length : 0;
      const inventoryValue = productsData.reduce((sum, prod) => sum + (parseFloat(prod.price) * prod.quantity), 0);
      
      const recentInvoices = invoices
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        .slice(0, 5);

      const topProducts = productsData
        .map(p => ({
          ...p,
          inventoryValue: parseFloat(p.price) * p.quantity
        }))
        .sort((a, b) => b.inventoryValue - a.inventoryValue)
        .slice(0, 5);

      setKpis({
        totalRevenue,
        totalProducts: productsData.length,
        totalCustomers: customers.length,
        totalInvoices: invoices.length,
        averageInvoiceAmount,
        inventoryValue,
        recentInvoices,
        topProducts
      });

      setError('');
    } catch (err) {
      console.error('Dashboard error:', err);
      setError('Failed to load dashboard data: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount) => {
    return `$${parseFloat(amount).toFixed(2)}`;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getNutritionScoreColor = (score) => {
    switch(score) {
      case 'A': return '#27ae60';
      case 'B': return '#f39c12';
      case 'C': return '#e67e22';
      case 'D': return '#e74c3c';
      case 'E': return '#c0392b';
      default: return '#95a5a6';
    }
  };

  const getNutritionScoreLabel = (score) => {
    switch(score) {
      case 'A': return 'Excellent';
      case 'B': return 'Good';
      case 'C': return 'Fair';
      case 'D': return 'Poor';
      case 'E': return 'Very Poor';
      default: return 'Not Rated';
    }
  };

  const openNutritionModal = (product) => {
    setSelectedProduct(product);
    setShowNutritionModal(true);
  };

  const closeNutritionModal = () => {
    setShowNutritionModal(false);
    setSelectedProduct(null);
  };

  if (loading) return <div className="loading">Loading dashboard...</div>;

  return (
    <div className="dashboard">
      <h1>Dashboard - Key Performance Indicators</h1>

      {error && <div className="error">{error}</div>}

      <div className="kpi-cards">
        <div className="kpi-card revenue">
          <div className="kpi-icon">💰</div>
          <div className="kpi-content">
            <h3>Total Revenue</h3>
            <p className="kpi-value">{formatCurrency(kpis.totalRevenue)}</p>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-icon">📦</div>
          <div className="kpi-content">
            <h3>Total Products</h3>
            <p className="kpi-value">{kpis.totalProducts}</p>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-icon">👥</div>
          <div className="kpi-content">
            <h3>Total Customers</h3>
            <p className="kpi-value">{kpis.totalCustomers}</p>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-icon">🧾</div>
          <div className="kpi-content">
            <h3>Total Invoices</h3>
            <p className="kpi-value">{kpis.totalInvoices}</p>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-icon">📊</div>
          <div className="kpi-content">
            <h3>Average Invoice</h3>
            <p className="kpi-value">{formatCurrency(kpis.averageInvoiceAmount)}</p>
          </div>
        </div>

        <div className="kpi-card inventory">
          <div className="kpi-icon">🏪</div>
          <div className="kpi-content">
            <h3>Inventory Value</h3>
            <p className="kpi-value">{formatCurrency(kpis.inventoryValue)}</p>
          </div>
        </div>
      </div>

      {/* Products Section */}
      <div className="products-section">
        <h2>🛒 Product Catalog</h2>
        
        {/* Search Bar */}
        <div className="search-container">
          <input
            type="text"
            placeholder="🔍 Search products by name, brand, or category..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        {/* Category Filter */}
        <div className="category-filter">
          <h3>Categories:</h3>
          <div className="category-buttons">
            {categories.map(cat => (
              <button
                key={cat}
                className={`category-btn ${selectedCategory === cat ? 'active' : ''}`}
                onClick={() => setSelectedCategory(cat)}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Products Grid */}
        <div className="products-grid">
          {filteredProducts.length === 0 ? (
            <p className="no-products">No products found matching your criteria.</p>
          ) : (
            filteredProducts.map(product => (
              <div key={product.id} className="product-card">
                <div className="product-image">
                  {product.picture ? (
                    <img src={product.picture} alt={product.name} />
                  ) : (
                    <div className="no-image">No Image</div>
                  )}
                </div>
                <div className="product-info">
                  <h3>{product.name}</h3>
                  <p className="brand">{product.brand}</p>
                  <p className="category-label">{categorizeProduct(product)}</p>
                  
                  <div className="product-details">
                    <span className="price">{formatCurrency(product.price)}</span>
                    <span className="quantity">Qty: {product.quantity}</span>
                  </div>

                  {/* Nutrition Score Badge */}
                  <div className="nutrition-section">
                    <div
                      className="nutrition-score-badge"
                      style={{ backgroundColor: getNutritionScoreColor(product.nutrition_score) }}
                      title={getNutritionScoreLabel(product.nutrition_score)}
                    >
                      {product.nutrition_score || 'N/A'}
                    </div>
                    <button
                      className="nutrition-btn"
                      onClick={() => openNutritionModal(product)}
                    >
                      📊 Nutrition
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
        
        {filteredProducts.length > 0 && (
          <p className="products-count">Showing {filteredProducts.length} of {products.length} products</p>
        )}
      </div>

      {/* Recent Invoices & Top Products */}
      <div className="dashboard-sections">
        <div className="dashboard-section">
          <h2>Recent Invoices</h2>
          {kpis.recentInvoices.length === 0 ? (
            <p className="no-data">No invoices yet</p>
          ) : (
            <table className="dashboard-table">
              <thead>
                <tr>
                  <th>Invoice #</th>
                  <th>Total</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {kpis.recentInvoices.map(invoice => (
                  <tr key={invoice.id}>
                    <td>#{invoice.id}</td>
                    <td className="amount">{formatCurrency(invoice.total)}</td>
                    <td>{formatDate(invoice.created_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <div className="dashboard-section">
          <h2>Top Products by Inventory Value</h2>
          {kpis.topProducts.length === 0 ? (
            <p className="no-data">No products yet</p>
          ) : (
            <table className="dashboard-table">
              <thead>
                <tr>
                  <th>Product</th>
                  <th>Quantity</th>
                  <th>Value</th>
                </tr>
              </thead>
              <tbody>
                {kpis.topProducts.map(product => (
                  <tr key={product.id}>
                    <td>{product.name}</td>
                    <td>{product.quantity}</td>
                    <td className="amount">{formatCurrency(product.inventoryValue)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* Nutrition Modal */}
      {showNutritionModal && selectedProduct && (
        <div className="modal-overlay" onClick={closeNutritionModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-btn" onClick={closeNutritionModal}>✕</button>
            
            <div className="modal-header">
              <h2>{selectedProduct.name}</h2>
              <p className="modal-brand">{selectedProduct.brand}</p>
            </div>

            <div className="nutrition-details">
              {/* Nutrition Score */}
              <div className="nutrition-score-large">
                <div className="score-badge" style={{ backgroundColor: getNutritionScoreColor(selectedProduct.nutrition_score) }}>
                  {selectedProduct.nutrition_score || 'N/A'}
                </div>
                <div className="score-info">
                  <h3>Nutrition Score</h3>
                  <p className="score-label">{getNutritionScoreLabel(selectedProduct.nutrition_score)}</p>
                  <div className="score-guide">
                    <span className="score-a">A - Excellent</span>
                    <span className="score-b">B - Good</span>
                    <span className="score-c">C - Fair</span>
                    <span className="score-d">D - Poor</span>
                    <span className="score-e">E - Very Poor</span>
                  </div>
                </div>
              </div>

              {/* Nutritional Info */}
              <div className="nutritional-facts">
                <h3>Nutritional Information (per 100g)</h3>
                {selectedProduct.nutritional_info ? (
                  <div className="nutrition-grid">
                    <div className="nutrition-item">
                      <span className="label">Energy</span>
                      <span className="value">{selectedProduct.nutritional_info.energy_kcal ?? 'N/A'} kcal</span>
                    </div>
                    <div className="nutrition-item">
                      <span className="label">Protein</span>
                      <span className="value">{selectedProduct.nutritional_info.protein_g ?? 'N/A'} g</span>
                    </div>
                    <div className="nutrition-item">
                      <span className="label">Fat</span>
                      <span className="value">{selectedProduct.nutritional_info.fat_g ?? 'N/A'} g</span>
                    </div>
                    <div className="nutrition-item">
                      <span className="label">Carbohydrates</span>
                      <span className="value">{selectedProduct.nutritional_info.carbs_g ?? 'N/A'} g</span>
                    </div>
                    <div className="nutrition-item">
                      <span className="label">Fiber</span>
                      <span className="value">{selectedProduct.nutritional_info.fiber_g ?? 'N/A'} g</span>
                    </div>
                    <div className="nutrition-item">
                      <span className="label">Salt</span>
                      <span className="value">{selectedProduct.nutritional_info.salt_g ?? 'N/A'} g</span>
                    </div>
                  </div>
                ) : (
                  <p className="no-nutrition-data">No nutritional data available</p>
                )}
              </div>

              {/* Product Details */}
              <div className="product-details-modal">
                <h3>Product Details</h3>
                <div className="details-grid">
                  <div className="detail-item">
                    <span className="label">Price:</span>
                    <span className="value">{formatCurrency(selectedProduct.price)}</span>
                  </div>
                  <div className="detail-item">
                    <span className="label">Quantity in Stock:</span>
                    <span className="value">{selectedProduct.quantity} units</span>
                  </div>
                  <div className="detail-item">
                    <span className="label">Category:</span>
                    <span className="value">{categorizeProduct(selectedProduct)}</span>
                  </div>
                  <div className="detail-item">
                    <span className="label">Barcode:</span>
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
