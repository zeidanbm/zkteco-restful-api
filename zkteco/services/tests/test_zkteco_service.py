import unittest
from unittest.mock import MagicMock
from zkteco.services.zk_service import ZkService
from __editable___pyzk_0_9_1_finder import const

class TestZkService(unittest.TestCase):
    # Mock setup
    zk_mock = MagicMock()
    zk_instance_mock = MagicMock()
    zk_mock.return_value = zk_instance_mock
    
    @classmethod
    def setUpClass(self):
        self.patcher = unittest.mock.patch('zkteco_service.ZK', self.zk_mock)
        self.patcher.start()
    
    @classmethod
    def tearDownClass(self):
        self.patcher.stop()
        
    def setUpQuickUser(self):
        # Common setup for each test
        self.zkteco_service = ZkService(ip='127.0.0.1')
        self.zkteco_service.create_user(user_id=1, user_data={'name': 'John'})

    def test_disable_device_called(self):
        # Act
        self.setUpQuickUser()
        
        # Assert
        self.zk_instance_mock.disable_device.assert_called_once()
        
    def test_set_user_called(self):
        # Act
        self.setUpQuickUser()

        # Assert
        self.zk_instance_mock.set_user.assert_called_once_with(
            uid=1,
            name='John',
            privilege=const.USER_DEFAULT,
            password='',
            group_id='',
            user_id=1,
            card=0
        )
    
    def test_enable_device_called(self):
        # Act
        self.setUpQuickUser()

        # Assert
        self.zk_instance_mock.enable_device.assert_called_once()
