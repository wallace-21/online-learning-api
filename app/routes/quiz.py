#!/usr/bin/python3

"""
    imports necessary for the program to run
"""

from flask import Flask
from database import get_db
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from uuid import uuid4
from models.quiz import Quiz


# Parser for POST request arguments (creates)
quiz_post_args = reqparse.RequestParser()
quiz_post_args.add_argument("name", type=str,
                            help="Fill in the name of the quiz", required=True)
quiz_post_args.add_argument("number_of_questions",
                            type=int, help="Fill in the number of questions",
                            required=True)
quiz_post_args.add_argument("topic", type=str,
                            help="The topic of what  your quiz will forcus on",
                            required=True)


# Parser for PUT request arguments (updates)
quiz_update_args = reqparse.RequestParser()
quiz_update_args.add_argument("name", type=str,
                              help="Fill in the name of the quiz")
quiz_update_args.add_argument("number_of_questions",
                              type=int, help="Fill in the number of questions")
quiz_update_args.add_argument("topic", type=str,
                              help="Topic of what your quiz will forcus on")

# Fields for marshalling the Quiz model
resource_fields = {
        "id": fields.String,
        "name": fields.String,
        "number_of_questions": fields.Integer,
        "topic": fields.String
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
        quiz = Quiz(id=str(uuid4()),
                    name=args["name"],
                    number_of_questions=args["number_of_questions"],
                    topic=args["topic"])

        with get_db() as db:
            db.add(quiz)
            # Commit the transaction to save changes
            db.commit()
            # Refresh the user instance to ensure all
            db.refresh(quiz)

        return quiz, 201

    @marshal_with(resource_fields)
    def get(self, quiz_name):
        """
            Handle GET requests to retrieve a quiz by name.

            Args:
                quiz_name (str): The name of the quiz to retrieve.

            Returns:
                The quiz object if found, or a 404 error
                if the quiz does not exist.
        """
        with get_db() as db:
            # Query the user by Name
            quiz = db.query(Quiz).filter_by(name=quiz_name).first()
            if not quiz:
                abort(404, message="Quiz not found")

        return quiz, 201

    @marshal_with(resource_fields)
    def put(self, quiz_name):
        """
            Update an existing quiz's details.

            Args:
                course_name (str): The name of the quiz to update.

            Returns:
                The updated quiz object and HTTP status code 201.
        """

        args = quiz_update_args.parse_args()

        with get_db() as db:
            # Query the user by ID
            quiz = db.query(Quiz).filter_by(id=quiz_name).first()
            if not quiz:
                abort(404, message="Quiz not found")

            # Update fields if provided
            if args["name"] is not None:
                quiz.name = args["name"]
            if args["number_of_questions"] is not None:
                quiz.number_of_questions = args["number_of_questions"]
            if args["topic"] is not None:
                quiz.topic = args["topic"]

            db.commit()
            # Commit the transaction to save changes
            db.refresh(quiz)

        return quiz, 201

    def delete(self, quiz_name):
        """ Delete an existing course.

            Args:
                course_name (str): The ID of the quiz to delete.

            Raises:
                404: If the course is not found.

            Returns:
                dict: A message confirming the quiz has been deleted.
        """

        with get_db() as db:
            # Query the user by ID
            quiz = db.query(Quiz).filter_by(id=quiz_name).first()
            if not quiz:
                abort(404, message="Quiz not found")

            db.delete(quiz)
            # Commit the transaction to save changes of the deleted quiz
            db.commit()
        return {"message": "Quiz deleted"}, 201


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

            return quizzes, 201
