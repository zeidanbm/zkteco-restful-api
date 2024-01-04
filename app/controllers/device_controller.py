import os
from flask import Blueprint, jsonify
from app.services.zkteco_service import ZktecoService
from zk import ZK


bp = Blueprint('device', __name__, url_prefix='/')


@bp.route('/device/capture', methods=['GET'])
def device_capture():
    try:
        zkteco_service = ZktecoService(
            zk_class=ZK,
            ip=os.environ.get('DEVICE_IP', '192.168.20.205'),
            port=int(os.environ.get('DEVICE_PORT', '4370'))
        )
        zkteco_service.start_live_capture_thread()
        return jsonify({"message": "Device capture started successfully"})
    except Exception as e:
        error_message = f"Error starting device capture: {str(e)}"
        return jsonify({"message": error_message}), 500
    