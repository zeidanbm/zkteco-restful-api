class SimulatorZK:
    def __init__(self, ip, port=4370, timeout=5, password=0, force_udp=False, omit_ping=False):
        # Initialize any required attributes for your simulator
        self.users = {}

    def connect(self):
        # Implement connection logic if needed
        pass

    def disable_device(self):
        # Implement disable_device logic if needed
        pass

    def enable_device(self):
        # Implement enable_device logic if needed
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
