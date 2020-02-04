from flask import Blueprint, request, jsonify, g
from .db import Admin, Course, Video
from .keys import SECRET
from .utils import checkpw
from .middleware.login import admin_login_required
import bcrypt
import json
import jwt

admin_courses_routes = Blueprint('admin_courses_routes', __name__)

@admin_courses_routes.route('/api/admin/course/', methods=['POST'])
@admin_login_required

def getcourses():
    try:
        admin = Admin.objects(id=g.admin['id']).first()
        return jsonify({"course": admin.courses}), 200

    except:
        return jsonify({"error": "Something went wrong"}), 400