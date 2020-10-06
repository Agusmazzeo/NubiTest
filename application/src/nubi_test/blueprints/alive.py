from flask import Blueprint, current_app, jsonify

alive_bp = Blueprint('alive_bp', __name__)


@alive_bp.route('', methods=['GET'])
def alive():
    return jsonify(alive=True), 200