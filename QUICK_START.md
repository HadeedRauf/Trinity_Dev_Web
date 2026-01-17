# Trinity Grocery - Quick Start Guide

## 🚀 System Ready!

Everything is configured and running. Here's what you need to know:

### �� Project Location
```
/home/hadeed/Pictures/TRINITY DEV
```

### 🌐 Access URLs
| Component | URL | Status |
|-----------|-----|--------|
| **Frontend** | http://localhost:3000 | ✅ Running |
| **Backend API** | http://localhost:8000/api/ | ✅ Running |
| **Django Admin** | http://localhost:8000/admin/ | ✅ Running |

## 🔐 Login Credentials

```
Username: admin
Password: admin
```

### Login Steps
1. Go to http://localhost:3000
2. Form is pre-filled with credentials
3. Click "Login"
4. You'll see the dashboard

## 🛠 Available Commands

### View Logs
```bash
cd "/home/hadeed/Pictures/TRINITY DEV"

# All services
docker-compose logs -f

# Backend only
docker logs trinitydev-backend-1 -f

# Frontend only
docker logs trinitydev-frontend-1 -f
```

### Stop Services
```bash
cd "/home/hadeed/Pictures/TRINITY DEV"
docker-compose down
```

### Restart Services
```bash
cd "/home/hadeed/Pictures/TRINITY DEV"
docker-compose restart
```

### Full Rebuild
```bash
cd "/home/hadeed/Pictures/TRINITY DEV"
docker-compose down
docker-compose up --build --detach
```

## 🗄️ Database Management

### Access Database (PostgreSQL)
```bash
docker exec -it trinitydev-db-1 psql -U postgres -d time_manager
```

### Backup Database
```bash
docker exec trinitydev-db-1 pg_dump -U postgres time_manager > backup.sql
```

### Restore Database
```bash
docker exec -i trinitydev-db-1 psql -U postgres time_manager < backup.sql
```

## 👨‍💼 Django Admin Panel

Access at: http://localhost:8000/admin/
- Username: `admin`
- Password: `admin`

**You can**:
- Create/edit users
- Manage products
- Manage customers
- View invoices
- Configure application settings

## 📊 API Endpoints

### Authentication
```
POST /api/token/           - Get JWT tokens (username + password)
POST /api/token/refresh/   - Refresh expired token
```

### Resources
```
GET/POST   /api/products/       - List & create products
GET/PUT/DELETE /api/products/{id}/  - Manage single product

GET/POST   /api/customers/      - List & create customers
GET/PUT/DELETE /api/customers/{id}/ - Manage single customer

GET/POST   /api/invoices/       - List & create invoices
GET/PUT/DELETE /api/invoices/{id}/  - Manage single invoice
```

### Example API Call (with authentication)
```bash
# Get token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'

# Use token to fetch products
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/products/
```

## 🐛 Troubleshooting

### 1. Cannot Login (401 Error)
- Clear browser cache
- Verify credentials: `admin` / `admin`
- Check backend is running: `docker ps`
- Restart frontend: `docker-compose restart frontend`

### 2. API Returns 500 Error
- Check backend logs: `docker logs trinitydev-backend-1 -f`
- Ensure database is running: `docker ps`
- Verify migrations: Check log output for "Applied" messages

### 3. Cannot Access Database
- Password: `postgres`
- Database name: `time_manager`
- Make sure `trinitydev-db-1` container is running

### 4. Frontend Not Updating Changes
- Clear cache: Press Ctrl+Shift+Delete (Chrome/Firefox)
- Restart container: `docker-compose restart frontend`
- Check logs: `docker logs trinitydev-frontend-1 -f`

## 📚 Project Structure

```
/home/hadeed/Pictures/TRINITY DEV/
├── backend/
│   ├── api/                    # API models, views, serializers
│   ├── backend/                # Django settings
│   ├── manage.py               # Django CLI
│   ├── requirements.txt         # Python dependencies
│   └── Dockerfile              # Backend container
│
├── frontend/
│   ├── src/
│   │   ├── pages/             # React pages (Login, Dashboard, etc)
│   │   ├── components/        # Reusable components
│   │   ├── context/           # React context (Auth, etc)
│   │   ├── services/          # API calls
│   │   └── App.jsx            # Main app component
│   ├── public/                # Static assets
│   ├── package.json           # Node dependencies
│   └── Dockerfile             # Frontend container
│
├── docker-compose.yml          # Docker setup
├── README.md                   # Project docs
├── PROJECT_SETUP.md            # Detailed setup guide
├── LOGIN_CREDENTIALS.md        # Authentication info
└── QUICK_START.md              # This file
```

## 🎯 What You Can Do

✅ **Already Implemented**:
- User authentication with JWT tokens
- Product management (CRUD)
- Customer management (CRUD)
- Invoice/order management (CRUD)
- PostgreSQL database with persistent storage
- Django admin panel
- RESTful API

🔲 **Coming Soon** (From project README):
- Open Food Facts integration
- KPI reports
- Unit tests
- CI/CD pipeline
- Advanced documentation

## 💡 Tips & Best Practices

1. **Always use the admin panel** for testing data operations
2. **Keep tokens secure** - Never commit credentials to git
3. **Use Docker logs** to debug issues
4. **Backup database** before making major changes
5. **Test API** with curl/Postman before building features

## 🔄 Development Workflow

```
1. Make code changes
2. Frontend changes = Auto reload (Vite)
3. Backend changes = Restart container (docker-compose restart backend)
4. Database changes = Create migration, then migrate
5. Test with login: admin/admin
```

## 📞 Need Help?

Refer to these files:
- `PROJECT_SETUP.md` - Detailed technical setup
- `LOGIN_CREDENTIALS.md` - Authentication details
- `README.md` - Original project documentation
- Backend logs: `docker logs trinitydev-backend-1 -f`
- Frontend logs: `docker logs trinitydev-frontend-1 -f`

---

**Status**: ✅ Ready to Use
**Last Updated**: January 17, 2026
**Location**: /home/hadeed/Pictures/TRINITY DEV
