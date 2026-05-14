# AfriBnB - Mini Airbnb MVP

A production-ready mini Airbnb clone built with Flask, SQLAlchemy, and JWT authentication. Perfect for property owners to list accommodations and travelers to find and review them.

## ✨ Features

- **User Authentication**: Register and login with secure password hashing using bcrypt
- **JWT Tokens**: Secure API access with JSON Web Tokens
- **Place Listings**: Create, read, update, and delete property listings
- **Reviews**: Users can leave ratings and reviews on listings
- **Amenities**: Manage available amenities for properties
- **Authorization**: Users can only modify their own listings
- **RESTful API**: Full-featured API for all operations
- **Frontend UI**: Simple, responsive web interface for browsing and managing listings
- **Database**: SQLAlchemy ORM with support for PostgreSQL and SQLite

## 🚀 Quick Start

### Local Development

1. **Clone and setup**:
```bash
cd c:\Dev\AfriBnB
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your settings:
# DATABASE_URL=sqlite:///afribnb.db  (for local dev)
# FLASK_ENV=development
# DEBUG=True
```

3. **Run the application**:
```bash
python app.py
```

The app will be available at `http://localhost:5000`

4. **Run tests**:
```bash
pytest tests.py -v
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get current user profile (requires token)

### Places (Listings)
- `POST /api/places` - Create new listing (requires auth)
- `GET /api/places` - Get all listings (paginated)
- `GET /api/places/<id>` - Get listing details
- `PUT /api/places/<id>` - Update listing (owner only)
- `DELETE /api/places/<id>` - Delete listing (owner only)

### Reviews
- `POST /api/places/<id>/reviews` - Create review for place (requires auth)
- `GET /api/places/<id>/reviews` - Get reviews for place
- `DELETE /api/reviews/<id>` - Delete review (owner only)

### Amenities
- `POST /api/amenities` - Create amenity (requires auth)
- `GET /api/amenities` - Get all amenities

### System
- `GET /api/health` - Health check
- `GET /api/info` - API information

## 📋 Example Usage

### Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123"
  }'
```

Response includes `access_token` - use this in subsequent requests:

### Create Listing
```bash
curl -X POST http://localhost:5000/api/places \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "name": "Beautiful Beachfront Villa",
    "description": "Stunning villa with ocean views",
    "city": "Accra",
    "country": "Ghana",
    "price_per_night": 250,
    "rooms": 3,
    "bathrooms": 2,
    "max_guests": 6
  }'
```

## 🗄️ Database Models

### User
- `id` - UUID primary key
- `email` - Unique email address
- `password_hash` - Hashed password (bcrypt)
- `first_name`, `last_name` - User profile info
- `created_at`, `updated_at` - Timestamps
- Relations: owns multiple Places, writes Reviews

### Place
- `id` - UUID primary key
- `owner_id` - Reference to User who owns the place
- `name`, `description` - Listing details
- `address`, `city`, `country` - Location info
- `price_per_night` - Daily rate
- `rooms`, `bathrooms` - Property specs
- `max_guests` - Maximum occupancy
- `created_at`, `updated_at` - Timestamps
- Relations: has many Reviews, owner is User

### Review
- `id` - UUID primary key
- `place_id` - Reference to reviewed Place
- `reviewer_id` - Reference to User writing review
- `rating` - 1-5 star rating
- `comment` - Review text
- `created_at`, `updated_at` - Timestamps

### Amenity
- `id` - UUID primary key
- `name` - Amenity name (WiFi, Pool, etc.)
- `created_at` - Creation timestamp

## 🔐 Security Features

- ✅ Passwords hashed with bcrypt (not stored in plaintext)
- ✅ JWT authentication tokens for stateless API access
- ✅ Authorization checks (users can only modify their own listings)
- ✅ CORS enabled for cross-origin requests
- ✅ Environment variables for sensitive config
- ✅ SQL injection prevention with SQLAlchemy ORM

## 📦 Deployment

### Deploy to Render (Free Tier)

1. **Push to GitHub**:
```bash
git init
git add .
git commit -m "Initial commit: AfriBnB MVP"
git remote add origin https://github.com/YOUR_USERNAME/afribnb.git
git push -u origin main
```

2. **Create Render account** at https://render.com

3. **Create new Web Service**:
   - Connect GitHub repository
   - Select repository
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn wsgi:app`

4. **Add environment variables** in Render dashboard:
   - `DATABASE_URL` - PostgreSQL URL provided by Render
   - `JWT_SECRET_KEY` - Your secret key
   - `SECRET_KEY` - Your Flask secret key
   - `FLASK_ENV` - production

5. **Deploy** - Render will automatically build and deploy

### Deploy to Vercel (Frontend Only)

Frontend code can be deployed separately if you want a static deployment.

### Deploy to Heroku (Deprecated but still works)

```bash
heroku login
heroku create afribnb-app
git push heroku main
heroku config:set DATABASE_URL=your_postgres_url
heroku open
```

## 🧪 Testing

Run the full test suite:

```bash
pytest tests.py -v

# Run specific test
pytest tests.py::test_register_user -v

# Run with coverage
pip install pytest-cov
pytest tests.py --cov=app
```

Test coverage includes:
- ✅ User registration and login
- ✅ JWT authentication
- ✅ Place CRUD operations
- ✅ Review creation and deletion
- ✅ Authorization checks
- ✅ Amenity management
- ✅ Error handling

## 📱 Frontend Features

- User authentication UI (register/login)
- Browse all listings with pagination
- Filter by location and price (coming soon)
- Create/edit/delete your own listings
- Leave reviews on other properties
- Responsive mobile-friendly design

## 🛠️ Tech Stack

- **Backend**: Flask 2.3.3 with Flask-SQLAlchemy
- **Authentication**: Flask-JWT-Extended with bcrypt
- **Database**: SQLAlchemy ORM (PostgreSQL/SQLite)
- **Frontend**: Vanilla JavaScript with responsive CSS
- **Testing**: Pytest
- **Deployment**: Render, Heroku, Vercel compatible

## 📝 Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/afribnb_prod

# Flask
FLASK_ENV=production
DEBUG=False
SECRET_KEY=your-secret-key-min-32-chars-random

# JWT
JWT_SECRET_KEY=your-jwt-secret-key-min-32-chars

# Server
PORT=5000
```

## 🐛 Troubleshooting

### Database connection issues
- Check `DATABASE_URL` format
- Ensure PostgreSQL server is running
- Verify credentials are correct

### JWT token errors
- Ensure `JWT_SECRET_KEY` is set in environment
- Check token hasn't expired
- Include `Authorization: Bearer TOKEN` header

### CORS errors
- Flask-CORS is enabled for all origins in development
- Configure specific origins in production

## ✅ Production Checklist

Before deploying to production:

- [ ] Change all secret keys and passwords
- [ ] Set `FLASK_ENV=production`
- [ ] Set `DEBUG=False`
- [ ] Configure real PostgreSQL database
- [ ] Setup HTTPS/SSL
- [ ] Configure CORS for your domain
- [ ] Setup error logging and monitoring
- [ ] Run full test suite
- [ ] Backup database before first production deploy
- [ ] Setup automated backups
- [ ] Monitor application performance
- [ ] Configure rate limiting
- [ ] Setup security headers

## 👨‍💻 Authors

- Segni Jabesa - segniwoldemichael@gmail.com

---

**Built with ❤️ as a mini Airbnb MVP. Ready for production deployment!**