from zk import ZK, const
from typing import Type
import requests
import os
import threading
from struct import unpack
from socket import timeout
import time


class ZktecoService:
    def __init__(self, zk_class: Type[ZK], ip, port=4370, timeout=30, password=0, force_udp=False):
        try:
            self.zk = zk_class(
                ip,
                port=port,
                timeout=timeout,
                password=password,
                force_udp=force_udp,
                verbose=True
            )
            self.connect()
        except Exception as e:
            print(f"Could not connect to Zkteco device on {ip}:{port} : {e}")

    def start_live_capture_thread(self):
        self.live_capture_thread = threading.Thread(target=self.live_capture)
        self.live_capture_thread.start()

    def live_capture(self, new_timeout=3600):
        self.zk.cancel_capture()
        self.zk.verify_user()
        self.enable_device()
        self.zk.reg_event(1)
        self.zk._ZK__sock.settimeout(new_timeout)
        self.zk.end_live_capture = False
        while not self.zk.end_live_capture:
            try:
                data_recv = self.zk._ZK__sock.recv(1032)
                self.zk._ZK__ack_ok()
              
                header = unpack('HHHH', data_recv[8:16])
                data = data_recv[16:]
               
                if not header[0] == 500:
                    continue
                if not len(data):
                    continue
                while len(data) >= 12:
                    if len(data) == 36:
                        user_id, _status, _punch, _timehex, _other = unpack('<24sBB6s4s', data[:36])
                        data = data[36:]
                    
                    user_id = (user_id.split(b'\x00')[0]).decode(errors='ignore')
                    self.send_attendace_request(user_id)
            except timeout:
                print("time out")
            except (KeyboardInterrupt, SystemExit):
                break
        self.zk._ZK__sock.settimeout(60)
        self.zk.reg_event(0)

    def send_attendace_request(self, member_id):
        try:
            attendance_url = os.environ.get('BACKEND_URL') + '/check-in'
            payload = { 'member_id': member_id }
            requests.post(attendance_url, data=payload)
        except requests.RequestException as e:
            print(f"Error in send_attendance_request: {str(e)}")

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
                user_id=user_id
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
        if(self.zk.is_connect and self.zk.helper.test_ping()):
            return
        
        attempts = 3
        for _ in range(attempts):
            try:
                self.zk.connect()
                print("Connected to ZK device successfully")
                return
            except Exception as e:
                print(f"Failed to connect to ZK device. Retrying... ({e})")
                time.sleep(1)  # Wait for 2 seconds before retrying

    def disconnect(self):
        try:
            self.zk.disconnect()
            print("Disconnected from ZK device")
        except Exception as e:
            print(f"Error disconnecting from ZK device: {e}")

    def enable_device(self):
        self.zk.enable_device()

    def disable_device(self):
        self.zk.disable_device()
