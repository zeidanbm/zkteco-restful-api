from flask import Blueprint, request, jsonify
from zkteco.services.zk_service import get_zk_service
from zkteco.validations import create_user_schema, delete_user_schema, get_fingerprint_schema, delete_fingerprint_schema, validate_data
from flask import current_app

bp = Blueprint('user', __name__, url_prefix='/')
zk_service = get_zk_service()

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

        current_app.logger.info(f"Creating user with ID: {user_id} and Data: {user_data}")
    
        zk_service.create_user(user_id, user_data)
        return jsonify({"message": "User added successfully"})
    except Exception as e:
        error_message = f"Error creating user: {str(e)}"
        current_app.logger.error(error_message)
        return jsonify({"message": error_message}), 500

def serialize_user(user):
    return {
        "id": user.user_id,
        "name": user.name,
        "groupId": user.group_id
    }

def serialize_template(template):
    return {
        "id": template.uid,
        "fid": template.fid,
        "valid": template.valid,
        "template": template.template.decode('utf-8', errors='ignore'),
    }

@bp.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = zk_service.get_all_users()
        # Serialize each User object to a dictionary
        serialized_users = [serialize_user(user) for user in users]
        return jsonify({"message": "Users retrieved successfully", "data": serialized_users})
    except Exception as e:
        error_message = f"Error retrieving users: {str(e)}"
        current_app.logger.error(error_message)
        return jsonify({"message": error_message}), 500
    

@bp.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    data = {"user_id": int(user_id)}

    error = validate_data(data, delete_user_schema.schema)
    if error:
        return jsonify({"error": error}), 400
    
    try:
        current_app.logger.info(f"Deleting user with ID: {user_id}")
        zk_service.delete_user(data["user_id"])
        return jsonify({"message": "User deleted successfully"})
    except Exception as e:
        error_message = f"Error deleting user: {str(e)}"
        current_app.logger.error(error_message)
        return jsonify({"message": error_message}), 500


@bp.route('/user/<user_id>/fingerprint', methods=['POST'])
def create_fingerprint(user_id):
    data = request.json
    temp_id = data.get('temp_id')
    
    try:
        current_app.logger.info(f"Creating fingerprint for user with ID: {user_id} and finger index: {temp_id}")
        zk_service.enroll_user(int(user_id), int(temp_id))
        return jsonify({"message": "Fingerprint created successfully"})
    except Exception as e:
        error_message = f"Error creating fingerprint: {str(e)}"
        current_app.logger.error(error_message)
        return jsonify({"message": error_message}), 500


@bp.route('/user/<user_id>/fingerprint/<temp_id>', methods=['DELETE'])
def delete_fingerprint(user_id, temp_id):
    data = {"user_id": int(user_id), "temp_id": int(temp_id)}

    error = validate_data(data, delete_fingerprint_schema.schema)
    if error:
        return jsonify({"error": error}), 400

    try:
        current_app.logger.info(f"Deleting fingerprint for user with ID: {user_id} and finger index: {temp_id}")
        zk_service.delete_user_template(data["user_id"], data["temp_id"])
        return jsonify({"message": "Fingerprint deleted successfully"})
    except Exception as e:
        error_message = f"Error deleting fingerprint: {str(e)}"
        current_app.logger.error(error_message)
        return jsonify({"message": error_message}), 500


@bp.route('/user/<user_id>/fingerprint/<temp_id>', methods=['GET'])
def get_fingerprint(user_id, temp_id):
    data = {"user_id": int(user_id), "temp_id": int(temp_id)}

    error = validate_data(data, get_fingerprint_schema.schema)
    if error:
        return jsonify({"error": error}), 400
    
    try:
        current_app.logger.info(f"Getting fingerprint for user with ID: {user_id} and finger index: {temp_id}")
        template = zk_service.get_user_template(data["user_id"], data["temp_id"])
        # Serialize template
        serialized_template = serialize_template(template)
        current_app.logger.info(f"Fingerprint retrieved : {template.template}")
        return jsonify({"message": "Fingerprint retrieved successfully", "data": serialized_template})
    except Exception as e:
        error_message = f"Error retrieving fingerprint: {str(e)}"
        current_app.logger.error(error_message)
        return jsonify({"message": error_message}), 500
