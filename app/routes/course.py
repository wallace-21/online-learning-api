from flask_restful import Api, Resource, reqparse, marshal_with, fields, abort
from database import get_db
from uuid import uuid4
from models.course import Course


course_post_args = reqparse.RequestParser()
course_post_args.add_argument("name", type=str, help="Enter name of the course", required=True)
course_post_args.add_argument("price", type=int, help="How much much does the course cost?", default=0)
course_post_args.add_argument("duration", type=str, help="How long does the the course take?", default="selfpace")
course_post_args.add_argument("description", type=str, help="description of the course")
course_post_args.add_argument("certification", type=bool, help="Does the course provide certification", default=False)

course_update_args = reqparse.RequestParser()
course_update_args.add_argument("name", type=str, help="Enter name of the course")
course_update_args.add_argument("price", type=int, help="How much much does the course cost?",)
course_update_args.add_argument("duration", type=str, help="How long does the the course take?")
course_update_args.add_argument("description", type=str, help="description of the course")
course_update_args.add_argument("certification", type=bool, help="Does the course provide certification")

resource_fields = {
        "id": fields.String,
        "name": fields.String,
        "price": fields.Integer,
        "duration": fields.String,
        "certification": fields.Boolean,
        "description": fields.String
}


class CourseResource(Resource):

    @marshal_with(resource_fields)
    def post(self):
        args = course_post_args.parse_args()
        course = Course(id=str(uuid4()),
                        name=args["name"],
                        price=args["price"],
                        duration=args["duration"],
                        certification=args["certification"],
                        description=args["description"])

        with get_db() as db:
            db.add(course)
            db.commit()
            db.refresh(course)
        return course, 201

    @marshal_with(resource_fields)
    def get(self, course_name):
        with get_db() as db:
            course = db.query(Course).filter_by(name=course_name).first()
            if not course:
                abort(404, message="Course not found")

            return course, 201

    @marshal_with(resource_fields)
    def put(self, course_name):
        args = course_update_args.parse_args()

        with get_db() as db:
            course = db.query(Course).filter_by(id=course_name).first()
            if not course:
                abort(404, message="Course not found")

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

    def delete(self, course_name):
        with get_db() as db:
            course = db.query(Course).filter_by(id=course_name).first()
            if not course:
                abort(404, message="course not found")

            db.delete(course)
            db.commit()

            return {"message": "Course deleted"}
class CoursesResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        with get_db() as db:
            courses = db.query(Course).all()
            return courses, 201
