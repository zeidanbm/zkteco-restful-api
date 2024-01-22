from distutils.util import strtobool
import os

from dotenv import load_dotenv
from zk import ZK, const
from typing import Type
import time
from zkteco.logger import app_logger

load_dotenv()

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
            app_logger.warning(f"Could not connect to Zkteco device on {ip}:{port} : {e}")

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
        
        retry_count = 0
        max_retries_log = 10

        while True:
            try:
                self.zk.connect()
                app_logger.info("Connected to ZK device successfully")
                retry_count = 0
                return
            except Exception as e:
                retry_count += 1
                app_logger.info(retry_count)
                app_logger.info(max_retries_log)
                if retry_count < max_retries_log:
                    app_logger.warning(f"Failed to connect to ZK device. Retrying... ({e})")
                time.sleep(6)
                continue

    def disconnect(self):
        try:
            self.zk.disconnect()
            app_logger.info("Disconnected from ZK device")
        except Exception as e:
            app_logger.error(f"Error disconnecting from ZK device: {e}")

    def enable_device(self):
        self.zk.enable_device()

    def disable_device(self):
        self.zk.disable_device()


def get_zk_service():
    zk_service =  ZkService(
        zk_class = ZK,
        ip = os.environ.get('DEVICE_IP'),
        port = os.environ.get('DEVICE_PORT'),
        verbose = bool(strtobool(os.getenv("FLASK_DEBUG", "false")))
    )
    return zk_service