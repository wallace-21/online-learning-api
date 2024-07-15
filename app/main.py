from flask import Flask
from flask_restful import Api
from config import Config
from database import Base, engine, get_db
from models.user import User
from routes.user import UserResource, UsersResource
from routes.course import CourseResource, CoursesResource
from routes.quiz import QuizResource, QuizzesResource, CourseQuizzesResource
app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)

"""
    Initialize database
"""
Base.metadata.create_all(bind=engine)

"""
    Register resources
"""
api.add_resource(UserResource, "/user", "/user/<string:user_id>")
api.add_resource(UsersResource, "/users")
api.add_resource(CourseResource, "/course", "/course/<int:course_id>")
api.add_resource(CoursesResource, "/courses")
api.add_resource(QuizResource, "/quiz", "/quiz/<int:quiz_id>")
api.add_resource(QuizzesResource, "/quizzes")
api.add_resource(CourseQuizzesResource, "/course/<int:course_id>/quizzes")

if __name__ == "__main__":
    app.run(debug=True)
