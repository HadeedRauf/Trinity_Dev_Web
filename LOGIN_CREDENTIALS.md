# Trinity Grocery - Login Credentials & Fixed Issues

## ✅ Fixed Issues

### Problem: 401 Unauthorized Error on Login
**Root Cause**: Default password in `Login.jsx` was `admin123` but the admin user was created with password `admin`.

**Solution**: 
1. Created admin superuser with credentials: `admin` / `admin`
2. Updated `frontend/src/pages/Login.jsx` to use correct default password
3. Restarted frontend container
4. Added demo credentials hint on login page

## 👤 Admin Account

### Credentials
```
Username: admin
Password: admin
Email: admin@admin.com
Type: Superuser (Full Access)
```

### How to Use
1. Open http://localhost:3000
2. The login form is pre-filled with credentials
3. Click "Login" button
4. You'll be redirected to the dashboard

## 🔐 Authentication Flow

```
1. User enters username & password
   ↓
2. Frontend sends POST to /api/token/
   ↓
3. Backend validates credentials
   ↓
4. Backend returns JWT tokens (access + refresh)
   ↓
5. Frontend stores tokens in localStorage
   ↓
6. Frontend includes token in Authorization header
   ↓
7. User logged in, redirected to /dashboard
```

## 🔑 JWT Tokens

### Access Token
- Used for API requests
- Validity: 1 hour (configurable)
- Included in `Authorization: Bearer <token>` header

### Refresh Token
- Used to get new access token when expired
- Validity: 24 hours (configurable)
- Stored in localStorage

## 📋 Test Credentials

If you need to create additional test users, use Django admin:

```bash
# Access Django admin
http://localhost:8000/admin/

# Login with: admin / admin
```

## 🛠 Troubleshooting

### Login Fails with 401 Error
- Clear browser cache and localStorage
- Check that backend is running: `docker ps`
- Verify admin user exists: `docker exec trinitydev-backend-1 python manage.py shell`
- Try credentials: `admin` / `admin`

### Token Expired / Invalid
- The frontend automatically redirects to login
- Just log in again with your credentials

### Forgot Password
Use Django CLI to reset:
```bash
docker exec -it trinitydev-backend-1 python manage.py changepassword admin
```

## 📝 Related Files

- Frontend Login Page: `frontend/src/pages/Login.jsx`
- Auth Context: `frontend/src/context/AuthContext.jsx`
- API Service: `frontend/src/services/api.js`
- Backend Settings: `backend/backend/settings.py`
- User Model: `backend/api/models.py`

## 🚀 Next Steps

1. ✅ Login with admin/admin
2. Explore the dashboard
3. Create products and customers
4. Generate invoices
5. Build additional features

---

**Last Updated**: January 17, 2026
**Status**: ✅ Login Working
