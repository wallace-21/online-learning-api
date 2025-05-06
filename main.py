# Flask modules
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

# Database
from app.config import Config
from app.models.user import User
#from app.models.enrollment import Enrollment
from app.utils.db import Base, engine, get_db

#routes/endpoints
from app.routes.user_routes import SignupResource, LoginResource, UserResource


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
api = Api(app)


# Initialize database
Base.metadata.create_all(bind=engine)


# Register resources
# User endpoints
api.add_resource(SignupResource, "/api/auth/signup")
api.add_resource(LoginResource, "/api/auth/login")
api.add_resource(UserResource, "/api/auth/user")


if __name__ == "__main__":
    app.run(debug=True)
