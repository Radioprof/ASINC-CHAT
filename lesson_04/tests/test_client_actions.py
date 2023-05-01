import os
import sys
import unittest
import time
sys.path.append(os.path.join(os.getcwd(), '..'))

from tools.client_actions import auth, presence


class TestAnswerMessage(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_right_auth(self):
        data = {
                "action": "authenticate",
                "time": time.time(),
                "user": {
                    "account_name": 'admin',
                    "password": 'admin'
                    }
                }
        self.assertEqual(auth('admin', 'admin'), data)

    def test_right_presence(self):
        data = {
            "action": "presence",
            "time": time.time(),
            "type": "status",
            "user": {
                "account_name": 'guest',
                "status": 'online'
                }
            }
        self.assertEqual(presence('guest', 'online'), data)

    def test_wrong_auth(self):
        data = {
                "action": "authenticate",
                "time": time.time(),
                "user": {
                    "account_name": 'admin',
                    "password": 'admin'
                    }
                }
        self.assertEqual(auth('guest', '1234'), data)


if __name__ == '__main__':
    unittest.main()
