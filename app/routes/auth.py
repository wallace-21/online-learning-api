#!/usr/bin/python3

""" """

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from models.user import User
from database import get_db

# Initialize the HTTPBasicAuth instance
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    """
    Verify the password for a given username.

    Args:
        username (str): The username of the user.
        password (str): The password provided for verification.

    Returns:
        User: The user object if the username exists and the password is correct.
        None: If the username does not exist or the password is incorrect.
    """
    with get_db() as db:
        user = db.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return user
    return None
