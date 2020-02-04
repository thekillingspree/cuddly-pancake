from flask import Flask, request, jsonify
from flask_cors import CORS
from .admin import admin_routes
from .user import user_routes
from .rooms import room_routes
from .course import course_routes
from .admin_all_courses import admin_courses_routes
from .admin_video_info import admin_videos_routes
from .user_all_courses import user_courses_routes
from .user_video_info import user_videos_routes

app = Flask(__name__)
#CORS - Cross Origin Resource Sharing - This needs to be enabled to use our API/server with our app/website since the server the client will have different origins.
CORS(app)

app.register_blueprint(admin_routes)
app.register_blueprint(user_routes)
app.register_blueprint(course_routes)
app.register_blueprint(admin_courses_routes)
app.register_blueprint(admin_videos_routes)
app.register_blueprint(user_courses_routes)
app.register_blueprint(user_videos_routes)

if __name__ == '__main__':
    app.run(debug=True)