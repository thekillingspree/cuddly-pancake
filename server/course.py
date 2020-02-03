from flask import Blueprint, request, jsonify, g
from .db import Admin, User, Course
from .keys import SECRET
from .middleware.login import *
import json
import jwt

course_routes = Blueprint('course_routes', __name__)


@course_routes.route('/api/course/new', methods=['POST'])
@admin_login_required
def create():
    try:
        admin = Admin.objects(id=g.admin['id']).first()
        name = request.json['name']
        imageURL = request.json['imageURL']
        description = request.json['description']
        for course in admin.courses:
            if course.name == name:
                raise Exception('You have already created a course with name as \'{}\''.format(name))
        course = Course(name=name, imageURL=imageURL, description=description)
        course.save()
        admin.courses.append(course)
        admin.save()
        return course.to_json(), 200
    except KeyError:
        return jsonify({'error': 'Please provide all fields'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# @course_routes.route('/api/rooms/view', methods=['GET'])
# @admin_login_required
# @admin_is_authorized
# def viewroom():
#     try:
#         admin = Admin.objects(id=g.admin['id']).first()
#         cid = request.args.get('cid')
#         if not rid:
#             raise Exception('Please provide room id.')
#         room = Room.objects(id=rid).first()
#         res = json.loads(room.to_json())
#         res['entrylist'] = []
#         for entry in room.entrylist:
#             u = entry.user
#             d = json.loads(entry.to_json())
#             d['user'] = {'fullname': u.fullname, 'tecid': u.tecid}
#             res['entrylist'].append(d)
#         return jsonify(res), 200
#     except KeyError:
#         return jsonify({'error': 'Please provide all fields'}), 400
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400
