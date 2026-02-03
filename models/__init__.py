"""
models/__init__.py - Models Package Initialization

This file makes the models directory a Python package and exports
the model classes for easy importing elsewhere in the application.

Usage:
    from models import Space
    
Note: The main Space model is defined in app.py for this project.
This separate models/space.py file is an alternative structure.
"""

# Import the Space model from the space module
from .space import Space

# Define what gets exported when using "from models import *"
__all__ = ['Space']