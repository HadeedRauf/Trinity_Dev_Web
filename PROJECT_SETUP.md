# Trinity Dev Web - Project Setup Complete ✅

## 📍 Project Location
```
/home/hadeed/Pictures/TRINITY DEV
```

## 🔗 GitHub Repository
```
https://github.com/HadeedRauf/Trinity_Dev_Web.git
Owner: HadeedRauf
Branch: main
```

## 🚀 Services Status

All services are running and accessible:

| Service | Port | URL | Status |
|---------|------|-----|--------|
| Frontend (React) | 3000 | http://localhost:3000 | ✅ Running |
| Backend API (Django) | 8000 | http://localhost:8000/api/ | ✅ Running |
| PostgreSQL Database | 5432 | localhost:5432 | ✅ Running |

## 📁 Project Structure

```
TRINITY DEV/
├── backend/                    # Django REST Framework
│   ├── api/                   # API app (models, views, serializers)
│   ├── backend/               # Django settings
│   ├── manage.py              # Django management script
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile             # Backend container config
│
├── frontend/                  # React + Vite
│   ├── src/                   # React components & pages
│   ├── public/                # Static assets
│   ├── package.json           # Node dependencies
│   └── Dockerfile             # Frontend container config
│
├── docker-compose.yml         # Multi-container orchestration
├── .gitignore                 # Git ignore rules
└── README.md                  # Project documentation
```

## 🛠 Tech Stack

### Backend
- **Framework**: Django 5.2.10
- **API**: Django REST Framework
- **Auth**: djangorestframework-simplejwt (JWT tokens)
- **Database**: PostgreSQL 15
- **Server**: Gunicorn
- **Python**: 3.11

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **HTTP Client**: Axios
- **Styling**: CSS (custom)
- **Node**: 18+

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL 15 with persistent volume
- **Networking**: Docker bridge network (trinitydev_default)

## 🔐 Initial Setup

### Database Credentials
```
User: postgres
Password: postgres
Database: time_manager
Host: db
Port: 5432
```

### API Environment Variables (in docker-compose.yml)
```
DATABASE_NAME: time_manager
DATABASE_USER: postgres
DATABASE_PASSWORD: postgres
DATABASE_HOST: db
DATABASE_PORT: 5432
SECRET_KEY: changeme
REACT_APP_API_URL: http://localhost:8000/api
```

## 🌐 API Endpoints

### Authentication
```
POST   /api/token/          - Get JWT access/refresh tokens
POST   /api/token/refresh/  - Refresh access token
```

### Resources (Protected with JWT)
```
GET    /api/products/       - List all products
POST   /api/products/       - Create new product
GET    /api/products/{id}/  - Get product details
PUT    /api/products/{id}/  - Update product
DELETE /api/products/{id}/  - Delete product

GET    /api/customers/      - List all customers
POST   /api/customers/      - Create new customer
GET    /api/customers/{id}/ - Get customer details
PUT    /api/customers/{id}/ - Update customer
DELETE /api/customers/{id}/ - Delete customer

GET    /api/invoices/       - List all invoices
POST   /api/invoices/       - Create new invoice
GET    /api/invoices/{id}/  - Get invoice details
PUT    /api/invoices/{id}/  - Update invoice
DELETE /api/invoices/{id}/  - Delete invoice
```

## 🚢 Docker Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker logs trinitydev-backend-1 -f
docker logs trinitydev-frontend-1 -f
docker logs trinitydev-db-1 -f
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

### Rebuild Services
```bash
cd "/home/hadeed/Pictures/TRINITY DEV"
docker-compose up --build --detach
```

## 📝 Django Management

### Create Admin User
```bash
docker exec -it trinitydev-backend-1 python manage.py createsuperuser
```

### Access Django Admin
```
http://localhost:8000/admin/
```

### Run Tests
```bash
docker exec trinitydev-backend-1 python manage.py test
```

### Make Migrations
```bash
docker exec trinitydev-backend-1 python manage.py makemigrations
docker exec trinitydev-backend-1 python manage.py migrate
```

## 🎯 Features

### Implemented
- ✅ JWT-based authentication (access + refresh tokens)
- ✅ RESTful API for products, customers, invoices
- ✅ PostgreSQL database with persistent volumes
- ✅ React frontend with responsive design
- ✅ Django admin panel
- ✅ Docker containerization
- ✅ Hot reload in development (frontend)
- ✅ Database migrations

### Planned (From README)
- 🔲 Open Food Facts integration for product enrichment
- 🔲 KPI reports endpoint
- 🔲 Unit tests (target 20%+ coverage)
- 🔲 CI/CD pipeline
- 🔲 Technical documentation and UML diagrams

## 🎬 Quick Start

### Start Services
```bash
cd "/home/hadeed/Pictures/TRINITY DEV"
docker-compose up --build --detach
```

### Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/
- Django Admin: http://localhost:8000/admin/

### Check Status
```bash
docker ps --format "table {{.Names}}\t{{.Status}}"
```

## 📊 Database

### Persistent Storage
Database data is stored in Docker volume: `trinitydev_db_data`

To view data location:
```bash
docker volume inspect trinitydev_db_data
```

To backup database:
```bash
docker exec trinitydev-db-1 pg_dump -U postgres time_manager > backup.sql
```

To restore database:
```bash
docker exec -i trinitydev-db-1 psql -U postgres time_manager < backup.sql
```

## 🔍 Monitoring

### Check Container Health
```bash
docker stats
```

### View All Containers (including stopped)
```bash
docker ps -a
```

### Inspect Container Details
```bash
docker inspect trinitydev-backend-1
docker inspect trinitydev-frontend-1
docker inspect trinitydev-db-1
```

## 📚 Additional Resources

- Django Docs: https://docs.djangoproject.com
- DRF Docs: https://www.django-rest-framework.org
- React Docs: https://react.dev
- Vite Docs: https://vitejs.dev
- Docker Docs: https://docs.docker.com

---

**Last Updated**: January 17, 2026
**Project Status**: Ready for Development
