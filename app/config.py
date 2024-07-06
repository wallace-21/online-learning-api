import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
        Configuration class for setting up the SQLAlchemy database URI.
    """

    # The SQLALCHEMY_DATABASE_URI is retrieved from an environment variable named 'DATABASE_URL'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
