from flask import Blueprint, request, jsonify, g
from mongoengine.errors import ValidationError, NotUniqueError
import bcrypt
import jwt
import json
import time
import re

from .middleware.login import user_login_required, user_is_authorized
from .db import User, Course
from .keys import SECRET
from .utils import checkpw

user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/api/users/signup', methods=['POST'])
def signin():
    try:
        username = request.json['username']
        fullname = request.json['fullname']
        email = request.json['email']
        if User.objects(username=username).first():
            raise Exception('Username already taken.')
        if User.objects(email=email).first():
            raise Exception('Email has been already registered.')
        unhashed = request.json['password']
        if not checkpw(unhashed):
            raise Exception('Password must be at least 6 characters long and must contain a number.')
        password = bcrypt.hashpw(unhashed.encode(), bcrypt.gensalt())
        user = User(username=username, fullname=fullname, email=email, password=password)
        user.save()
        token = jwt.encode({'id': str(user.id), 'username': user.username, 'fullname': user.fullname, 'email': user.email}, SECRET, algorithm='HS256')
        userdict = json.loads(user.to_json())
        del userdict['password']
        return jsonify({'result': userdict , 'token': token.decode()}), 200
    except KeyError:
        return jsonify({'error': 'Please provide all the required fields'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@user_routes.route('/api/users/login', methods=['POST'])
def login():
    try:
        username = request.json['username']
        password = request.json['password']
        user = User.objects(username=username).first()
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            userdict = json.loads(user.to_json())
            del userdict['password']        
            token = jwt.encode({'id': str(user.id), 'username': user.username, 'fullname': user.fullname, 'email': user.email}, SECRET, algorithm='HS256')
            return jsonify({'result': userdict, 'token': token.decode()}), 200
        else:
            raise Exception('Username or password Incorrect') 

    except KeyError:
        return jsonify({'error': 'Please provide all the required fields'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@user_routes.route('/api/users/profile', methods=['GET'])
@user_login_required
@user_is_authorized
def profile():
    try:
        user = User.objects(id=g.user['id']).first()
        if not user:
            raise Exception('User not found.')
        userdict = json.loads(user.to_json())
        del userdict['password']
        userdict['history'] = []
        if user.current_course:
            cd = json.loads(user.current_course.to_json())
            userdict['current_course'] = cd
        for entry in user.enrolled:
            ed = json.loads(entry.to_json())
            userdict['history'].append(ed)
        return jsonify(userdict), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_routes.route('/api/users/enroll', methods=['POST'])
@user_login_required
@user_is_authorized
def enter():
    
    try:
        cid = request.json['id']
        course = Course.objects(id=cid).first()
        user = User.objects(id=g.user['id']).first() 
        if not user:
            raise Exception("Please Signup first.")
        if not course:
            raise Exception('Invalid Course id')
        if user.current_course and user.current_course == course:
            raise Exception('You have already enrolled to this course.')
        user.current_course = course
        course.enrolled_num = course.enrolled_num + 1
        user.enrolled.append(course)
        #TODO: Decide whether to add room to history on entering or after entring
        user.save()
        course.save()
        return jsonify({'result': 'SUCCESS'}), 200
    except KeyError:
        return jsonify({'error': 'id and uid is required.'}), 400
    except ValidationError:
        return jsonify({'error': 'Please provide a valid id'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_routes.route('/api/users/enrolled', methods=['GET'])
@user_login_required
@user_is_authorized
def enrolled():
    
    try:
        user = User.objects(id=g.user['id']).first() 
        if not user:
            raise Exception("Please Signup first.")
        enrolled_courses = []
        for course in user.enrolled:
            enrolled_courses.append(json.loads(course.to_json()))
        return jsonify(enrolled_courses), 200
    except KeyError:
        return jsonify({'error': 'id and uid is required.'}), 400
    except ValidationError:
        return jsonify({'error': 'Please provide a valid id'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_routes.route('/api/users/completed', methods=['POST'])
@user_login_required
@user_is_authorized
def uexit():
    '''
    Route to record exits. This helps in storing the exit time of a user.
    Also helps in providing insights on how much time an user spends inside the room on average.
    Requires two fields, id and uid, which have the same meaning as the above /entry route.
    '''
    try:
        cid = request.json['id']
        course = Course.objects(id=cid).first()
        user = User.objects(id=g.user['id']).first()
        if not user:
            raise Exception('User not found. Please signup first.')
        elif not course:
            raise Exception('Course id is invalid.')
        elif not user.current_course:
            raise Exception('Please enroll to a course first to complete.')
        elif user.current_course.id != course.id or not course:
            raise Exception('You have not enrolled into this course.')
        user.current_course = None
        user.save()
        return jsonify({'message': 'Thank you for completing {}.'.format(course.name)}), 200
    except KeyError:
        return jsonify({'error': 'Please provide all the required data.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400