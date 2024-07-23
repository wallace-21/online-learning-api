#!/usr/bin/python3

"""
    imports neseccery for the program
"""
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from uuid import uuid4
from database import get_db
from models.user import User
from .auth import auth
from werkzeug.security import generate_password_hash, check_password_hash


# Initialize the request parser and add expected arguments for user creation
user_post_args = reqparse.RequestParser()
user_post_args.add_argument(
    "username",
    type=str,
    help="Username of the user",
    required=True
)
user_post_args.add_argument(
    "password",
    type=str,
    help="Password for the user",
    required=True
)

# Define the resource fields for marshalling response data
resource_fields = {
    "id": fields.Integer,
    "username": fields.String
}


class UserResource(Resource):
    """
        Resource for handling individual user operations,
        such as creating and retrieving a user.
    """
    @marshal_with(resource_fields)
    def post(self):
        """
            Handle POST requests to create a new user.

            Parses the request arguments, creates a new user,
            and saves it to the database.

            Returns:
                The created user object and a 201 status code.
        """
        args = user_post_args.parse_args()
        hashed_password = generate_password_hash(args["password"])
        user = User(username=args["username"], password=hashed_password)

        with get_db() as db:
            db.add(user)
            # Commit the transaction to save changes
            db.commit()
            # Refresh the user instance to ensure all
            # fields are properly populated
            db.refresh(user)
        return user, 201


    @auth.login_required
    @marshal_with(resource_fields)
    def get(self, user_id):
        """
            Handle GET requests to retrieve a user by ID.

            Args:
                user_id (str): The ID of the user to retrieve.

            Returns:
                The user object if found, or a 404 error
                if the user does not exist.
        """
        with get_db() as db:
            # Query the user by ID
            user = db.query(User).filter_by(id=user_id).first()
            if not user:
                abort(404, message="username not found")
            return user
            
            # Commit the transaction to save changes
            db.commit()
            db.refresh(user)

            return user, 201


class UsersResource(Resource):
    """
        Resource for handling operations to retrieving all users.
    """
    @auth.login_required
    @marshal_with(resource_fields)
    def get(self):
        """
            Handle GET requests to retrieve all users.

            Returns:
                A list of all user objects.
        """
        with get_db() as db:
            all_users = db.query(User).all()
            return all_users

class LoginResource(Resource):
    """
        Resource for handling user authentication.
    """
    def post(self):
        """
            Handle POST requests to authenticate a user.

            Parses the request arguments, validates the user,
            and returns an appropriate response.

            Returns:
                A success message and status code if authentication
                is successful, or an error message if not.
        """
        args = user_post_args.parse_args()
        username = args["username"]
        password = args["password"]

        with get_db() as db:
            user = db.query(User).filter_by(username=username).first()
            if not user or not check_password_hash(user.password, password):
                abort(401, message="Invalid username or password")
            return {"message": "Login successful"}, 200
