#!/usr/bin/python3
"""BaseModel class that defines all common attributes/methods"""
from datetime import datetime
import uuid
import models

class BaseModel:
    """Base class of all models"""

    def __init__(self, *args, **kwargs):
        """Initialize BaseModel instance"""
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key in ("created_at", "updated_at"):
                    value = datetime.fromisoformat(value)
                setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)
    
    def __str__(self):
        """String representation"""
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__
        )
    
    def save(self):
        """Update updated_at and save to storage"""
        self.updated_at = datetime.now()
        models.storage.save()
    
    def to_dict(self):
        """Convert instance to dictionary format"""
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        return new_dict