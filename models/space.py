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

    def to_dict(self):
        """
        Convert Space object to dictionary for JSON serialization
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'location': self.location,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
