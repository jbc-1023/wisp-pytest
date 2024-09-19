import jwt
from datetime import datetime, timedelta
from flask import Blueprint, g, request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Request body must be JSON"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Missing required fields!"}), 400

    db = get_db()

    insert_query = """
        INSERT INTO users (username, password)
        VALUES (?, ?)
    """

    try:
        cursor = db.execute(insert_query, (username, generate_password_hash(password, "pbkdf2")))
        db.commit()
        return jsonify({
            "message": "User registered successfully!",
            "user": {
                "id": cursor.lastrowid,
                "username": username,
                "wins": 0
            }
        }), 201

    except db.IntegrityError:
        return jsonify({"message": "Username already exists!"}), 400
    except Exception as e:
        return jsonify({"message": "An error occurred: " + str(e)}), 500

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Request body must be JSON"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    db = get_db()
    try:
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        if user and check_password_hash(user["password"], password):
            return jsonify({
                "status": "success",
                "token": jwt.encode(
                    {
                        "user_id": user["id"],
                        "exp" : datetime.utcnow() + timedelta(minutes = 30)
                    },
                    current_app.config["SECRET_KEY"],
                    algorithm="HS256"
                ),
                "user": {
                    "id": user["id"],
                    "username": user["username"],
                    "wins": user["wins"]
                }
            }), 200
        else:
            return jsonify({"status": "failed"}), 403

    except Exception as e:
        return jsonify({"message": "An error occurred: " + str(e)}), 500
