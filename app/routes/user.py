#!/usr/bin/python3

"""
    imports neseccery for the program
"""
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from uuid import uuid4
from database import get_db
from models.user import User


# Initialize the request parser and add expected arguments for user creation
user_post_args = reqparse.RequestParser()
user_post_args.add_argument("name", type=str,
                            help="Name shouldn't be empty", required=True)
user_post_args.add_argument("surname", type=str,
                            help="Surname shouldn't be empty", required=True)
user_post_args.add_argument("nationality", type=str,
                            help="Nationality shouldn't be empty",
                            required=True)
user_post_args.add_argument("email", type=str,
                            help="Email shouldn't be empty", required=True)
user_post_args.add_argument("password", help="Set a password", required=True)
user_post_args.add_argument("instructor", type=bool,
                            help="Are you an instuctor")

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("name", type=str,
                              help="Name shouldn't be empty")
user_update_args.add_argument("surname", type=str,
                              help="Surname shouldn't be empty")
user_update_args.add_argument("nationality", type=str,
                            help="Nationality shouldn't be empty")
user_update_args.add_argument("email", type=str,
                              help="Email shouldn't be empty")
user_update_args.add_argument("password", help="Set a password")
user_update_args.add_argument("instructor", type=bool,
                              help="Are you an instuctor")

# Define the resource fields for marshalling response data
resource_fields = {
    "name": fields.String,
    "surname": fields.String,
    "instructor": fields.Boolean,
    "nationality": fields.String,
    "email": fields.String,
    "date_created": fields.DateTime
}

# Define the full resource fields, including more information
full_resource_fields = {
    "id": fields.String,
    "name": fields.String,
    "surname": fields.String,
    "instructor": fields.Boolean,
    "nationality": fields.String,
    "email": fields.String,
    "password": fields.String,
    "date_created": fields.DateTime
}


class UserResource(Resource):
    """
        Resource for handling individual user operations,
        such as creating and retrieving a user.
    """
    @marshal_with(full_resource_fields)
    def post(self):
        """
            Handle POST requests to create a new user.

            Parses the request arguments, creates a new user,
            and saves it to the database.

            Returns:
                The created user object and a 201 status code.
        """
        args = user_post_args.parse_args()
        user = User(id=str(uuid4()),
                    name=args["name"],
                    surname=args["surname"],
                    instructor=args.get("instructor", False),
                    nationality=args["nationality"],
                    email=args["email"],
                    password=args["password"])

        with get_db() as db:
            db.add(user)
            # Commit the transaction to save changes
            db.commit()
            # Refresh the user instance to ensure all
            # fields are properly populated
            db.refresh(user)
        return user, 201

    @marshal_with(full_resource_fields)
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
                abort(404, message="user not found")
            return user
            
            # Commit the transaction to save changes
            db.commit()
            db.refresh(user)

            return user, 201
    @marshal_with(full_resource_fields)
    def put(self, user_id):
        """
            Update an existing user's details.

            Args:
                user_id (int): The ID of the user to update.

            Raises:
                404: If the user is not found.
                400: If attempting to update 'nationality' or 'instructor'.

            Returns:
                The updated user object and HTTP status code 201.
            """
        args = user_update_args.parse_args()

        with get_db() as db:
            # Query the user by ID
            user = db.query(User).filter_by(id=user_id).first()
            if not user:
                abort(404, message="User not found")

            # Check for forbidden fields
            if args["nationality"] is not None:
                abort(400, message="Updating 'nationality' is not allowed")
            if args["instructor"] is None:
                abort(400, message="Updating 'instructor' is not allowed")

            # Update fields if provided
            if args["name"] is not None:
                user.name = args["name"]
            if args["surname"] is not None:
                user.surname = args["surname"]
            if args["email"] is not None:
                user.email = args["email"]
            if args["password"] is not None:
                user.password = args["password"]

            # Commit the transaction to save changes
            db.commit()
            db.refresh(user)

            return user, 201
    def delete(self, user_id):
        """ Delete an existing user.

            Args:
                user_id (int): The ID of the user to delete.

            Raises:
                404: If the user is not found.

            Returns:
                dict: A message confirming the user has been deleted.
        """
        with get_db() as db:
            # Query the user by ID
            user = db.query(User).filter_by(id=user_id).first()
            if not user:
                abort(404, message="user not found")

            db.delete(user)
            # Commit the transaction to save changes
            db.commit()
            return {"message": "user deleted"}


class UsersResource(Resource):
    """
        Resource for handling operations to retrieving all users.
    """
    @marshal_with(full_resource_fields)
    def get(self):
        """
            Handle GET requests to retrieve all users.

            Returns:
                A list of all user objects.
        """
        with get_db() as db:
            all_users = db.query(User).all()
            return all_users
