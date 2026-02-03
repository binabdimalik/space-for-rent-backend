
# Flask - The main web framework for building the API
from flask import Flask, jsonify, request

# SQLAlchemy - ORM (Object Relational Mapper) for database operations
from flask_sqlalchemy import SQLAlchemy

# Flask-Migrate - Handles database migrations (schema changes)
from flask_migrate import Migrate

# CORS - Cross-Origin Resource Sharing, allows React frontend to connect
from flask_cors import CORS

# Werkzeug security - For password hashing (secure password storage)
# Note: These are imported for future authentication implementation
from werkzeug.security import generate_password_hash, check_password_hash  # noqa: F401

# OS module - For environment variables and file paths
import os

# DateTime - For timestamp generation
from datetime import datetime

# ==================== APP CONFIGURATION ====================

# Create the Flask application instance
app = Flask(__name__)

# Enable CORS to allow the React frontend to make requests to this API
# Without this, browsers would block cross-origin requests
CORS(app)

# Get the absolute path of the directory containing this file
# Used for constructing the SQLite database path
basedir = os.path.abspath(os.path.dirname(__file__))

# Database configuration
# First checks for DATABASE_URL environment variable (used in production with PostgreSQL)
# Falls back to local SQLite database for development
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') or ('sqlite:///' + os.path.join(basedir, 'app.db'))

# Disable modification tracking to save memory (not needed for this app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secret key for session management and security features
# In production, this should be a secure random string from environment variables
app.config['SECRET_KEY'] = 'your-secret-key-here'

# ==================== INITIALIZE EXTENSIONS ====================

# Initialize SQLAlchemy with the Flask app
# This creates the 'db' object used for all database operations
db = SQLAlchemy(app)

# Initialize Flask-Migrate for database migrations
# Allows running 'flask db migrate' and 'flask db upgrade' commands
migrate = Migrate(app, db)


# ==================== DATABASE MODELS ====================
# Models define the structure of database tables using Python classes
# Each class represents a table, and each attribute represents a column

# ----------------------------------------------------------
# 1. USER MODEL - Stores user account information
# ----------------------------------------------------------
class User(db.Model):
    """
    User Model - Represents registered users of the platform
    
    Users can:
    - Book rental spaces
    - Leave reviews for spaces they've stayed at
    - Have a profile with personal information
    """
    # Define the table name in the database
    __tablename__ = 'users'
    
    # Primary key - unique identifier for each user
    id = db.Column(db.Integer, primary_key=True)
    
    # Username - must be unique, used for login
    username = db.Column(db.String(80), unique=True, nullable=False)
    
    # Email address - must be unique, used for communication
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # Full name - display name for the user
    full_name = db.Column(db.String(100))
    
    # Profile picture URL - optional profile image
    profile_picture = db.Column(db.String(200))
    
    # Password hash - securely stored password (never store plain text!)
    password_hash = db.Column(db.String(200))
    
    # Relationships - define connections to other tables
    # backref creates a reverse reference (booking.user, review.user)
    # lazy=True means related items are loaded on demand
    bookings = db.relationship('Booking', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    
    def to_dict(self):
        """
        Convert User object to dictionary for JSON serialization
        Note: password_hash is intentionally excluded for security
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'profile_picture': self.profile_picture
        }
    

# ----------------------------------------------------------
# 2. SPACE MODEL - Stores rental space listings
# ----------------------------------------------------------
class Space(db.Model):
    """
    Space Model - Represents rental spaces available on the platform
    
    Each space has:
    - Basic info (title, description, location)
    - Pricing information
    - Geographic coordinates for map display
    - Capacity and amenities
    """
    # Define the table name in the database
    __tablename__ = 'spaces'
    
    # Primary key - unique identifier for each space
    id = db.Column(db.Integer, primary_key=True)
    
    # Title - name of the space (e.g., "Modern Meeting Room")
    title = db.Column(db.String(100), nullable=False)
    
    # Description - detailed information about the space
    description = db.Column(db.Text, nullable=False)
    
    # Price per night - rental cost in dollars
    price_per_night = db.Column(db.Float, nullable=False)
    
    # Location - address or area description
    location = db.Column(db.String(100), nullable=False)
    
    # Geographic coordinates for map display
    latitude = db.Column(db.Float)   # North-South position
    longitude = db.Column(db.Float)  # East-West position
    
    # Capacity - maximum number of guests/people
    capacity = db.Column(db.Integer, default=2)
    
    # Amenities - comma-separated list of features (WiFi, Kitchen, etc.)
    amenities = db.Column(db.Text)
    
    # Image URL - photo of the space
    image_url = db.Column(db.String(200))
    
    # Relationships to bookings and reviews
    bookings = db.relationship('Booking', backref='space', lazy=True)
    reviews = db.relationship('Review', backref='space', lazy=True)
    
    def to_dict(self):
        """
        Convert Space object to dictionary for JSON serialization
        Used when sending space data to the frontend
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price_per_night': self.price_per_night,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'capacity': self.capacity,
            'amenities': self.amenities,
            'image_url': self.image_url
        }

