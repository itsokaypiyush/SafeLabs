from flask import Blueprint, request, jsonify, session as flask_session
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity
)
from flask_login import login_user, logout_user, current_user
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

routes_bp = Blueprint("routes", __name__)

# ✅ Late import karenge in `app.py`
def load_user(user_id):
    from app import db  # ✅ Yaha import karenge
    return User.query.get(int(user_id))

@routes_bp.route("/register", methods=["POST"])
def register():
    from app import db  # ✅ Late import
    data = request.json
    hashed_password = generate_password_hash(data["password"])  
    new_user = User(email=data["email"], password=hashed_password)

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

@routes_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()

    if user and check_password_hash(user.password, data["password"]):
        login_user(user)
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
        refresh_token = create_refresh_token(identity=user.id)  

        flask_session["last_active"] = datetime.utcnow().isoformat()
        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

@routes_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)  
def refresh():
    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=user_id, expires_delta=timedelta(hours=1))
    return jsonify({"access_token": new_access_token})

@routes_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    logout_user()
    flask_session.pop("last_active", None)
    return jsonify({"message": "Logged out"}), 200

@routes_bp.route("/check_session", methods=["GET"])
@jwt_required()
def check_session():
    last_active_str = flask_session.get("last_active")

    if last_active_str:
        last_active = datetime.fromisoformat(last_active_str)
        if (datetime.utcnow() - last_active) > timedelta(seconds=120):
            logout_user()
            flask_session.pop("last_active", None)
            return jsonify({"error": "Session timeout, logged out"}), 401

    flask_session["last_active"] = datetime.utcnow().isoformat()
    return jsonify({"message": "Session active"}), 200
