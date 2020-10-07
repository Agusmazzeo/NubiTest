from flask import Blueprint, current_app, jsonify, request

from nubi_test.models.mongo import Poll, Answer

polls_bp = Blueprint('polls_bp', __name__)


@polls_bp.route('', methods=['GET'])
def get_all_polls():
    polls = []
    polls = Poll.get_all()
    return jsonify(success=True, result=polls), 200

@polls_bp.route('/labels', methods=['GET'])
def get_by_label():
    labels = request.args.to_dict()
    polls = Poll.get_by_labels(labels)
    return jsonify(success=True, result=polls), 200

@polls_bp.route('/create', methods=['POST'])
def create_poll():
    current_app.logger.info("A new poll was received.")
    if request.mimetype != 'application/json':
        current_app.logger.info(
            "Job submission received with incorrect Content-Type. Must be 'application/json'")
        return jsonify(success=False), 400

    poll_template = request.get_json()
    output = Poll.create(poll_template)
    if output['status']:
        message = "The poll was succesfully saved!"
        current_app.logger.info(message)
        status_code = 200
    else:
        message = output['result']
        current_app.logger.warning(message)
        status_code = 400
    return jsonify(success=output['status'], result=message), status_code


@polls_bp.route('/answer/<poll_id>', methods=['POST'])
def answer_poll(poll_id):
    current_app.logger.info(f"An answer to poll {id} was received.")
    if request.mimetype != 'application/json':
        current_app.logger.info(
            "Job submission received with incorrect Content-Type. Must be 'application/json'")
        return jsonify(success=False), 400

    answer_template = request.get_json()
    output = Answer.create(poll_id, answer_template)
    if output['status']:
        message = "The Answer was succesfully saved!"
        current_app.logger.info(message)
        status_code = 200
    else:
        message = output['result']
        current_app.logger.warning(message)
        status_code = 400
    return jsonify(success=output['status'], result=message), status_code
