#!/usr/bin/python3

"""
    Imports necessary for the program to run
"""

from flask import Flask
from database import get_db
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from models.lecture import Lecture
from models.course import Course
from datetime import datetime


# Custom function to parse datetime
def valid_date(s):
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        raise ValueError(f"Not a valid date: '{s}'.")


# Parser/args for POST request arguments (creates)
lecture_post_args = reqparse.RequestParser()
lecture_post_args.add_argument(
    "name",
    type=str,
    help="Fill in the name of the assignment",
    required=True
)
lecture_post_args.add_argument(
    "date_and_time",
    type=valid_date,
    help="Fill in the date and time of the lecture (format: YYYY-MM-DD HH:MM)"
)
lecture_post_args.add_argument(
    "mentors",
    type=str,
    help="Who's gonna lead/teach in the lecture",
    required=True
)
lecture_post_args.add_argument(
    "duration",
    type=int,
    help="How long is the lecture",
    required=True
)
lecture_post_args.add_argument(
    "course_id",
    type=int,
    help="Course ID associated with lecture.",
    required=True
)

# Parser/args for PUT request arguments (updates)
lecture_update_args = reqparse.RequestParser()
lecture_update_args.add_argument(
    "name",
    type=str,
    help="Fill in the name of the assignment"
)
lecture_update_args.add_argument(
    "date_and_time",
    type=valid_date,
    help="Fill in the date and time of the lecture (format: YYYY-MM-DD HH:MM)"
)
lecture_update_args.add_argument(
    "mentors",
    type=str,
    help="Who's gonna lead/teach in the lecture"
)
lecture_update_args.add_argument(
    "duration",
    type=int,
    help="How long is the lecture"
)
lecture_update_args.add_argument(
    "course_id",
    type=int,
    help="Course ID associated with lecture."
)

# Fields for marshalling the Assignment model
resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "date_and_time": fields.DateTime,
    "mentors": fields.String,
    "duration": fields.Integer,
    "course_id": fields.Integer,
    "created_date": fields.DateTime
}


class LectureResource(Resource):
    """
        Resource for handling individual lecture operations,
        such as creating, updating and retrieving lecture.
    """
    @marshal_with(resource_fields)
    def post(self):
        """
            Handle POST requests to create a new lecture.

            Parses the request arguments, creates a new lecture,
            and saves it to the database.

            Returns:
                The created lecture object and a 201 status code.
        """

        args = lecture_post_args.parse_args()
        lecture = Lecture(
            name=args["name"],
            date_and_time=args["date_and_time"],
            mentors=args["mentors"],
            duration=args["duration"],
            course_id=args["course_id"])

        with get_db() as db:
            db.add(lecture)
            db.commit()
            db.refresh(lecture)

        return lecture, 201

    @marshal_with(resource_fields)
    def get(self, lecture_id):
        """
            Handle GET requests to retrieve lecture by ID.

            Args:
                lecture_id (int): The ID of the lecture to retrieve.

            Returns:
                The lecture object if found, or a 404 error
                if the lecture does not exist.
        """

        with get_db() as db:
            lecture = db.query(Lecture).filter_by(id=lecture_id).first()
            if not lecture:
                abort(404, message="lecture not found")

        return lecture, 200

    @marshal_with(resource_fields)
    def put(self, lecture_id):
        """
            Update an existing lecture's details.

            Args:
                lecture_id (int): The name of the lecture to update.

            Returns:
                The updated lecture object and HTTP status code 201.
        """
        args = lecture_update_args.parse_args()

        with get_db() as db:
            lecture = db.query(Lecture).filter_by(id=lecture_id).first()
            if not lecture:
                abort(404, message="lecture not found")

            if args["name"] is not None:
                abort(400, message="Updating 'name' is not allowed")
            if args["course_id"] is not None:
                abort(400, message="Updating 'course_id' is not allowed")

            if args["date_and_time"] is not None:
                lecture.date_and_time = args["date_and_time"]
            if args["duration"] is not None:
                lecture.duration = args["duration"]
            if args["mentors"] is not None:
                lecture.mentors = args["mentors"]

            db.commit()
            db.refresh(lecture)

        return lecture, 200

    def delete(self, lecture_id):
        """ Delete an existing lecture.

            Args:
                lecture_id (int): The ID of the lecture to delete.

            Raises:
                404: If the lecture is not found.

            Returns:
                dict: A message confirming the lecture has been deleted.
        """

        with get_db() as db:
            lecture = db.query(Lecture).filter_by(id=lecture_id).first()
            if not lecture:
                abort(404, message="Quiz not found")

            db.delete(lecture)
            db.commit()
        return {"message": "Lecture deleted"}, 200


class LecturesResource(Resource):
    """
        Resource for handling operations to retrieving all lectures.
    """
    @marshal_with(resource_fields)
    def get(self):
        """
            Handle GET requests to retrieve all lectures.

            Returns:
                A list of all lectures objects.
        """
        with get_db() as db:
            lecture = db.query(Lecture).all()
        return lecture, 200


class CourseLectureResource(Resource):
    """
        Resource for handling operations to retrieve lecture by course ID.
    """

    @marshal_with(resource_fields)
    def get(self, course_id):
        """
            Retrieves all lecture associated with a given course ID.

            Args:
                lecture_id (int): The ID of the course for
                which lecture are to be retrieved.

            Returns:
                A list of lectures associated with the given course ID.
                A tuple containing the list of lectures
        """
        with get_db() as db:
            course = db.query(Course).filter_by(id=course_id).first()
            if not course:
                abort(404, message="Course not found")

            lectures = db.query(Lecture).filter_by(course_id=course_id).all()
        return lectures, 200
