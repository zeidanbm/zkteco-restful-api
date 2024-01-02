from zk import ZK, const
from typing import Type
import requests
import os
import threading
from struct import unpack
from socket import timeout


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
        socket = self.zk.get_socket()
        socket.settimeout(new_timeout)
        self.zk.end_live_capture = False
        while not self.zk.end_live_capture:
            try:
                data_recv = socket.recv(1032)
                self.zk.ack_ok()
              
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
        socket.settimeout(60)
        self.zk.reg_event(0)

    def fingerprint_capture(self):
        for attendance in self.zk.live_capture():
            if attendance is None:
                pass
            else:
                self.send_attendace_request(attendance.user_id)

    def send_attendace_request(self, member_id):
        try:
            attendance_url = os.environ.get('BACKEND_URL') + '/check-in'
            payload = { 'member_id': member_id }
            response = requests.post(attendance_url, data=payload)

            # Handle the response as needed
            print(response.text)
        except requests.RequestException as e:
            print(f"Error in send_attendance_request: {str(e)}")
            # Handle the error as needed

    def create_user(self, user_id, user_data):
        try:
            zk_instance = self.zk
            
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

            print(f"User with ID {user_id} created successfully")
        except Exception as e:
            print(f"Error creating user: {e}")
        finally:
            self.enable_device()
            self.start_live_capture_thread()

    def get_all_users(self):
        try:
            zk_instance = self.zk
            self.disable_device()
            users = zk_instance.get_users()

            for user in users:
                print(user)
            
            print(f"Users retrieved successfully")
        except Exception as e:
            print(f"Error retrieving users: {e}")
        finally:
            self.enable_device()

    def delete_user(self, user_id):
        try:
            zk_instance = self.zk
            self.disable_device()
            zk_instance.delete_user(
                user_id=user_id
            )
            
            print(f"User with ID {user_id} deleted successfully")
        except Exception as e:
            print(f"Error deleting user: {e}")
        finally:
            self.enable_device()
    
    def enroll_user(self, user_id, temp_id):
        try:
            zk_instance = self.zk
            self.disable_device()
            zk_instance.enroll_user(
                uid = user_id,
                temp_id = temp_id,
                user_id = str(user_id)
            )
            
            print(f"User with ID {user_id} enrolled successfully")
        except Exception as e:
            print(f"Error enrolling user: {e}")
        finally:
            self.enable_device()
            
    def cancel_enroll_user(self):
        try:
            zk_instance = self.zk
            self.disable_device()
            zk_instance.cancel_capture()
            
            print(f"Fingerprint capture canceled successfully")
        except Exception as e:
            print(f"Error canceling fingerprint capture: {e}")
        finally:
            self.enable_device()
    
    def delete_user_template(self, user_id, temp_id):
        try:
            zk_instance = self.zk
            self.disable_device()
            zk_instance.delete_user_template(
                uid = user_id,
                temp_id = temp_id,
                user_id= str(user_id)
            )
            
            print(f"User with ID {user_id} fingerprint template {temp_id} deleted successfully")
        except Exception as e:
            print(f"Error deleting fingerprint template: {e}")
        finally:
            self.enable_device()
    
    def get_user_template(self, user_id, temp_id):
        try:
            zk_instance = self.zk
            self.disable_device()
            zk_instance.get_user_template(
                uid = user_id,
                temp_id = temp_id,
                user_id = str(user_id)
            )
            
            print(f"User with ID {user_id} template {temp_id} retrieved successfully")
        except Exception as e:
            print(f"Error retrieving user template: {e}")
        finally:
            self.enable_device()
    
    def connect(self):
        try:
            self.zk.connect()
            print("Connected to the fingerprint machine")
        except Exception as e:
            print(f"Error connecting to the fingerprint machine: {e}")

    def disconnect(self):
        try:
            self.zk.disconnect()
            print("Disconnected from the fingerprint machine")
        except Exception as e:
            print(f"Error disconnecting from the fingerprint machine: {e}")

    def enable_device(self):
        self.zk.enable_device()
        #self.start_live_capture_thread()

    def disable_device(self):
        #self.zk.end_live_capture = True
        self.zk.disable_device()
