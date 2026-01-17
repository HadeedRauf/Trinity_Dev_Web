import React, { useState, useEffect } from 'react';
import { getProducts, createProduct, updateProduct, deleteProduct, searchOpenFoodFacts } from '../services/api';

export default function ProductManagement() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    price: '',
    brand: '',
    picture: '',
    category: '',
    quantity: '',
    nutritional_info: {}
  });
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedProducts, setSelectedProducts] = useState(new Set());
  const [deleting, setDeleting] = useState(false);
  const [sortConfig, setSortConfig] = useState({ key: 'name', direction: 'asc' });

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      setLoading(true);
      const response = await getProducts();
      setProducts(Array.isArray(response.data) ? response.data : []);
      setError('');
      setSelectedProducts(new Set());
    } catch (err) {
      console.error('Load products error:', err);
      setError('Failed to load products');
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingProduct) {
        await updateProduct(editingProduct.id, formData);
      } else {
        await createProduct(formData);
      }
      setShowModal(false);
      resetForm();
      loadProducts();
    } catch (err) {
      console.error('Submit error:', err);
      setError('Failed to save product');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Delete this product?')) {
      try {
        await deleteProduct(id);
        loadProducts();
      } catch (err) {
        console.error('Delete error:', err);
        setError('Failed to delete product');
      }
    }
  };

  const handleBulkDelete = async () => {
    if (selectedProducts.size === 0) {
      alert('Please select products to delete');
      return;
    }

    if (!window.confirm(`Delete ${selectedProducts.size} product(s)?`)) {
      return;
    }

    setDeleting(true);
    try {
      for (const productId of selectedProducts) {
        await deleteProduct(productId);
      }
      setSelectedProducts(new Set());
      loadProducts();
      alert('Products deleted successfully');
    } catch (err) {
      console.error('Bulk delete error:', err);
      setError('Failed to delete some products');
    } finally {
      setDeleting(false);
    }
  };

  const toggleSelectProduct = (id) => {
    const newSelected = new Set(selectedProducts);
    if (newSelected.has(id)) {
      newSelected.delete(id);
    } else {
      newSelected.add(id);
    }
    setSelectedProducts(newSelected);
  };

  const toggleSelectAll = () => {
    if (selectedProducts.size === filteredProducts.length) {
      setSelectedProducts(new Set());
    } else {
      setSelectedProducts(new Set(filteredProducts.map(p => p.id)));
    }
  };

  const handleEdit = (product) => {
    setEditingProduct(product);
    setFormData({
      name: product.name || '',
      price: product.price || '',
      brand: product.brand || '',
      picture: product.picture || '',
      category: product.category || '',
      quantity: product.quantity || '',
      nutritional_info: product.nutritional_info || {}
    });
    setShowModal(true);
  };

  const resetForm = () => {
    setFormData({
      name: '',
      price: '',
      brand: '',
      picture: '',
      category: '',
      quantity: '',
      nutritional_info: {}
    });
    setEditingProduct(null);
  };

  const handleOpenFoodFactsSearch = async (query) => {
    try {
      const results = await searchOpenFoodFacts(query);
      if (!Array.isArray(results) || results.length === 0) {
        alert('No results from OpenFoodFacts');
        return;
      }

      const ofProduct = results[0];
      const nutriments = ofProduct.nutriments || {};

      setFormData({
        ...formData,
        name: ofProduct.product_name || formData.name,
        brand: ofProduct.brands || formData.brand,
        picture: ofProduct.image_url || formData.picture || ofProduct.image_small_url || '',
        category: ofProduct.categories || formData.category,
        nutritional_info: { nutriments: nutriments, serving_size: ofProduct.serving_size }
      });
    } catch (err) {
      console.error('OpenFoodFacts error:', err);
      alert('Failed to fetch product data');
    }
  };

  const filteredProducts = products.filter(p =>
    p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (p.brand && p.brand.toLowerCase().includes(searchTerm.toLowerCase())) ||
    (p.category && p.category.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const sortedProducts = [...filteredProducts].sort((a, b) => {
    const aValue = a[sortConfig.key] || '';
    const bValue = b[sortConfig.key] || '';
    
    if (sortConfig.key === 'price' || sortConfig.key === 'quantity') {
      return sortConfig.direction === 'asc' 
        ? parseFloat(aValue) - parseFloat(bValue)
        : parseFloat(bValue) - parseFloat(aValue);
    }
    
    const comparison = String(aValue).localeCompare(String(bValue));
    return sortConfig.direction === 'asc' ? comparison : -comparison;
  });

  const handleSort = (key) => {
    setSortConfig({
      key,
      direction: sortConfig.key === key && sortConfig.direction === 'asc' ? 'desc' : 'asc'
    });
  };

  const SortIcon = ({ columnKey }) => {
    if (sortConfig.key !== columnKey) return ' ↕️';
    return sortConfig.direction === 'asc' ? ' ↑' : ' ↓';
  };

  return (
    <div className="product-management">
      <h1>Product Management</h1>

      {error && <div className="error-message">{error}</div>}

      <div className="section-header">
        <button className="btn-primary" onClick={() => { resetForm(); setShowModal(true); }}>
          ➕ Add Product
        </button>
      </div>

      {/* Search Bar */}
      <div className="search-box">
        <input
          type="text"
          placeholder="Search products by name, brand, or category..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
      </div>

      {/* Bulk Actions */}
      {selectedProducts.size > 0 && (
        <div className="bulk-actions">
          <span>{selectedProducts.size} product(s) selected</span>
          <button 
            className="btn-danger" 
            onClick={handleBulkDelete}
            disabled={deleting}
          >
            🗑️ {deleting ? 'Deleting...' : 'Delete Selected'}
          </button>
        </div>
      )}

      {loading ? (
        <div className="loading">Loading products...</div>
      ) : filteredProducts.length === 0 ? (
        <div className="no-products">No products found</div>
      ) : (
        <>
          <div className="select-all-container">
            <label>
              <input
                type="checkbox"
                checked={selectedProducts.size === filteredProducts.length && filteredProducts.length > 0}
                onChange={toggleSelectAll}
              />
              Select All ({filteredProducts.length})
            </label>
          </div>

          {/* Interactive Data Grid */}
          <div className="products-table-wrapper">
            <table className="products-table">
              <thead>
                <tr>
                  <th className="checkbox-column">
                    <input
                      type="checkbox"
                      checked={selectedProducts.size === filteredProducts.length && filteredProducts.length > 0}
                      onChange={toggleSelectAll}
                    />
                  </th>
                  <th onClick={() => handleSort('name')} className="sortable">
                    Product Name <SortIcon columnKey="name" />
                  </th>
                  <th onClick={() => handleSort('brand')} className="sortable">
                    Brand <SortIcon columnKey="brand" />
                  </th>
                  <th onClick={() => handleSort('category')} className="sortable">
                    Category <SortIcon columnKey="category" />
                  </th>
                  <th onClick={() => handleSort('price')} className="sortable">
                    Price <SortIcon columnKey="price" />
                  </th>
                  <th onClick={() => handleSort('quantity')} className="sortable">
                    Quantity <SortIcon columnKey="quantity" />
                  </th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {sortedProducts.map((product) => (
                  <tr 
                    key={product.id} 
                    className={selectedProducts.has(product.id) ? 'selected-row' : ''}
                  >
                    <td className="checkbox-column">
                      <input
                        type="checkbox"
                        checked={selectedProducts.has(product.id)}
                        onChange={() => toggleSelectProduct(product.id)}
                      />
                    </td>
                    <td className="product-name">
                      <strong>{product.name}</strong>
                    </td>
                    <td>{product.brand || '-'}</td>
                    <td>
                      <span className="category-badge">{product.category || 'Uncategorized'}</span>
                    </td>
                    <td className="price-cell">
                      ${parseFloat(product.price || 0).toFixed(2)}
                    </td>
                    <td className="quantity-cell">
                      {product.quantity || 0} pcs
                    </td>
                    <td className="actions-cell">
                      <button 
                        className="btn-action btn-edit" 
                        onClick={() => handleEdit(product)}
                        title="Edit product"
                      >
                        ✏️ Edit
                      </button>
                      <button 
                        className="btn-action btn-delete" 
                        onClick={() => handleDelete(product.id)}
                        title="Delete product"
                      >
                        🗑️ Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="products-count">
            Total: {filteredProducts.length} product(s)
          </div>
        </>
      )}

      {/* Modal */}
      {showModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>{editingProduct ? 'Edit Product' : 'Add Product'}</h2>
            <form onSubmit={handleSubmit}>
              <div style={{ marginBottom: '15px' }}>
                <label style={{ display: 'block', marginBottom: '5px' }}>Search OpenFoodFacts (barcode or name):</label>
                <div style={{ display: 'flex', gap: '10px' }}>
                  <input
                    type="text"
                    placeholder="e.g., 7622201513442 or Apple"
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') {
                        e.preventDefault();
                        handleOpenFoodFactsSearch(e.target.value);
                      }
                    }}
                    style={{ flex: 1, padding: '8px' }}
                  />
                  <button
                    type="button"
                    onClick={(e) => {
                      const input = e.target.previousElementSibling;
                      handleOpenFoodFactsSearch(input.value);
                    }}
                    className="btn-secondary"
                  >
                    Search
                  </button>
                </div>
              </div>

              <div style={{ marginBottom: '15px' }}>
                <label>Product Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                  className="form-input"
                />
              </div>

              <div style={{ marginBottom: '15px' }}>
                <label>Brand</label>
                <input
                  type="text"
                  value={formData.brand}
                  onChange={(e) => setFormData({ ...formData, brand: e.target.value })}
                  className="form-input"
                />
              </div>

              <div style={{ marginBottom: '15px' }}>
                <label>Price</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.price}
                  onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                  required
                  className="form-input"
                />
              </div>

              <div style={{ marginBottom: '15px' }}>
                <label>Quantity</label>
                <input
                  type="number"
                  value={formData.quantity}
                  onChange={(e) => setFormData({ ...formData, quantity: e.target.value })}
                  className="form-input"
                />
              </div>

              <div style={{ marginBottom: '15px' }}>
                <label>Category</label>
                <input
                  type="text"
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="form-input"
                />
              </div>

              <div style={{ marginBottom: '15px' }}>
                <label>Picture URL</label>
                <input
                  type="url"
                  value={formData.picture}
                  onChange={(e) => setFormData({ ...formData, picture: e.target.value })}
                  className="form-input"
                />
              </div>

              <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
                <button type="submit" className="btn-primary">
                  {editingProduct ? 'Update Product' : 'Add Product'}
                </button>
                <button
                  type="button"
                  onClick={() => { setShowModal(false); resetForm(); }}
                  className="btn-secondary"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
