import copy
import datetime
import os
import re

from flask import Blueprint, jsonify, request, make_response

from project import db
from project.api.models import User

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/hello/all', methods=['GET'])
def all_users():
    """
    Fetch all users from the database
    :return: JSONify'd response of all users
    """
    response_object = {'status': 'success', 'container_id': os.uname()[1],
                       'users': [user.to_json() for user in User.query.all()]}
    return jsonify(response_object)


@users_blueprint.route('/', methods=['GET'])
def ping():
    """
    Heartbeat of application
    :return: Pong message
    """
    return jsonify({
        'status': 'success',
        'message': 'pong!',
        'container_id': os.uname()[1]
    })


def validate_birthday(birthday_str):
    status, birthday, error_msg = False, None, ''
    try:
        birthday = datetime.date.fromisoformat(birthday_str)
    except ValueError as ve:
        error_msg = f'Invalid birth date string {birthday_str}: {ve}'
    else:
        in_the_past = birthday < datetime.date.today()
        if not in_the_past:
            error_msg = f'Birthday cannot be in the future: {birthday_str}\n'
        else:
            status = True
    return status, birthday, error_msg


def insert_user(name, birthday_str):
    pattern = '^[a-zA-Z]+$'
    if not re.match(pattern, name):
        return make_response(f'The value "{name}" does not match this regex pattern: {pattern}\n', 400)
    status, birthday, error_msg = validate_birthday(birthday_str)
    if not status:
        return make_response(error_msg, 400)
    db.session.add(User(name=name, birthday=birthday))
    db.session.commit()
    # Post an update, don't return anything
    return make_response('', 204)


def calculate_birthday(user):
    """
    For a given user, wish them appropriately
    :param user: User object which is an instance of db.Model
    :return: Flask response
    """
    response_object = dict()
    today = datetime.date.today()
    this_years_birthday = datetime.date(today.year, user.birthday.month, user.birthday.day)
    if this_years_birthday > today:
        remaining = (this_years_birthday - today).days
    else:
        next_years_birthday = datetime.date(today.year + 1, user.birthday.month, user.birthday.day)
        remaining = (next_years_birthday - today).days
    if remaining == 0:
        msg = f'Hello, {user.name}! Happy birthday!\n'
    else:
        msg = f'Hello, {user.name}! Your birthday is in {remaining} days\n'
    response_object['message'] = msg
    return jsonify(response_object)


def update_user(user, birthday_str):
    status, birthday, error_msg = validate_birthday(birthday_str)
    if not status:
        return make_response(error_msg, 400)
    else:
        user.birthday = birthday
        db.session.commit()
        return make_response('', 204)


@users_blueprint.route('/hello/<username>', methods=['PUT', 'DELETE', 'GET'])
def single_user(username):
    """
    Performs edit, delete or get operations on a user
    :return: Success/Fail response as json
    """
    user = User.query.filter_by(name=username.lower()).first()
    if request.method == 'PUT':
        put_data = request.get_json()
        if put_data is None:
            return make_response(f'Invalid request {request}: Please provide dateOfBirth as JSON input\n', 400)
        birthday_str = put_data.get('dateOfBirth', '')
        if user is None:
            # The current user does not exist, let's add them in
            return insert_user(username, birthday_str)
        else:
            # The user exists, let's change the data as needed
            return update_user(user, birthday_str)
    elif request.method == 'DELETE':
        user = User.query.filter_by(name=username.lower()).first()
        db.session.delete(user)
        db.session.commit()
        # Post an update, don't return anything
        return make_response('', 204)
    else:
        if user is None:
            return make_response(f'User {username} is not found\n', 404)
        else:
            return calculate_birthday(user)
