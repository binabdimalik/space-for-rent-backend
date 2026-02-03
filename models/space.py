# models/space.py
from app import db

class Space(db.Model):
    """
    Space Model - Represents a rental space listing (simplified version)
    """
    __tablename__ = 'spaces'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
