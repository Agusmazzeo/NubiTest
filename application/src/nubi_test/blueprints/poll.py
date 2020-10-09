from flask import Blueprint, current_app, jsonify, request, session

from nubi_test.models.mongo import Poll, Answer

polls_bp = Blueprint('polls_bp', __name__)


@polls_bp.route('', methods=['GET'])
def get_all_polls():
    status_code = 200
    polls = []
    polls = Poll.get_all()
    if not polls['status']:
        current_app.logger.error(polls['result'])
        status_code = 500
    return jsonify(success=polls['status'], result=polls['result']), status_code


@polls_bp.route('/labels', methods=['GET'])
def get_by_label():
    status_code = 200
    labels = request.args.to_dict()
    polls = Poll.get_by_labels(labels)
    if not polls['status']:
        current_app.logger.error(polls['result'])
        status_code = 500
    return jsonify(success=polls['status'], result=polls['result']), status_code

@polls_bp.route('/user', methods=['GET'])
def get_by_user():
    status_code = 200
    user_id = request.args.to_dict()['id']
    polls = Poll.get_by_user(user_id)
    if not polls['status']:
        current_app.logger.error(polls['result'])
        status_code = 500
    return jsonify(success=polls['status'], result=polls['result']), status_code

@polls_bp.route('/create', methods=['POST'])
def create_poll():
    output = {}
    current_app.logger.info("A new poll was received.")
    user_id = session.get('user')
    if user_id:
        if request.mimetype != 'application/json':
            current_app.logger.info(
                "Job submission received with incorrect Content-Type. Must be 'application/json'")
            return jsonify(success=False), 400

        poll_template = request.get_json()
        poll_template['author'] = user_id
        output = Poll.create(poll_template)
        if output['status']:
            message = "The poll was succesfully saved!"
            current_app.logger.info(message)
            status_code = 200
        else:
            message = output['result']
            current_app.logger.warning(message)
            status_code = 400
    else:
        output['status'] = False
        message = "You must login before creating polls."
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
    answer_template['author'] = session.get('user', 'Unknown')
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
