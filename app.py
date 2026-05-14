#!/usr/bin/env python3
"""
AfriBnB Flask Application - Production MVP
Full CRUD API with JWT Authentication
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt
from datetime import datetime
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///afribnb.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# =====================
# DATABASE MODELS
# =====================

class User(db.Model):
    """User model with authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: __import__('uuid').uuid4().hex)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    places = db.relationship('Place', backref='owner', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='reviewer', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Verify password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        """Convert to dict"""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat(),
        }


class Place(db.Model):
    """Place/Listing model"""
    __tablename__ = 'places'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: __import__('uuid').uuid4().hex)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text)
    address = db.Column(db.String(255))
    city = db.Column(db.String(128))
    country = db.Column(db.String(128))
    price_per_night = db.Column(db.Float, nullable=False)
    max_guests = db.Column(db.Integer, default=1)
    rooms = db.Column(db.Integer, default=1)
    bathrooms = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dict"""
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'city': self.city,
            'country': self.country,
            'price_per_night': self.price_per_night,
            'max_guests': self.max_guests,
            'rooms': self.rooms,
            'bathrooms': self.bathrooms,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }


class Review(db.Model):
    """Review model"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: __import__('uuid').uuid4().hex)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    reviewer_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dict"""
        return {
            'id': self.id,
            'place_id': self.place_id,
            'reviewer_id': self.reviewer_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat(),
        }


class Amenity(db.Model):
    """Amenity model"""
    __tablename__ = 'amenities'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: __import__('uuid').uuid4().hex)
    name = db.Column(db.String(255), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dict"""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
        }


# =====================
# AUTHENTICATION ROUTES
# =====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register new user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    user = User(
        email=data['email'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', '')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'message': 'User registered successfully',
        'user': user.to_dict(),
        'access_token': access_token
    }), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(),
        'access_token': access_token
    }), 200


@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def profile():
    """Get current user profile"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200


# =====================
# PLACE CRUD ROUTES
# =====================

@app.route('/api/places', methods=['POST'])
@jwt_required()
def create_place():
    """Create new listing"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('price_per_night'):
        return jsonify({'error': 'Name and price_per_night required'}), 400
    
    place = Place(
        owner_id=user_id,
        name=data['name'],
        description=data.get('description', ''),
        address=data.get('address', ''),
        city=data.get('city', ''),
        country=data.get('country', ''),
        price_per_night=data['price_per_night'],
        max_guests=data.get('max_guests', 1),
        rooms=data.get('rooms', 1),
        bathrooms=data.get('bathrooms', 1)
    )
    
    db.session.add(place)
    db.session.commit()
    
    return jsonify({'message': 'Place created', 'place': place.to_dict()}), 201


@app.route('/api/places', methods=['GET'])
def get_places():
    """Get all listings"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    places = Place.query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'places': [p.to_dict() for p in places.items],
        'total': places.total,
        'pages': places.pages,
        'current_page': page
    }), 200


@app.route('/api/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Get place details"""
    place = Place.query.get(place_id)
    
    if not place:
        return jsonify({'error': 'Place not found'}), 404
    
    return jsonify(place.to_dict()), 200


@app.route('/api/places/<place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    """Update place"""
    user_id = get_jwt_identity()
    place = Place.query.get(place_id)
    
    if not place:
        return jsonify({'error': 'Place not found'}), 404
    
    if place.owner_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    if 'name' in data:
        place.name = data['name']
    if 'description' in data:
        place.description = data['description']
    if 'price_per_night' in data:
        place.price_per_night = data['price_per_night']
    if 'address' in data:
        place.address = data['address']
    if 'city' in data:
        place.city = data['city']
    if 'country' in data:
        place.country = data['country']
    if 'max_guests' in data:
        place.max_guests = data['max_guests']
    if 'rooms' in data:
        place.rooms = data['rooms']
    if 'bathrooms' in data:
        place.bathrooms = data['bathrooms']
    
    db.session.commit()
    
    return jsonify({'message': 'Place updated', 'place': place.to_dict()}), 200


@app.route('/api/places/<place_id>', methods=['DELETE'])
@jwt_required()
def delete_place(place_id):
    """Delete place"""
    user_id = get_jwt_identity()
    place = Place.query.get(place_id)
    
    if not place:
        return jsonify({'error': 'Place not found'}), 404
    
    if place.owner_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(place)
    db.session.commit()
    
    return jsonify({'message': 'Place deleted'}), 200


# =====================
# REVIEW CRUD ROUTES
# =====================

@app.route('/api/places/<place_id>/reviews', methods=['POST'])
@jwt_required()
def create_review(place_id):
    """Create review for place"""
    user_id = get_jwt_identity()
    place = Place.query.get(place_id)
    
    if not place:
        return jsonify({'error': 'Place not found'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('rating') or not (1 <= data['rating'] <= 5):
        return jsonify({'error': 'Rating (1-5) required'}), 400
    
    review = Review(
        place_id=place_id,
        reviewer_id=user_id,
        rating=data['rating'],
        comment=data.get('comment', '')
    )
    
    db.session.add(review)
    db.session.commit()
    
    return jsonify({'message': 'Review created', 'review': review.to_dict()}), 201


@app.route('/api/places/<place_id>/reviews', methods=['GET'])
def get_place_reviews(place_id):
    """Get reviews for place"""
    place = Place.query.get(place_id)
    
    if not place:
        return jsonify({'error': 'Place not found'}), 404
    
    reviews = Review.query.filter_by(place_id=place_id).all()
    
    return jsonify({
        'reviews': [r.to_dict() for r in reviews],
        'count': len(reviews)
    }), 200


@app.route('/api/reviews/<review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    """Delete review"""
    user_id = get_jwt_identity()
    review = Review.query.get(review_id)
    
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    
    if review.reviewer_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(review)
    db.session.commit()
    
    return jsonify({'message': 'Review deleted'}), 200


# =====================
# AMENITY ROUTES
# =====================

@app.route('/api/amenities', methods=['POST'])
@jwt_required()
def create_amenity():
    """Create amenity (admin only in real app)"""
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Name required'}), 400
    
    if Amenity.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Amenity already exists'}), 409
    
    amenity = Amenity(name=data['name'])
    db.session.add(amenity)
    db.session.commit()
    
    return jsonify({'message': 'Amenity created', 'amenity': amenity.to_dict()}), 201


@app.route('/api/amenities', methods=['GET'])
def get_amenities():
    """Get all amenities"""
    amenities = Amenity.query.all()
    
    return jsonify({
        'amenities': [a.to_dict() for a in amenities],
        'count': len(amenities)
    }), 200


# =====================
# HEALTH & INFO ROUTES
# =====================

@app.route('/', methods=['GET'])
def index():
    """Serve main index page"""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'healthy', 'version': '1.0.0'}), 200


@app.route('/api/info', methods=['GET'])
def info():
    """API info"""
    return jsonify({
        'name': 'AfriBnB API',
        'version': '1.0.0',
        'description': 'Mini Airbnb Clone MVP',
        'endpoints': {
            'auth': ['/api/auth/register', '/api/auth/login', '/api/auth/profile'],
            'places': ['/api/places', '/api/places/<id>'],
            'reviews': ['/api/places/<id>/reviews', '/api/reviews/<id>'],
            'amenities': ['/api/amenities']
        }
    }), 200


# =====================
# ERROR HANDLERS
# =====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500"""
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500


# =====================
# CREATE TABLES & RUN
# =====================

def create_tables():
    """Create database tables"""
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    create_tables()
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
