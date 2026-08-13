from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)

CORS(app)


# Temporary in-memory user storage
# We will replace this with a database later.

users = []


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "service": "user-service",
        "status": "healthy"
    })


# ==========================================
# CREATE USER
# ==========================================

@app.route("/api/users", methods=["POST"])
def create_user():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400


    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")


    if not name or not email or not phone:

        return jsonify({
            "error": "Name, email and phone are required"
        }), 400


    user = {

        "user_id": str(uuid.uuid4()),

        "name": name,

        "email": email,

        "phone": phone

    }


    users.append(user)


    return jsonify({

        "message": "User created successfully",

        "user": user

    }), 201


# ==========================================
# GET ALL USERS
# ==========================================

@app.route("/api/users", methods=["GET"])
def get_users():

    return jsonify(users)


# ==========================================
# GET USER BY ID
# ==========================================

@app.route("/api/users/<user_id>", methods=["GET"])
def get_user(user_id):

    for user in users:

        if user["user_id"] == user_id:

            return jsonify(user)


    return jsonify({
        "error": "User not found"
    }), 404


# ==========================================
# DELETE USER
# ==========================================

@app.route("/api/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):

    for user in users:

        if user["user_id"] == user_id:

            users.remove(user)

            return jsonify({
                "message": "User deleted successfully"
            })


    return jsonify({
        "error": "User not found"
    }), 404


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