# ----------------------------------------------------------
# 3. BOOKING MODEL - Stores reservation information
# ----------------------------------------------------------
class Booking(db.Model):
    """
    Booking Model - Represents space reservations
    
    Links users to spaces with:
    - Check-in and check-out dates
    - Number of guests
    - Total price
    - Booking status (pending, confirmed, cancelled)
    """
    # Define the table name in the database
    __tablename__ = 'bookings'
    
    # Primary key - unique identifier for each booking
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to users table - who made the booking
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Foreign key to spaces table - which space was booked
    space_id = db.Column(db.Integer, db.ForeignKey('spaces.id'), nullable=False)
    
    # Reservation dates (stored as strings for simplicity)
    check_in_date = db.Column(db.String(50), nullable=False)
    check_out_date = db.Column(db.String(50), nullable=False)
    
    # Number of guests for this booking
    guests = db.Column(db.Integer, default=1)
    
    # Total cost of the booking
    total_price = db.Column(db.Float, nullable=False)
    
    # Booking status: 'pending', 'confirmed', or 'cancelled'
    status = db.Column(db.String(20), default='pending')
    
    def to_dict(self):
        """
        Convert Booking object to dictionary for JSON serialization
        """
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
    

# ----------------------------------------------------------
# 4. REVIEW MODEL - Stores user reviews and ratings
# ----------------------------------------------------------
class Review(db.Model):
    """
    Review Model - Represents user reviews for spaces
    
    Allows users to:
    - Rate spaces (1-5 stars)
    - Leave written comments about their experience
    """
    # Define the table name in the database
    __tablename__ = 'reviews'
    
    # Primary key - unique identifier for each review
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to users table - who wrote the review
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Foreign key to spaces table - which space is being reviewed
    space_id = db.Column(db.Integer, db.ForeignKey('spaces.id'), nullable=False)
    
    # Star rating from 1 to 5
    rating = db.Column(db.Integer, nullable=False)
    
    # Written review/feedback (optional)
    comment = db.Column(db.Text)
    
    def to_dict(self):
        """
        Convert Review object to dictionary for JSON serialization
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'space_id': self.space_id,
            'rating': self.rating,
            'comment': self.comment
        }


# ==================== API ROUTES ====================
# Routes define the API endpoints that the frontend can call
# Each route handles a specific HTTP method (GET, POST, PUT, DELETE)

# ----------------------------------------------------------
# HOME ROUTE - API Information
# ----------------------------------------------------------
@app.get('/')
def index():
    """
    Home Route - Returns API information and available endpoints
    
    This is the root endpoint that provides documentation about
    the API and lists all available endpoints for developers.
    
    Returns:
        JSON object with API info and endpoint list
    """
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

# ----------------------------------------------------------
# SPACES ROUTES - CRUD operations for rental spaces
# ----------------------------------------------------------

@app.get('/api/spaces')
def get_spaces():
    """
    GET /api/spaces - Retrieve all spaces
    
    Fetches all rental spaces from the database and returns them
    as a JSON array. Used by the frontend to display space listings.
    
    Returns:
        JSON array of all space objects
    """
    # Query all spaces from the database
    spaces = Space.query.all()
    # Convert each space to dictionary and return as JSON
    return jsonify([space.to_dict() for space in spaces])

@app.get('/api/spaces/<int:id>')
def get_space(id):
    """
    GET /api/spaces/<id> - Retrieve a single space by ID
    
    Fetches a specific space by its ID. Returns 404 if not found.
    Used when displaying space details page.
    
    Args:
        id: The unique identifier of the space
        
    Returns:
        JSON object of the space, or 404 error
    """
    # get_or_404 returns the space or raises a 404 error if not found
    space = Space.query.get_or_404(id)
    return jsonify(space.to_dict())

@app.post('/api/spaces')
def create_space():
    """
    POST /api/spaces - Create a new space listing
    
    Creates a new rental space with the provided data.
    Validates that all required fields are present.
    
    Request Body:
        title (required): Name of the space
        description (required): Detailed description
        price_per_night (required): Rental price
        location (required): Address/location
        latitude (optional): GPS latitude
        longitude (optional): GPS longitude
        capacity (optional): Max guests (default: 2)
        amenities (optional): Features list
        image_url (optional): Photo URL
        
    Returns:
        201: Created space object
        400: Validation error
    """
    # Get JSON data from request body
    data = request.get_json()
    
    # Validate required fields are present
    required_fields = ['title', 'description', 'price_per_night', 'location']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400
    
    # Create new Space object with provided data
    new_space = Space(
        title=data['title'],
        description=data['description'],
        price_per_night=float(data['price_per_night']),
        location=data['location'],
        latitude=data.get('latitude'),          # Optional field
        longitude=data.get('longitude'),        # Optional field
        capacity=data.get('capacity', 2),       # Default to 2 if not provided
        amenities=data.get('amenities', ''),    # Default to empty string
        image_url=data.get('image_url', '')     # Default to empty string
    )
    
    # Add to database session and commit the transaction
    db.session.add(new_space)
    db.session.commit()
    
    # Return the created space with 201 Created status
    return jsonify(new_space.to_dict()), 201

@app.put('/api/spaces/<int:id>')
def update_space(id):
    """
    PUT /api/spaces/<id> - Update an existing space
    
    Updates a space with the provided data. Only updates
    fields that are included in the request body.
    
    Args:
        id: The unique identifier of the space to update
        
    Request Body:
        Any space fields to update (all optional)
        
    Returns:
        Updated space object, or 404 if not found
    """
    # Find the space or return 404
    space = Space.query.get_or_404(id)
    
    # Get JSON data from request
    data = request.get_json()
    
    # Update only the fields that are provided in the request
    if 'title' in data:
        space.title = data['title']
    if 'description' in data:
        space.description = data['description']
    if 'price_per_night' in data:
        space.price_per_night = float(data['price_per_night'])
    if 'location' in data:
        space.location = data['location']
    if 'latitude' in data:
        space.latitude = data['latitude']
    if 'longitude' in data:
        space.longitude = data['longitude']
    
    # Commit the changes to the database
    db.session.commit()
    
    # Return the updated space
    return jsonify(space.to_dict())

@app.delete('/api/spaces/<int:id>')
def delete_space(id):
    """
    DELETE /api/spaces/<id> - Delete a space
    
    Permanently removes a space from the database.
    
    Args:
        id: The unique identifier of the space to delete
        
    Returns:
        Success message, or 404 if not found
    """
    # Find the space or return 404
    space = Space.query.get_or_404(id)
    
    # Delete from database
    db.session.delete(space)
    db.session.commit()
    
    # Return success message
    return jsonify({"message": "Space deleted successfully"}), 200



# ----------------------------------------------------------
# USERS ROUTES - User management endpoints
# ----------------------------------------------------------

@app.get('/api/users')
def get_users():
    """
    GET /api/users - Retrieve all users
    
    Fetches all registered users from the database.
    Used by admin panel to view user list.
    
    Returns:
        JSON array of all user objects (without passwords)
    """
    # Query all users from database
    users = User.query.all()
    # Convert to JSON (to_dict excludes password_hash)
    return jsonify([user.to_dict() for user in users])

@app.post('/api/users')
def create_user():
    """
    POST /api/users - Register a new user
    
    Creates a new user account with the provided data.
    
    Request Body:
        username (required): Unique username
        email (required): Unique email address
        full_name (optional): User's full name
        profile_picture (optional): Profile image URL
        
    Returns:
        201: Created user object
        400: Validation error
    """
    # Get JSON data from request
    data = request.get_json()
    
    # Validate required fields
    if 'username' not in data or 'email' not in data:
        return jsonify({"error": "Username and email are required"}), 400
    
    # Create new User object
    new_user = User(
        username=data['username'],
        email=data['email'],
        full_name=data.get('full_name', ''),
        profile_picture=data.get('profile_picture', '')
    )
    
    # Add to database and commit
    db.session.add(new_user)
    db.session.commit()
    
    # Return created user with 201 status
    return jsonify(new_user.to_dict()), 201
