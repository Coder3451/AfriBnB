#!/usr/bin/python3
"""FileStorage class for serialization/desialization"""
import json
import os

class FileStorage:
    """Serializes instaces to a JSON and deserializes JSON to instances"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return all objects"""
        return self.__objects
    
    def new(self, obj):
        """Add new object to storage"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj
    
    def save(self):
        """Serialize objecs to JSON file"""
        obj_dict = {}
        for key, obj in self.__objects.items():
            obj_dict[key] = obj.to_dict()
        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(obj_dict, f)
    
    def reload(self):
        """Deserialize JSON file to objects"""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
            }

        if os.path.exists(self.__file_path):
            with open(self.__file_path, "r", encoding="utf-8") as f:
                obj_dict = json.load(f)
                for key, value in obj_dict.items():
                    cls_name = value["__class__"]
                    self.__objects[key] = classes[cls_name](**value)