"""
models/space.py - Space Model Definition (Alternative)

This file contains an alternative/simplified Space model definition.
Note: The main application uses the Space model defined in app.py,
which has additional fields for the complete rental platform.

This file demonstrates a modular approach to organizing models
in separate files within a models package.
"""

# Import the database instance from the main app
from app import db


class Space(db.Model):
    """
    Space Model - Represents a rental space listing (simplified version)
    
    This is a basic version of the Space model with essential fields.
    For the full implementation with all features, see app.py.
    
    Attributes:
        id: Unique identifier (primary key)
        title: Name of the space
        description: Detailed description
        price: Rental price
        location: Physical address
        created_at: Timestamp when the space was created
    """
    # Define the database table name
    __tablename__ = 'spaces'
    
    # Primary key - unique identifier for each space
    id = db.Column(db.Integer, primary_key=True)
    
    # Title - name of the rental space
    title = db.Column(db.String(100), nullable=False)
    
    # Description - detailed information about the space
    description = db.Column(db.Text)
    
    # Price - rental cost (simplified, single price field)
    price = db.Column(db.Float, nullable=False)
    
    # Location - address or area description
    location = db.Column(db.String(100))
    
    # Created at - automatically set to current timestamp when record is created
    # server_default uses the database server's current time
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def to_dict(self):
        """
        Convert Space object to dictionary for JSON serialization
        
        This method is called when we need to send space data
        to the frontend as JSON.
        
        Returns:
            dict: Dictionary representation of the space
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'location': self.location,
            # Convert datetime to ISO format string, handle None case
            'created_at': self.created_at.isoformat() if self.created_at else None
        }