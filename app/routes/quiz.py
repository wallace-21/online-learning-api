from flask import Flask
from database import get_db
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from uuid import uuid4
from models.quiz import Quiz

quiz_post_args = reqparse.RequestParser()
quiz_post_args.add_argument("name", type=str, help="Fill in the name of the quiz", required=True)
quiz_post_args.add_argument("number_of_questions", type=int, help="Fill in the number of questions", required=True)
quiz_post_args.add_argument("topic", type=str, help="The topic of what  your quiz will forcus on", required=True)

quiz_update_args = reqparse.RequestParser()
quiz_update_args.add_argument("name", type=str, help="Fill in the name of the quiz")
quiz_update_args.add_argument("number_of_questions", type=int, help="Fill in the number of questions")
quiz_update_args.add_argument("topic", type=str, help="The topic of what  your quiz will forcus on")

resource_fields = {
        "id": fields.String,
        "name": fields.String,
        "number_of_questions": fields.Integer,
        "topic": fields.String
}


class QuizResource(Resource):

    @marshal_with(resource_fields)
    def post(self):
        args = quiz_post_args.parse_args()
        quiz = Quiz(id=str(uuid4()),
                    name=args["name"],
                    number_of_questions=args["number_of_questions"],
                    topic=args["topic"])

        with get_db() as db:
            db.add(quiz)
            db.commit()
            db.refresh(quiz)

        return quiz, 201

    @marshal_with(resource_fields)
    def get(self, quiz_name):
        with get_db() as db:
            quiz = db.query(Quiz).filter_by(name=quiz_name).first()
            if not quiz:
                abort(404, message="Quiz not found")

        return quiz, 201

    @marshal_with(resource_fields)
    def put(self, quiz_name):
        args = quiz_update_args.parse_args()

        with get_db() as db:
            quiz = db.query(Quiz).filter_by(id=quiz_name).first()
            if not quiz:
                abort(404, message="Quiz not found")

            if args["name"] is not None:
                quiz.name=args["name"]
            if args["number_of_questions"] is not None:
                quiz.number_of_questions=args["number_of_questions"]
            if args["topic"] is not None:
                quiz.topic=args["topic"]

            db.commit()
            db.refresh(quiz)

        return quiz, 201

    def delete(self, quiz_name):
        with get_db() as db:
            quiz = db.query(Quiz).filter_by(id=quiz_name).first()
            if not quiz:
                abort(404, message="Quiz not found")

            db.delete(quiz)
            db.commit()
        return {"message": "Quiz deleted"}, 201

class QuizzesResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        with get_db() as db:
            quizzes = db.query(Quiz).all()

            return quizzes, 201
