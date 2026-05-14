#!/usr/bin/python3
"""DBStorage engine"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        
        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
            pool_pre_ping=True
        )

    def all(self, cls=None):
        """Query all objects"""
        from models.state import State
        from models.city import City
        
        # Only query State and City for now (User, Place, etc tables don't exist yet)
        if cls is None:
            classes = [State, City]
        else:
            classes = [cls]
        
        objects = {}
        for cl in classes:
            try:
                for obj in self.__session.query(cl).all():
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    objects[key] = obj
            except:
                pass
        return objects

    def new(self, obj):
        """Add object to session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create tables and session"""
        from models.base_model import Base
        from models.state import State
        from models.city import City
        
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session()
