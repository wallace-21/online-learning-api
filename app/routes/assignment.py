#!/usr/bin/python3

"""
    Imports necessary for the program to run
"""

from flask import Flask
from database import get_db
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from models.assignment import Assignment
from models.course import Course


# Custom function to parse datetime
def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError(f"Not a valid date: '{s}'.")

# Parser/args for POST request arguments (creates)
assignment_post_args = reqparse.RequestParser()
assignment_post_args.add_argument("name", type=str, help="Fill in the name of the assignment", required=True)
assignment_post_args.add_argument("release_date", type=valid_date, help="Fill in the release date (format: YYYY-MM-DD HH:MM)", required=True)
assignment_post_args.add_argument("due_date", type=valid_date, help="Fill in the due date (format: YYYY-MM-DD HH:MM)", required=True)
assignment_post_args.add_argument("course_id", type=int, help="What's the ID of the linked course", required=True)
assignment_post_args.add_argument("description", type=str, help="The description of the assignment", required=True)
assignment_post_args.add_argument("max_marks", type=int, help="The maximum marks for the assignment", required=True)
assignment_post_args.add_argument("submission_type", type=str, help="The type of submission required", required=True)


# Parser/args for PUT request arguments (updates)
assignment_update_args = reqparse.RequestParser()
assignment_update_args.add_argument("name", type=str, help="Fill in the name of the assignment")
assignment_update_args.add_argument("release_date", type=valid_date, help="Fill in the release date (format: YYYY-MM-DD HH:MM:SS)")
assignment_update_args.add_argument("due_date", type=valid_date, help="Fill in the due date (format: YYYY-MM-DD HH:MM:SS)")
assignment_update_args.add_argument("course_id", type=int, help="What's the ID of the linked course")
assignment_update_args.add_argument("description", type=str, help="The description of the assignment")
assignment_update_args.add_argument("max_marks", type=int, help="The maximum marks for the assignment")
assignment_update_args.add_argument("submission_type", type=str, help="The type of submission required")


# Fields for marshalling the Assignment model
resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "release_date": fields.DateTime,
    "due_date": fields.DateTime,
    "course_id": fields.Integer,
    "description": fields.String,
    "max_marks": fields.Integer,
    "submission_type": fields.String,
}


class AssignmentResource(Resource):
    """
        Resource for handling individual assignment operations,
        such as creating, updating and retrieving assignments.
    """
    @marshal_with(resource_fields)
    def post(self):
        """
            Handle POST requests to create a new assignment.

            Parses the request arguments, creates a new assignment,
            and saves it to the database.

            Returns:
                The created assgnment object and a 201 status code.
        """

        args = assignment_post_args.parse_args()
        assignment = Assignment(
            name=args["name"],
            release_date=args["release_date"],
            due_date=args["due_date"],
            course_id=args["course_id"],
            description=args["description"],
            max_marks=args["max_marks"],
            submission_type=args["submission_type"])

        with get_db() as db:
            db.add(assignment)
            db.commit()
            db.refresh(assignment)

        return assignment, 201

    @marshal_with(resource_fields)
    def get(self, assignment_id):
        """
            Handle GET requests to retrieve a assignment by ID.

            Args:
                assignment_id (int): The ID of the assignment to retrieve.

            Returns:
                The assignment object if found, or a 404 error
                if the assignment does not exist.
        """

        with get_db() as db:
            assignment = db.query(Assignment).filter_by(id=assignment_id).first()
            if not assignment:
                abort(404, message="Assignment not found")

        return assignment, 200

    @marshal_with(resource_fields)
    def put(self, assignment_id):
        """
            Update an existing assignment's details.

            Args:
                assignment_id (int): The name of the assignment to update.

            Returns:
                The updated assignment object and HTTP status code 201.
        """
        args = assignment_update_args.parse_args()

        with get_db() as db:
            assignment = db.query(Assignment).filter_by(id=assignment_id).first()
            if not assignment:
                abort(404, message="Assignment not found")

            if args["name"] is not None:
                abort(400, message="Updating 'name' is not allowed")
            if args["course_id"] is not None:
                abort(400, message="Updating 'course_id' is not allowed")
            if args["release_date"] is not None:
                abort(400, message="Can't update 'release_datei'")

            if args["due_date"] is not None:
                assignment.due_date = args["due_date"]
            if args["description"] is not None:
                assignment.description = args["description"]
            if args["max_marks"] is not None:
                assignment.max_marks = args["max_marks"]

            db.commit()
            db.refresh(assignment)

        return assignment, 200

    def delete(self, assignment_id):
        """ Delete an existing assignment.

            Args:
                assignment (int): The ID of the assignment to delete.

            Raises:
                404: If the assignment is not found.

            Returns:
                dict: A message confirming the assignment has been deleted.
        """

        with get_db() as db:
            assignment= db.query(Assignment).filter_by(id=assignment_id).first()
            if not assignment:
                abort(404, message="Quiz not found")

            db.delete(assignment)
            db.commit()
        return {"message": "Assignment deleted"}, 200


class AssignmentsResource(Resource):
    """
        Resource for handling operations to retrieving all assignments.
    """
    @marshal_with(resource_fields)
    def get(self):
        """
            Handle GET requests to retrieve all assignments.

            Returns:
                A list of all assignments objects.
        """
        with get_db() as db:
            assignments = db.query(Assignment).all()
        return assignments, 200


class CourseAssignmentResource(Resource):
    """
        Resource for handling operations to retrieve assignment by course ID.
    """

    @marshal_with(resource_fields)
    def get(self, course_id):
        """
            Retrieves all assignment associated with a given course ID.

            Args:
                assignment_id (int): The ID of the course for which assignments are to be retrieved.

            Returns:
                A list of assignments associated with the given course ID.
                A tuple containing the list of assignments
        """
        with get_db() as db:
            course = db.query(Course).filter_by(id=course_id).first()
            if not course:
                abort(404, message="Course not found")

            assignments = db.query(Assignment).filter_by(course_id=course_id).all()
        return assignments, 200
