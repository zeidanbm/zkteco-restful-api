from flask import Blueprint, jsonify
from zkteco.services.zk_service import ZkService
from zk import ZK
from flask import current_app


bp = Blueprint('device', __name__, url_prefix='/')


@bp.route('/device/capture', methods=['GET'])
def device_connect():
    try:
        ZkService(
            zk_class = ZK,
            ip = current_app.config.get('DEVICE_IP'),
            port = current_app.config.get('DEVICE_PORT'),
            verbose = current_app.config.get('DEBUG')
        )

        return jsonify({"message": "Device connected successfully"})
    except Exception as e:
        error_message = f"Error starting device capture: {str(e)}"
        return jsonify({"message": error_message}), 500
    