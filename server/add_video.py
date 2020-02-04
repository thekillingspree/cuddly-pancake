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

        course.videos.append(video)
        course.save()
        return video.to_json(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@video_routes.route('/api/course/videoinfo', methods=['GET'])
def get_info():
    try:
        course = Course.objects(id=request.json['cid']).first()
        video = Video.objects(id=request.json['vid'], course=course).first()
        return video.to_json(), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 400


@video_routes.route('/api/course/allvideos', methods=['GET', 'POST'])
def get_all_videos_course():
    try:
        course = Course.objects(id=request.json['cid']).first()
        allvids = [json.loads(v.to_json()) for v in course.videos]
        return jsonify(allvids), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 400

@video_routes.route('/api/course/videoviews', methods=['POST'])
def updateViews():
    try:
        video = Video.objects(id=request.json['vid']).first()
        video.views = video.views + 1
        video.save()
        return jsonify({'result': 'SUCCESS'}), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 400


