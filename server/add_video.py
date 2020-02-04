from flask import Blueprint, request, jsonify, g
from .db import Admin, Course, Video
from .keys import SECRET
from .utils import checkpw
from .middleware.login import admin_login_required, admin_is_authorized
import bcrypt
import json
import jwt

video_routes = Blueprint('video_routes', __name__)

@video_routes.route('/api/course/addvideo', methods=['POST'])
@admin_login_required
@admin_is_authorized
def addvideo():
    try:
        name = request.json['name']
        course = Course.objects(id=request.json['cid']).first()
        url = request.json['url']
        if not course:
            return jsonify({"error": "Course not found"}), 400
        
        video = Video(name=name, course=course, url=url)
        # video.course = course
        video.save()
        return video.to_json(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400