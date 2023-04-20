import os
import sys
import time
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from tools.server_actions import answer_message


class TestAnswerMessage(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_right_message(self):
        data = {
                    "action": "presence",
                    "time": time.time(),
                    "user": {
                        "account_name": 'Guest',
                        }
                    }
        self.assertEqual(answer_message(data), {'response': 200})

    def test_wrong_message1(self):
        data = {
            "action": "authenticate",
            "time": time.time(),
            "user": {
                "account_name": 'Guest',
            }
        }
        self.assertEqual(answer_message(data), {'response': 400, 'error': 'Bad Request'})

    def test_wrong_message2(self):
        data = {
            "action": "presence",
            "time": time.time(),
            "user": {
                "account_name": 'Admin',
            }
        }
        self.assertEqual(answer_message(data), {'response': 400, 'error': 'Bad Request'})

    def test_wrong_message2(self):
        data = {
            "action": "presence",
            "user": {
                "account_name": 'Guest',
            }
        }
        self.assertEqual(answer_message(data), {'response': 400, 'error': 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
