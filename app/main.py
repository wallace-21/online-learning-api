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
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
api = Api(app)

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Online Learning API"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)

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
