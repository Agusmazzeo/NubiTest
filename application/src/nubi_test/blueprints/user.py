import uuid
from flask import Blueprint, current_app, jsonify, request, session

from nubi_test.models.mongo import User

users_bp = Blueprint('users_bp', __name__)


@users_bp.route('/sign_in', methods=['POST'])
def sign_in():
    current_app.logger.info("A new User was received.")
    if request.mimetype != 'application/json':
        current_app.logger.info(
            "Job submission received with incorrect Content-Type. Must be 'application/json'")
        return jsonify(success=False), 400

    user_template = request.get_json()
    output = User.sign_in(user_template)
    if output['status']:
        message = "The User was succesfully saved!"
        current_app.logger.info(message)
        status_code = 200
    else:
        message = output['result']
        current_app.logger.warning(message)
        status_code = 400
    return jsonify(success=output['status'], result=message), status_code


@users_bp.route('/log_in', methods=['POST'])
def log_in():
    current_app.logger.info("A User is trying to log in")
    if request.mimetype != 'application/json':
        current_app.logger.info(
            "Job submission received with incorrect Content-Type. Must be 'application/json'")
        return jsonify(success=False), 400

    user_template = request.get_json()
    output = User.log_in(user_template)
    if output['status']:
        session['user'] = str(output['result'])
        message = f"Welcome {user_template['username']}!"
        current_app.logger.info(message)
        status_code = 200
    else:
        message = output['result']
        current_app.logger.warning(message)
        status_code = 400
    return jsonify(success=output['status'], result=message), status_code


@users_bp.route('/log_out', methods=['POST'])
def log_out():
    try:
        current_app.logger.info(f"Logging out.")
        session.clear()
        status_code = 200
        result = "User correctly logged out!"
        status = True
    except Exception as ex:
        result = f"An error ocurred while logging out: {ex}"
        status_code = 500
        status = False
        current_app.logger.error(result)
    return jsonify(success=status, result=result), status_code

