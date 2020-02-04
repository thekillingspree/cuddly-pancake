from flask import Blueprint, request, jsonify, g
from .db import Video
from .keys import SECRET
from .utils import checkpw
from .middleware.login import admin_login_required
import bcrypt
import json
import jwt

admin_videos_routes = Blueprint('admin_videos_routes', __name__)

@admin_videos_routes.route('/api/admin/course/video-info', methods=['POST'])
@admin_login_required

def get_info():
    try:
        video = Video.objects(id=g.video['id']).first()
        return jsonify({"video":video}), 200
    except:
        return jsonify({"error":"Something went wrong"}), 400