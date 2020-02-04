from flask import Blueprint, request, jsonify, g
from .db import User, Course, Video
from .keys import SECRET
from .utils import checkpw
from .middleware.login import user_login_required
import bcrypt
import json
import jwt

user_courses_routes = Blueprint('user_courses_routes', __name__)

@user_courses_routes.route('/api/user/course/', methods=['POST'])
@user_login_required

def getcourses():
    try:
        user = User.objects(id=g.user['id']).first()
        return jsonify({"course": user.courses}), 200

    except:
        return jsonify({"error": "Something went wrong"}), 400