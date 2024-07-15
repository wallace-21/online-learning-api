#!/usr/bin/python3

"""
    Imports necessary for the program to run
"""

from flask import Flask
from database import get_db
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from models.quiz import Quiz
from models.course import Course

# Parser for POST request arguments (creates)
quiz_post_args = reqparse.RequestParser()
quiz_post_args.add_argument("name", type=str, help="Fill in the name of the quiz", required=True)
quiz_post_args.add_argument("number_of_questions", type=int, help="Fill in the number of questions", required=True)
quiz_post_args.add_argument("topic", type=str, help="The topic of what your quiz will focus on", required=True)
quiz_post_args.add_argument("course_id", type=int, help="What's the ID of the linked course", required=True)

# Parser for PUT request arguments (updates)
quiz_update_args = reqparse.RequestParser()
quiz_update_args.add_argument("name", type=str, help="Fill in the name of the quiz")
quiz_update_args.add_argument("number_of_questions", type=int, help="Fill in the number of questions")
quiz_update_args.add_argument("topic", type=str, help="Topic of what your quiz will focus on")
quiz_update_args.add_argument("course_id", type=int, help="ID to the linked course")

# Fields for marshalling the Quiz model
resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "number_of_questions": fields.Integer,
    "topic": fields.String,
    "course_id": fields.Integer
}


class QuizResource(Resource):
    """
        Resource for handling individual quiz operations,
        such as creating, updating and retrieving quizzes.
    """
    @marshal_with(resource_fields)
    def post(self):
        """
            Handle POST requests to create a new quiz.

            Parses the request arguments, creates a new quiz,
            and saves it to the database.

            Returns:
                The created quiz object and a 201 status code.
        """

        args = quiz_post_args.parse_args()
        quiz = Quiz(
            name=args["name"],
            number_of_questions=args["number_of_questions"],
            topic=args["topic"],
            course_id=args["course_id"])

        with get_db() as db:
            db.add(quiz)
            db.commit()
            db.refresh(quiz)

        return quiz, 201

    @marshal_with(resource_fields)
    def get(self, quiz_id):
        """
            Handle GET requests to retrieve a quiz by name.

            Args:
                quiz_name (str): The name of the quiz to retrieve.

            Returns:
                The quiz object if found, or a 404 error
                if the quiz does not exist.
        """

        with get_db() as db:
            quiz = db.query(Quiz).filter_by(id=quiz_id).first()
            if not quiz:
                abort(404, message="Quiz not found")

        return quiz, 200

    @marshal_with(resource_fields)
    def put(self, quiz_id):
        """
            Update an existing quiz's details.

            Args:
                course_name (str): The name of the quiz to update.

            Returns:
                The updated quiz object and HTTP status code 201.
        """
        args = quiz_update_args.parse_args()

        with get_db() as db:
            quiz = db.query(Quiz).filter_by(id=quiz_id).first()
            if not quiz:
                abort(404, message="Quiz not found")

            if args["course_id"] is not None:
                abort(400, message="Updating 'course_id' is not allowed")

            if args["name"] is not None:
                quiz.name = args["name"]
            if args["number_of_questions"] is not None:
                quiz.number_of_questions = args["number_of_questions"]
            if args["topic"] is not None:
                quiz.topic = args["topic"]

            db.commit()
            db.refresh(quiz)

        return quiz, 200

    def delete(self, quiz_id):
        """ Delete an existing course.

            Args:
                course_name (str): The ID of the quiz to delete.

            Raises:
                404: If the course is not found.

            Returns:
                dict: A message confirming the quiz has been deleted.
        """

        with get_db() as db:
            quiz = db.query(Quiz).filter_by(id=quiz_id).first()
            if not quiz:
                abort(404, message="Quiz not found")

            db.delete(quiz)
            db.commit()
        return {"message": "Quiz deleted"}, 200


class QuizzesResource(Resource):
    """
        Resource for handling operations to retrieving all quizzes.
    """
    @marshal_with(resource_fields)
    def get(self):
        """
            Handle GET requests to retrieve all quizzes.

            Returns:
                A list of all quizzes objects.
        """
        with get_db() as db:
            quizzes = db.query(Quiz).all()
        return quizzes, 200


class CourseQuizzesResource(Resource):
    """
        Resource for handling operations to retrieve quizzes by course ID.
    """

    @marshal_with(resource_fields)
    def get(self, course_id):
        """
            Retrieves all quizzes associated with a given course ID.

            Args:
                course_id (int): The ID of the course for which quizzes are to be retrieved.

            Returns:
                A list of quizzes associated with the given course ID.
                A tuple containing the list of quizzes
        """
        with get_db() as db:
            course = db.query(Course).filter_by(id=course_id).first()
            if not course:
                abort(404, message="Course not found")
            
            quizzes = db.query(Quiz).filter_by(course_id=course_id).all()
        return quizzes, 200
