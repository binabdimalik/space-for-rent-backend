# models/space.py
from app import db

class Space(db.Model):
    """
    Space Model - Represents a rental space listing (simplified version)
    """
    __tablename__ = 'spaces'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
