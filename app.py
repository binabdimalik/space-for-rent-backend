# app.py
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Initialize app
app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Basic route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to Spaces for Rent API"})

# Import models (to be created)
from models import *

if __name__ == '__main__':
    app.run(port=5555, debug=True)