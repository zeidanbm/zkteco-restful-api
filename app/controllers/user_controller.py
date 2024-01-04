import os
from flask import Blueprint, request, jsonify
from app.services.zkteco_service import ZktecoService
from zk import ZK
from app.validations import create_user_schema, delete_user_schema, get_fingerprint_schema, delete_fingerprint_schema, validate_data

bp = Blueprint('user', __name__, url_prefix='/')

zkteco_service = ZktecoService(
    zk_class=ZK,
    ip=os.environ.get('DEVICE_IP', '192.168.20.205'),
    port=int(os.environ.get('DEVICE_PORT', '4370'))
)

@bp.route('/user', methods=['POST'])
def create_user():
    data = request.json

    # Validate against the create user schema
    error = validate_data(data, create_user_schema.schema)
    if error:
        return jsonify({"error": error}), 400

    try:
        user_id = data.get('user_id')
        user_data = data.get('user_data')
    
        zkteco_service.create_user(user_id, user_data)
        return jsonify({"message": "User added successfully"})
    except Exception as e:
        error_message = f"Error creating user: {str(e)}"
        return jsonify({"message": error_message}), 500


@bp.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = zkteco_service.get_all_users()
        return jsonify({"message": "Users retrieved successfully", "data": users})
    except Exception as e:
        error_message = f"Error retrieving users: {str(e)}"
        return jsonify({"message": error_message}), 500
    


@bp.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    data = {"user_id": int(user_id)}

    error = validate_data(data, delete_user_schema.schema)
    if error:
        return jsonify({"error": error}), 400
    
    try:
        zkteco_service.delete_user(data["user_id"])
        return jsonify({"message": "User deleted successfully"})
    except Exception as e:
        error_message = f"Error deleting user: {str(e)}"
        return jsonify({"message": error_message}), 500


@bp.route('/user/<user_id>/fingerprint', methods=['POST'])
def create_fingerprint(user_id):
    data = request.json
    temp_id = data.get('temp_id')
    
    try:
        zkteco_service.enroll_user(int(user_id), int(temp_id))
        return jsonify({"message": "Fingerprint created successfully"})
    except Exception as e:
        error_message = f"Error creating fingerprint: {str(e)}"
        return jsonify({"message": error_message}), 500


@bp.route('/user/<user_id>/fingerprint/<temp_id>', methods=['DELETE'])
def delete_fingerprint(user_id, temp_id):
    data = {"user_id": int(user_id), "temp_id": int(temp_id)}

    error = validate_data(data, delete_fingerprint_schema.schema)
    if error:
        return jsonify({"error": error}), 400

    try:
        zkteco_service.delete_user_template(data["user_id"], data["temp_id"])
        return jsonify({"message": "Fingerprint deleted successfully"})
    except Exception as e:
        error_message = f"Error deleting fingerprint: {str(e)}"
        return jsonify({"message": error_message}), 500


@bp.route('/user/<user_id>/fingerprint/<temp_id>', methods=['GET'])
def get_fingerprint(user_id, temp_id):
    data = {"user_id": int(user_id), "temp_id": int(temp_id)}

    error = validate_data(data, get_fingerprint_schema.schema)
    if error:
        return jsonify({"error": error}), 400
    
    try:
        zkteco_service.get_user_template(data["user_id"], data["temp_id"])
        return jsonify({"message": "Fingerprint retrieved successfully"})
    except Exception as e:
        error_message = f"Error retrieving fingerprint: {str(e)}"
        return jsonify({"message": error_message}), 500
