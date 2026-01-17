import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login as apiLogin, register } from '../services/api';
import '../styles/Login.css';

export default function Login() {
  const navigate = useNavigate();
  const [mode, setMode] = useState('login'); // 'login' or 'register'
  const [loginData, setLoginData] = useState({ username: '', password: '' });
  const [registerData, setRegisterData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    first_name: '',
    last_name: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await apiLogin(loginData.username, loginData.password);
      
      // Store token and user data
      localStorage.setItem('access_token', response.access);
      localStorage.setItem('refresh_token', response.refresh);
      localStorage.setItem('user_role', response.role || 'customer');
      localStorage.setItem('username', loginData.username);

      // Redirect based on role
      if (response.role === 'admin') {
        navigate('/dashboard');
      } else {
        navigate('/customer');
      }
    } catch (err) {
      setError('Invalid username or password');
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (registerData.password !== registerData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);

    try {
      const response = await register({
        username: registerData.username,
        email: registerData.email,
        password: registerData.password,
        first_name: registerData.first_name,
        last_name: registerData.last_name
      });

      setError('');
      alert('Registration successful! Please log in.');
      setMode('login');
      setRegisterData({
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        first_name: '',
        last_name: ''
      });
      setLoginData({ username: registerData.username, password: registerData.password });
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed');
      console.error('Register error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <div className="login-header">
          <h1>Trinity Store</h1>
          <p>Grocery Management System</p>
        </div>

        {error && <div className="error-message">{error}</div>}

        {mode === 'login' ? (
          <form onSubmit={handleLoginSubmit} className="login-form">
            <h2>Welcome Back</h2>
            
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input
                type="text"
                id="username"
                value={loginData.username}
                onChange={(e) => setLoginData({ ...loginData, username: e.target.value })}
                placeholder="Enter your username"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                value={loginData.password}
                onChange={(e) => setLoginData({ ...loginData, password: e.target.value })}
                placeholder="Enter your password"
                required
              />
            </div>

            <button type="submit" className="btn-login" disabled={loading}>
              {loading ? 'Logging in...' : 'Login'}
            </button>

            <div className="login-footer">
              <p>
                Don't have an account?{' '}
                <button
                  type="button"
                  className="link-button"
                  onClick={() => setMode('register')}
                >
                  Register here
                </button>
              </p>
            </div>

            <div className="demo-creds">
              <p className="demo-title">Demo Credentials:</p>
              <p><strong>Admin:</strong> admin / admin</p>
              <p><strong>Customer:</strong> customer / customer123</p>
            </div>
          </form>
        ) : (
          <form onSubmit={handleRegisterSubmit} className="login-form">
            <h2>Create Customer Account</h2>

            <div className="form-group">
              <label htmlFor="first_name">First Name</label>
              <input
                type="text"
                id="first_name"
                value={registerData.first_name}
                onChange={(e) => setRegisterData({ ...registerData, first_name: e.target.value })}
                placeholder="First name"
              />
            </div>

            <div className="form-group">
              <label htmlFor="last_name">Last Name</label>
              <input
                type="text"
                id="last_name"
                value={registerData.last_name}
                onChange={(e) => setRegisterData({ ...registerData, last_name: e.target.value })}
                placeholder="Last name"
              />
            </div>

            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                value={registerData.email}
                onChange={(e) => setRegisterData({ ...registerData, email: e.target.value })}
                placeholder="your@email.com"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="reg_username">Username</label>
              <input
                type="text"
                id="reg_username"
                value={registerData.username}
                onChange={(e) => setRegisterData({ ...registerData, username: e.target.value })}
                placeholder="Choose a username"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="reg_password">Password</label>
              <input
                type="password"
                id="reg_password"
                value={registerData.password}
                onChange={(e) => setRegisterData({ ...registerData, password: e.target.value })}
                placeholder="Create a password"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="confirm_password">Confirm Password</label>
              <input
                type="password"
                id="confirm_password"
                value={registerData.confirmPassword}
                onChange={(e) => setRegisterData({ ...registerData, confirmPassword: e.target.value })}
                placeholder="Confirm password"
                required
              />
            </div>

            <button type="submit" className="btn-login" disabled={loading}>
              {loading ? 'Registering...' : 'Register'}
            </button>

            <div className="login-footer">
              <p>
                Already have an account?{' '}
                <button
                  type="button"
                  className="link-button"
                  onClick={() => setMode('login')}
                >
                  Login here
                </button>
              </p>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
