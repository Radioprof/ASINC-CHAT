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

    def test_right_message(self):


# def auth(name, password):
#     data = {
#         "action": "authenticate",
#         "time": time.time(),
#         "user": {
#             "account_name": name,
#             "password": password
#             }
#         }
#     return data
#
#
# def presence(name, status_mes=None):
#     data = {
#         "action": "presence",
#         "time": time.time(),
#         "type": "status",
#         "user": {
#             "account_name": name,
#             "status": status_mes
#             }
#         }
#     return data
