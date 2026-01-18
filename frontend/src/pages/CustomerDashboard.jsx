import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getProducts, getInvoices } from '../services/api';
import '../styles/CustomerDashboard.css';
import html2pdf from 'html2pdf.js';

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
  const [activeTab, setActiveTab] = useState('shop'); // 'shop', 'cart', 'invoices'
  const [cart, setCart] = useState([]);
  const [invoices, setInvoices] = useState([]);
  const [selectedInvoice, setSelectedInvoice] = useState(null);
  const [showInvoiceModal, setShowInvoiceModal] = useState(false);

  const username = localStorage.getItem('username') || 'Customer';

  useEffect(() => {
    loadDashboardData();
    loadInvoices();
    // Load cart from localStorage
    const savedCart = localStorage.getItem('customer_cart');
    if (savedCart) {
      setCart(JSON.parse(savedCart));
    }
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

  const loadInvoices = async () => {
    try {
      const response = await getInvoices();
      setInvoices(Array.isArray(response.data) ? response.data : []);
    } catch (err) {
      console.error('Load invoices error:', err);
    }
  };

  const addToCart = (product) => {
    const existingItem = cart.find(item => item.id === product.id);
    
    if (existingItem) {
      const updatedCart = cart.map(item =>
        item.id === product.id
          ? { ...item, quantity: item.quantity + 1 }
          : item
      );
      setCart(updatedCart);
      localStorage.setItem('customer_cart', JSON.stringify(updatedCart));
    } else {
      const newCart = [...cart, { ...product, quantity: 1 }];
      setCart(newCart);
      localStorage.setItem('customer_cart', JSON.stringify(newCart));
    }
    alert(`✅ ${product.name} added to cart!`);
  };

  const removeFromCart = (productId) => {
    const updatedCart = cart.filter(item => item.id !== productId);
    setCart(updatedCart);
    localStorage.setItem('customer_cart', JSON.stringify(updatedCart));
  };

  const updateCartQuantity = (productId, newQuantity) => {
    if (newQuantity <= 0) {
      removeFromCart(productId);
      return;
    }
    const updatedCart = cart.map(item =>
      item.id === productId ? { ...item, quantity: newQuantity } : item
    );
    setCart(updatedCart);
    localStorage.setItem('customer_cart', JSON.stringify(updatedCart));
  };

  const getCartTotal = () => {
    return cart.reduce((total, item) => total + (parseFloat(item.price) * item.quantity), 0);
  };

  const checkoutCart = () => {
    if (cart.length === 0) {
      alert('Your cart is empty!');
      return;
    }
    
    // Create a new invoice
    const newInvoice = {
      id: Date.now(),
      items: cart,
      total: getCartTotal(),
      created_at: new Date().toLocaleString(),
      status: 'Completed'
    };
    
    setInvoices([newInvoice, ...invoices]);
    setCart([]);
    localStorage.removeItem('customer_cart');
    setActiveTab('invoices');
    alert('✅ Purchase successful! Your invoice has been created.');
  };

  const downloadInvoicePDF = (invoice) => {
    const invoiceHTML = `
      <div style="font-family: Arial, sans-serif; padding: 20px;">
        <h1 style="text-align: center; color: #333;">Trinity Store Invoice</h1>
        <hr style="border: 1px solid #ddd;">
        
        <div style="margin: 20px 0;">
          <p><strong>Invoice ID:</strong> #${invoice.id}</p>
          <p><strong>Customer:</strong> ${username}</p>
          <p><strong>Date:</strong> ${invoice.created_at}</p>
          <p><strong>Status:</strong> ${invoice.status}</p>
        </div>
        
        <hr style="border: 1px solid #ddd;">
        
        <h3>Items Purchased:</h3>
        <table style="width: 100%; border-collapse: collapse;">
          <thead>
            <tr style="background-color: #f5f5f5;">
              <th style="border: 1px solid #ddd; padding: 10px; text-align: left;">Product</th>
              <th style="border: 1px solid #ddd; padding: 10px; text-align: center;">Quantity</th>
              <th style="border: 1px solid #ddd; padding: 10px; text-align: right;">Price</th>
              <th style="border: 1px solid #ddd; padding: 10px; text-align: right;">Total</th>
            </tr>
          </thead>
          <tbody>
            ${invoice.items.map(item => `
              <tr>
                <td style="border: 1px solid #ddd; padding: 10px;">${item.name} (${item.brand})</td>
                <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">${item.quantity}</td>
                <td style="border: 1px solid #ddd; padding: 10px; text-align: right;">$${parseFloat(item.price).toFixed(2)}</td>
                <td style="border: 1px solid #ddd; padding: 10px; text-align: right;">$${(parseFloat(item.price) * item.quantity).toFixed(2)}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
        
        <hr style="border: 1px solid #ddd; margin-top: 20px;">
        
        <div style="text-align: right; margin-top: 20px;">
          <h3>Total: $${invoice.total.toFixed(2)}</h3>
        </div>
        
        <hr style="border: 1px solid #ddd;">
        
        <p style="text-align: center; color: #666; margin-top: 30px;">
          Thank you for shopping at Trinity Store!<br/>
          <small>This is an automated invoice. No signature required.</small>
        </p>
      </div>
    `;

    const element = document.createElement('div');
    element.innerHTML = invoiceHTML;
    
    const opt = {
      margin: 10,
      filename: `invoice-${invoice.id}.pdf`,
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: { scale: 2 },
      jsPDF: { orientation: 'portrait', unit: 'mm', format: 'a4' }
    };
    
    html2pdf().set(opt).from(element).save();
  };

  const openInvoiceModal = (invoice) => {
    setSelectedInvoice(invoice);
    setShowInvoiceModal(true);
  };

  const closeInvoiceModal = () => {
    setShowInvoiceModal(false);
    setSelectedInvoice(null);
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
    localStorage.removeItem('customer_cart');
    navigate('/login');
  };

  const categories = ['All', 'Fruits and vegetables', 'Grains and cereals', 'Meat and poultry', 'Fish and seafood', 'Dairy and dairy alternatives', 'Fats and oils', 'Sugars and confectionery', 'Beverages', 'Ready-to-eat and convenience foods', 'Condiments, sauces, and spices'];

  return (
    <div className="customer-dashboard">
      <nav className="navbar">
        <div className="navbar-content">
          <h1 className="store-name">🏪 Trinity Store</h1>
          <div className="tab-navigation">
            <button 
              className={`tab-btn ${activeTab === 'shop' ? 'active' : ''}`}
              onClick={() => setActiveTab('shop')}
            >
              🛍️ Shop
            </button>
            <button 
              className={`tab-btn ${activeTab === 'cart' ? 'active' : ''}`}
              onClick={() => setActiveTab('cart')}
            >
              🛒 Cart ({cart.length})
            </button>
            <button 
              className={`tab-btn ${activeTab === 'invoices' ? 'active' : ''}`}
              onClick={() => setActiveTab('invoices')}
            >
              🧾 My Invoices ({invoices.length})
            </button>
          </div>
          <div className="navbar-actions">
            <span className="welcome-user">Welcome, {username}!</span>
            <button className="btn-logout" onClick={handleLogout}>Logout</button>
          </div>
        </div>
      </nav>

      <div className="dashboard-container">
        {error && <div className="error-message">{error}</div>}

        {/* SHOP TAB */}
        {activeTab === 'shop' && (
          <>
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
                      <div className="product-image">
                        {product.picture ? (
                          <img src={product.picture} alt={product.name} />
                        ) : (
                          <div className="no-image">📦 No Image</div>
                        )}
                      </div>
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
                            📊 Nutrition
                          </button>
                        </div>

                        <button 
                          className="btn-add-cart"
                          onClick={() => addToCart(product)}
                        >
                          ➕ Add to Cart
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="products-count">
                  Showing {filteredProducts.length} product(s)
                </div>
              </>
            )}
          </>
        )}

        {/* CART TAB */}
        {activeTab === 'cart' && (
          <div className="cart-container">
            <h2>🛒 Shopping Cart</h2>
            {cart.length === 0 ? (
              <div className="empty-cart">
                <p>Your cart is empty!</p>
                <button className="btn-continue-shopping" onClick={() => setActiveTab('shop')}>
                  Continue Shopping
                </button>
              </div>
            ) : (
              <>
                <table className="cart-table">
                  <thead>
                    <tr>
                      <th>Product</th>
                      <th>Price</th>
                      <th>Quantity</th>
                      <th>Total</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {cart.map(item => (
                      <tr key={item.id}>
                        <td>{item.name} ({item.brand})</td>
                        <td>${parseFloat(item.price).toFixed(2)}</td>
                        <td>
                          <input 
                            type="number" 
                            min="1" 
                            value={item.quantity}
                            onChange={(e) => updateCartQuantity(item.id, parseInt(e.target.value))}
                            className="quantity-input"
                          />
                        </td>
                        <td>${(parseFloat(item.price) * item.quantity).toFixed(2)}</td>
                        <td>
                          <button 
                            className="btn-remove"
                            onClick={() => removeFromCart(item.id)}
                          >
                            ❌ Remove
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>

                <div className="cart-summary">
                  <h3>Cart Summary</h3>
                  <div className="summary-row">
                    <span>Subtotal:</span>
                    <span>${getCartTotal().toFixed(2)}</span>
                  </div>
                  <div className="summary-row">
                    <span>Tax (10%):</span>
                    <span>${(getCartTotal() * 0.10).toFixed(2)}</span>
                  </div>
                  <div className="summary-row total">
                    <span>Total:</span>
                    <span>${(getCartTotal() * 1.10).toFixed(2)}</span>
                  </div>

                  <div className="cart-actions">
                    <button className="btn-continue-shopping" onClick={() => setActiveTab('shop')}>
                      Continue Shopping
                    </button>
                    <button className="btn-checkout" onClick={checkoutCart}>
                      ✅ Checkout
                    </button>
                  </div>
                </div>
              </>
            )}
          </div>
        )}

        {/* INVOICES TAB */}
        {activeTab === 'invoices' && (
          <div className="invoices-container">
            <h2>🧾 My Invoices</h2>
            {invoices.length === 0 ? (
              <div className="no-invoices">
                <p>You haven't made any purchases yet!</p>
                <button className="btn-shop-now" onClick={() => setActiveTab('shop')}>
                  Start Shopping
                </button>
              </div>
            ) : (
              <table className="invoices-table">
                <thead>
                  <tr>
                    <th>Invoice ID</th>
                    <th>Date</th>
                    <th>Items</th>
                    <th>Total</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {invoices.map(invoice => (
                    <tr key={invoice.id}>
                      <td>#{invoice.id}</td>
                      <td>{invoice.created_at}</td>
                      <td>{invoice.items.length} items</td>
                      <td>${invoice.total.toFixed(2)}</td>
                      <td><span className="status-badge completed">{invoice.status}</span></td>
                      <td>
                        <button 
                          className="btn-view"
                          onClick={() => openInvoiceModal(invoice)}
                        >
                          👁️ View
                        </button>
                        <button 
                          className="btn-download"
                          onClick={() => downloadInvoicePDF(invoice)}
                        >
                          📥 PDF
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
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

      {/* Invoice Modal */}
      {showInvoiceModal && selectedInvoice && (
        <div className="modal-overlay" onClick={closeInvoiceModal}>
          <div className="modal-content large" onClick={(e) => e.stopPropagation()}>
            <button className="close-btn" onClick={closeInvoiceModal}>✕</button>
            
            <div className="invoice-modal">
              <h2>Invoice #${selectedInvoice.id}</h2>
              <div className="invoice-details">
                <p><strong>Customer:</strong> {username}</p>
                <p><strong>Date:</strong> {selectedInvoice.created_at}</p>
                <p><strong>Status:</strong> {selectedInvoice.status}</p>
              </div>

              <table className="invoice-items-table">
                <thead>
                  <tr>
                    <th>Product</th>
                    <th>Quantity</th>
                    <th>Price</th>
                    <th>Total</th>
                  </tr>
                </thead>
                <tbody>
                  {selectedInvoice.items.map(item => (
                    <tr key={item.id}>
                      <td>{item.name} ({item.brand})</td>
                      <td>{item.quantity}</td>
                      <td>${parseFloat(item.price).toFixed(2)}</td>
                      <td>${(parseFloat(item.price) * item.quantity).toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <div className="invoice-total">
                <h3>Total: ${selectedInvoice.total.toFixed(2)}</h3>
              </div>

              <div className="invoice-actions">
                <button 
                  className="btn-download"
                  onClick={() => {
                    downloadInvoicePDF(selectedInvoice);
                    closeInvoiceModal();
                  }}
                >
                  📥 Download PDF
                </button>
                <button className="btn-close" onClick={closeInvoiceModal}>
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
