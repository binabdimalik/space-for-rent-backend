
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
