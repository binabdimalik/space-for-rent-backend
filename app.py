# app.py - API Version (for React frontend)
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable React to connect

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ==================== MODELS ====================

# 1. User Model
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(100))
    profile_picture = db.Column(db.String(200))
    
    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'profile_picture': self.profile_picture
        }

# 2. Space Model
class Space(db.Model):
    __tablename__ = 'spaces'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, default=2)
    amenities = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    
    # Relationships
    bookings = db.relationship('Booking', backref='space', lazy=True)
    reviews = db.relationship('Review', backref='space', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price_per_night': self.price_per_night,
            'location': self.location,
            'capacity': self.capacity,
            'amenities': self.amenities,
            'image_url': self.image_url
        }

# 3. Booking Model (Many-to-Many Relationship)
class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    space_id = db.Column(db.Integer, db.ForeignKey('spaces.id'), nullable=False)
    check_in_date = db.Column(db.String(50), nullable=False)  # Store as string for simplicity
    check_out_date = db.Column(db.String(50), nullable=False)
    guests = db.Column(db.Integer, default=1)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'space_id': self.space_id,
            'check_in_date': self.check_in_date,
            'check_out_date': self.check_out_date,
            'guests': self.guests,
            'total_price': self.total_price,
            'status': self.status
        }

# 4. Review Model
class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    space_id = db.Column(db.Integer, db.ForeignKey('spaces.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'space_id': self.space_id,
            'rating': self.rating,
            'comment': self.comment
        }

# ==================== ROUTES ====================

# Home route
@app.get('/')
def index():
    return jsonify({
        "message": "Spaces for Rent API",
        "version": "1.0",
        "endpoints": {
            "spaces": "/api/spaces",
            "users": "/api/users",
            "bookings": "/api/bookings",
            "reviews": "/api/reviews"
        }
    })

# Spaces CRUD Routes
@app.get('/api/spaces')
def get_spaces():
    spaces = Space.query.all()
    return jsonify([space.to_dict() for space in spaces])

@app.get('/api/spaces/<int:id>')
def get_space(id):
    space = Space.query.get_or_404(id)
    return jsonify(space.to_dict())

@app.post('/api/spaces')
def create_space():
    data = request.get_json()
    
    # Validation
    required_fields = ['title', 'description', 'price_per_night', 'location']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400
    
    new_space = Space(
        title=data['title'],
        description=data['description'],
        price_per_night=float(data['price_per_night']),
        location=data['location'],
        capacity=data.get('capacity', 2),
        amenities=data.get('amenities', ''),
        image_url=data.get('image_url', '')
    )
    
    db.session.add(new_space)
    db.session.commit()
    
    return jsonify(new_space.to_dict()), 201

@app.put('/api/spaces/<int:id>')
def update_space(id):
    space = Space.query.get_or_404(id)
    data = request.get_json()
    
    if 'title' in data:
        space.title = data['title']
    if 'description' in data:
        space.description = data['description']
    if 'price_per_night' in data:
        space.price_per_night = float(data['price_per_night'])
    if 'location' in data:
        space.location = data['location']
    
    db.session.commit()
    return jsonify(space.to_dict())

@app.delete('/api/spaces/<int:id>')
def delete_space(id):
    space = Space.query.get_or_404(id)
    db.session.delete(space)
    db.session.commit()
    return jsonify({"message": "Space deleted successfully"}), 200

# Users Routes
@app.get('/api/users')
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.post('/api/users')
def create_user():
    data = request.get_json()
    
    if 'username' not in data or 'email' not in data:
        return jsonify({"error": "Username and email are required"}), 400
    
    new_user = User(
        username=data['username'],
        email=data['email'],
        full_name=data.get('full_name', ''),
        profile_picture=data.get('profile_picture', '')
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(new_user.to_dict()), 201

# Bookings Routes
@app.get('/api/bookings')
def get_bookings():
    bookings = Booking.query.all()
    return jsonify([booking.to_dict() for booking in bookings])

@app.post('/api/bookings')
def create_booking():
    data = request.get_json()
    
    required_fields = ['user_id', 'space_id', 'check_in_date', 'check_out_date', 'total_price']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400
    
    new_booking = Booking(
        user_id=data['user_id'],
        space_id=data['space_id'],
        check_in_date=data['check_in_date'],
        check_out_date=data['check_out_date'],
        guests=data.get('guests', 1),
        total_price=float(data['total_price']),
        status=data.get('status', 'pending')
    )
    
    db.session.add(new_booking)
    db.session.commit()
    
    return jsonify(new_booking.to_dict()), 201

# Reviews Routes
@app.get('/api/reviews')
def get_reviews():
    reviews = Review.query.all()
    return jsonify([review.to_dict() for review in reviews])

@app.post('/api/reviews')
def create_review():
    data = request.get_json()
    
    if 'user_id' not in data or 'space_id' not in data or 'rating' not in data:
        return jsonify({"error": "user_id, space_id, and rating are required"}), 400
    
    new_review = Review(
        user_id=data['user_id'],
        space_id=data['space_id'],
        rating=data['rating'],
        comment=data.get('comment', '')
    )
    
    db.session.add(new_review)
    db.session.commit()
    
    return jsonify(new_review.to_dict()), 201

# ==================== INITIALIZE DATABASE ====================

@app.before_first_request
def create_tables():
    db.create_all()
    
    # Add sample data if database is empty
    if Space.query.count() == 0:
        sample_spaces = [
            Space(
                title="Modern Apartment",
                description="Beautiful apartment in city center",
                price_per_night=120.50,
                location="New York, NY",
                capacity=4,
                amenities="WiFi, Kitchen, AC"
            ),
            Space(
                title="Beach House",
                description="Luxury beachfront villa",
                price_per_night=350.00,
                location="Miami, FL",
                capacity=8,
                amenities="Pool, WiFi, Ocean View"
            )
        ]
        db.session.add_all(sample_spaces)
        db.session.commit()
        print("✅ Sample spaces added")

if __name__ == '__main__':
    app.run(port=5555, debug=True)