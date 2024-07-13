#!/usr/bin/python3

"""
    imports necessery for the program to run
"""

from flask_restful import Api, Resource, reqparse, marshal_with, fields, abort
from database import get_db
from uuid import uuid4
from models.course import Course

# Parser for POST request arguments (creates)
course_post_args = reqparse.RequestParser()
course_post_args.add_argument("name", type=str,
                              help="Enter name of the course", required=True)
course_post_args.add_argument("price", type=int,
                              help="How much much does the course cost?",
                              default=0)
course_post_args.add_argument("duration", type=str,
                              help="How long does the the course take?")
course_post_args.add_argument("description", type=str,
                              help="description of the course")
course_post_args.add_argument("certification", type=bool,
                              help="Does the course provide certification",
                              default=False)
course_post_args.add_argument("language", type=str,
                              help="The language in which the course is conducted.",
                              required=True)
course_post_args.add_argument("tags", type=str,
                              help="Tasgs or categories associated with the course.",
                              required=True)
course_post_args.add_argument("max_students", type=int,
                              help="Maximum number of students allowed to enroll in the course.",
                              required=True)

# Parser for PUT request arguments (updates)
course_update_args = reqparse.RequestParser()
course_update_args.add_argument("name", type=str,
                                help="Enter name of the course")
course_update_args.add_argument("price", type=int,
                                help="How much much does the course cost?",)
course_update_args.add_argument("duration", type=str,
                                help="How long does the the course take?")
course_update_args.add_argument("description", type=str,
                                help="description of the course")
course_update_args.add_argument("certification", type=bool,
                                help="Does the course provide certification")
course_update_args.add_argument("language",
                                help="The language in which the course is conducted.")
course_update_args.add_argument("tags",
                                help="Tasgs or categories associated with the course.")
course_update_args.add_argument("max_students",
                                help="Maximum number of students allowed to enroll in the course.")
# Fields for marshalling the Course model
resource_fields = {
        "id": fields.Integer,
        "name": fields.String,
        "language": fields.String,
        "price": fields.Integer,
        "duration": fields.String,
        "certification": fields.Boolean,
        "max_students": fields.Integer,
        "tags": fields.String,
        "description": fields.String
}


class CourseResource(Resource):
    """
        Resource for handling individual course operations,
        such as creating and retrieving courses.
    """

    @marshal_with(resource_fields)
    def post(self):
        """
            Handle POST requests to create a new course.

            Parses the request arguments, creates a new course,
            and saves it to the database.

            Returns:
                The created course object and a 201 status code.
        """
        args = course_post_args.parse_args()
        course = Course(name=args["name"],
                        price=args["price"],
                        duration=args["duration"],
                        certification=args["certification"],
                        language=args["language"],
                        tags=args["tags"],
                        max_students=args["max_students"],
                        description=args["description"])

        with get_db() as db:
            db.add(course)
            db.commit()
            db.refresh(course)
        return course, 201

    @marshal_with(resource_fields)
    def get(self, course_id):
        """
            Handle GET requests to retrieve a user by ID.

            Args:
                course_id (str): The name of the course to retrieve.

            Returns:
                The course object if found, or a 404 error
                if the course does not exist.
        """
        with get_db() as db:
            course = db.query(Course).filter_by(id=course_id).first()
            if not course:
                abort(404, message="Course not found")

            return course, 201

    @marshal_with(resource_fields)
    def put(self, course_id):
        """
            Update an existing user's details.

            Args:
                course_id (str): The name of the course to update.

            Returns:
                The updated course object and HTTP status code 201.
            """
        args = course_update_args.parse_args()

        with get_db() as db:
            course = db.query(Course).filter_by(id=course_id).first()
            if not course:
                abort(404, message="Course not found")

            if args["certification"] is not None:
                abort(400, message="Updating 'certification' is not allowed")

            if args["certification"] is None:
                course.certification = True

            if args["tags"] is not None:
                course.tags = args["tags"]
            if args["max_students"] is not None:
                course.max_students = args["max_students"]
            if args["name"] is not None:
                course.name = args["name"]
            if args["price"] is not None:
                course.price = args["price"]
            if args["duration"] is not None:
                course.duration = args["duration"]
            if args["description"] is not None:
                course.description = args["description"]

            db.commit()
            db.refresh(course)

            return course, 201

    def delete(self, course_id):
        """ Delete an existing course.

            Args:
                course_id (str): The ID of the user to delete.

            Raises:
                404: If the course is not found.

            Returns:
                dict: A message confirming the course has been deleted.
        """
        with get_db() as db:
            course = db.query(Course).filter_by(id=course_id).first()
            if not course:
                abort(404, message="course not found")

            db.delete(course)
            db.commit()

            return {"message": "Course deleted"}


class CoursesResource(Resource):
    """
        Resource for handling operations to retrieving all users.
    """

    @marshal_with(resource_fields)
    def get(self):
        """
            Handle GET requests to retrieve all courses.

            Returns:
                A list of all course objects.
        """
        with get_db() as db:
            courses = db.query(Course).all()

            return courses, 201
