from flask import Blueprint, request, jsonify, g
from .db import Admin, Course, Video
from .keys import SECRET
from .utils import checkpw
from .middleware.login import admin_login_required, admin_is_authorized
import bcrypt
import json
import jwt

video_routes = Blueprint('video_routes', __name__)

@video_routes.route('/api/admin/add-video', methods=['POST'])
@admin_login_required
@admin_is_authorized

def addvideo():
    try:
        name = request.json['name']
        course = request.json['course']
        url = request.json['url']
        if not Course.objects(course=course):
            return jsonify({"error": "Course not found"}), 400
        admin = Admin.objects(id=g.admin['id']).first()
        if not course in admin.courses:
            return jsonify({"error": "Invalid admin access"}), 400


        video = Video(name=name, course=course, url=url)
        video.save()
    except:
        return jsonify({"error": "Something went wrong"}), 400