from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

"""
    Create an engine that connects to the specified database URL
"""
engine = create_engine(DATABASE_URL)

"""
    Create a configured "Session" class
"""
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

"""
    Create a base class for our classes definitions
"""
Base = declarative_base()

"""
    Add query property to the base class
"""
Base.query = SessionLocal.query_property()

class DBSession:
    """
        This class handles the opening and closing of database sessions
    """
    def __enter__(self):
        """
            Enter the runtime context related to this object.
        
            Returns:
                The database session.
        """
        self.db = SessionLocal()
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        """
            Closes the database session.
        """
        self.db.close()

def get_db():
    """
        Provides a new instance of DBSession for database operations.

        Returns:
            An instance of DBSession
    """
    return DBSession()
