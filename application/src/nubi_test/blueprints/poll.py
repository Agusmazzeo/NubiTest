from flask import Blueprint, current_app, jsonify, request

from nubi_test.models.mongo import Poll

polls_bp = Blueprint('polls_bp', __name__)


@polls_bp.route('', methods=['GET'])
def get_all_polls():
    polls = []
    polls = Poll.get_all()
    current_app.logger.info(polls)
    return jsonify(success=True, result=polls), 200


@polls_bp.route('/create', methods=['POST'])
def create_poll():
    current_app.logger.info("A new poll was received.")
    if request.mimetype != 'application/json':
        current_app.logger.info(
            "Job submission received with incorrect Content-Type. Must be 'application/json'")
        return jsonify(success=False), 400

    poll_template = request.get_json()
    current_app.logger.info(poll_template)
    success = Poll.create(poll_template)
    if success:
        message = "The poll was succesfully saved!"
        current_app.logger.info(message)
        status_code = 200
    else:
        message = "A problem ocurred while saving the poll."
        current_app.logger.warning(message)
        status_code = 400
    return jsonify(success=success, result=message), status_code
