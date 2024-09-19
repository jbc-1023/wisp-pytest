from flask import Blueprint, g, request, jsonify
from app.db import get_db
from app.middleware import token_required
from app.util import check_winner

bp = Blueprint('ping', __name__)

@bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({ "message": "pong!",}), 200
