from flask import Blueprint, request, jsonify, g
from .db import Video
from .keys import SECRET
from .utils import checkpw
from .middleware.login import user_login_required
import bcrypt
import json
import jwt

user_videos_routes = Blueprint('user_videos_routes', __name__)

@user_videos_routes.route('/api/user/course/video-info', methods=['POST'])
@user_login_required

def get_info():
    try:
        course = Course.objects(id=req.json['cid']).first()
        video = Video.objects(id=req.json['vid'], course=course).first()
        return jsonify({"video":video}), 200
    except:
        return jsonify({"error":"Something went wrong"}), 400