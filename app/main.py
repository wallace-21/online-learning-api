from flask import Flask
from flask_restful import Api
from config import Config
from database import Base, engine, get_db
from models.user import User
from routes.user import UserResource, UsersResource
from routes.course import CourseResource, CoursesResource
from routes.quiz import QuizResource, QuizzesResource, CourseQuizzesResource
from routes.assignment import AssignmentResource, AssignmentsResource, CourseAssignmentResource
from routes.lecture import LectureResource, LecturesResource, CourseLectureResource
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
api = Api(app)

# Initialize database
Base.metadata.create_all(bind=engine)

    
# Register resources
# User endpoints
api.add_resource(UserResource, "/user", "/user/<string:user_id>")
api.add_resource(UsersResource, "/users")

# Course endpoints
api.add_resource(CourseResource, "/course", "/course/<int:course_id>")
api.add_resource(CoursesResource, "/courses")

#Quiz endpoints
api.add_resource(QuizResource, "/quiz", "/quiz/<int:quiz_id>")
api.add_resource(QuizzesResource, "/quizzes")
api.add_resource(CourseQuizzesResource, "/course/<int:course_id>/quizzes")

# Assignment endpoints
api.add_resource(AssignmentResource, "/assignment", "/assignment/<int:assignment_id>")
api.add_resource(AssignmentsResource, "/assignments")
api.add_resource(CourseAssignmentResource, "/course/<int:course_id>/assignments")

# Lecture endpoints
api.add_resource(LectureResource, "/lecture", "/lecture/<int:lecture_id>")
api.add_resource(LecturesResource, "/lectures")
api.add_resource(CourseLectureResource, "/course/<int:course_id>/lectures")

if __name__ == "__main__":
    app.run(debug=True)
