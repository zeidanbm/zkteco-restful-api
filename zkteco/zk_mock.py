class HelperMock:
    def test_ping(self, ping = True):
        return ping


class ZKSockMock:
    def settimeout(self, time):
        pass

    def recv(self, data):
        return b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F"

class ZKMock:
    def __init__(self, ip, port=4370, timeout=5, password=0, verbose=False, force_udp=False, omit_ping=False):
        self.users = {}
        self.is_connect = False
        self.is_enabled = True
        self.end_live_capture = False
        self.helper = HelperMock()
        self._ZK__sock = ZKSockMock()
        self.tcp = True

    def connect(self):
        # Implement connection logic if needed
        self.is_connect = True
        pass

    def disable_device(self):
        # Implement disable_device logic if needed
        pass

    def enable_device(self):
        # Implement enable_device logic if needed
        pass

    def cancel_capture(self):
        # Implement cancel_capture logic if needed
        pass

    def verify_user(self):
        # Implement verify_user logic if needed
        pass
    
    def reg_event(self, event_id):
        # Implement reg_event logic if needed
        pass

    def _ZK__ack_ok(self):
        pass

    def get_users(self):
        return self.users
    

    
    def set_user(self, uid, name, privilege, password, group_id, user_id, card):
        # Simulate setting a user by storing user data in the dictionary
        self.users[uid] = {
            'name': name,
            'privilege': privilege,
            'password': password,
            'group_id': group_id,
            'user_id': user_id,
            'card': card
        }
    
    def delete_user(self, uid=0, user_id=''):
        
        if not uid:
            users = self.get_users()
            users = list(filter(lambda x: x.user_id==str(user_id), users))
            if not users:
                return False
            uid = users[0].uid

        del self.users[uid]        


