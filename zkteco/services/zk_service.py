from zk import ZK, const
from typing import Type
import time
from flask import current_app, g
#from zkteco.simulator_zk import SimulatorZK

class ZkService:
    def __init__(self, zk_class: Type[ZK], ip, port=4370, verbose=False, timeout=None, password=0, force_udp=False):
        try:
            self.zk = zk_class(
                ip,
                port=port,
                timeout=timeout,
                password=password,
                force_udp=force_udp,
                verbose=verbose
            )
            self.connect()
        except Exception as e:
            current_app.logger.warning(f"Could not connect to Zkteco device on {ip}:{port} : {e}")

    def create_user(self, user_id, user_data):
        try:
            zk_instance = self.zk
            self.connect()
            self.disable_device()
            
            zk_instance.set_user(
                uid=user_id,
                name=user_data.get('name'),
                privilege=user_data.get('privilege', const.USER_DEFAULT),
                password=user_data.get('password', ''),
                group_id=user_data.get('group_id', 0),
                user_id=str(user_id),
                card=user_data.get('card', 0)
            )
        finally:
            self.enable_device()

    def get_all_users(self):
        try:
            zk_instance = self.zk
            self.connect()
            self.disable_device()
            users = zk_instance.get_users()

            return users
        finally:
            self.enable_device()

    def delete_user(self, user_id):
        try:
            zk_instance = self.zk
            self.connect()
            self.disable_device()
            zk_instance.delete_user(
                uid=user_id,
                user_id=str(user_id)
            )
        finally:
            self.enable_device()
    
    def enroll_user(self, user_id, temp_id):
        try:
            zk_instance = self.zk
            self.connect()
            self.disable_device()
            zk_instance.enroll_user(
                uid = user_id,
                temp_id = temp_id,
                user_id = str(user_id)
            )
        finally:
            self.enable_device()
            
    def cancel_enroll_user(self):
        try:
            zk_instance = self.zk
            self.connect()
            self.zk.end_live_capture = True
            self.disable_device()
            zk_instance.cancel_capture()
        finally:
            self.enable_device()
    
    def delete_user_template(self, user_id, temp_id):
        try:
            zk_instance = self.zk
            self.connect()
            self.disable_device()
            zk_instance.delete_user_template(
                uid = user_id,
                temp_id = temp_id,
                user_id= str(user_id)
            )
        finally:
            self.enable_device()
    
    def get_user_template(self, user_id, temp_id):
        try:
            zk_instance = self.zk
            self.connect()
            self.disable_device()
            zk_instance.get_user_template(
                uid = user_id,
                temp_id = temp_id,
                user_id = str(user_id)
            )
        finally:
            self.enable_device()
    
    def connect(self):
        if self.zk.is_connect and self.zk.helper.test_ping():
            return

        while True:
            try:
                self.zk.connect()
                current_app.logger.info("Connected to ZK device successfully")
                return
            except Exception as e:
                current_app.logger.warning(f"Failed to connect to ZK device. Retrying... ({e})")
                time.sleep(5)

    def disconnect(self):
        try:
            self.zk.disconnect()
            current_app.logger.info("Disconnected from ZK device")
        except Exception as e:
            current_app.logger.error(f"Error disconnecting from ZK device: {e}")

    def enable_device(self):
        self.zk.enable_device()

    def disable_device(self):
        self.zk.disable_device()


def get_zk_service():
    """
    Get the singleton instance of ZkService.

    If the instance does not exist in the Flask application context,
    create a new instance and store it in the context.

    Returns:
        SingletonClass: The singleton instance of ZkService.
    """
    if 'zk_service' not in g:
        g.zk_service =  ZkService(
            zk_class = ZK,
            ip = current_app.config.get('DEVICE_IP'),
            port = current_app.config.get('DEVICE_PORT'),
            verbose = current_app.config.get('DEBUG')
        )
    return g.zk_service