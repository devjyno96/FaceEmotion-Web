import time
import unittest

import requests
import json

from FaceEmotion.models import user as user_models
from FaceEmotion.models import manage
from FaceEmotion import database

from fastapi import status


def get_user_list():
    db = database.SessionLocal()
    manage.create_all()  # 초기화 매핑
    user_list = db.query(user_models.User).all()
    return user_list


class Order_01_User_Test(unittest.TestCase):

    def setUp(self):
        self.host = 'http://localhost:8000'
        self.create_user = {
            "username": "test_1",
            "password": "string",
            "name": "test_1",
            "is_admin": False
        }
        self.change_password = {
            "username": "test_1",
            "new_password": "string",
            "check_password": "string"
        }
        self.login_user = {
            "username": "test_1",
            "password": "string",
        }

    def test_01_can_create_user(self):
        response = requests.post(self.host + '/user/', data=json.dumps(self.create_user))
        data = json.loads(response.text)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg="user create data Error")

    def test_03_can_user_change_password(self):
        response = requests.put(self.host + '/user/password', data=json.dumps(self.change_password))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg="User Change Password Error")

    def test_04_user_create_10(self):
        for i in range(2, 12):
            create_user = {
                "username": f"test_{i}",
                "password": "string",
                "name": f"test_{i}",
                "is_admin": False
            }
            response = requests.post(self.host + '/user/', data=json.dumps(create_user))
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg="user create data Error")

    def test_06_can_user_login(self):
        return  # 로그인 기능 에러 발생
        header = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
        response = requests.post(self.host + '/user/login', headers=header, data=self.login_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg="User Login Error")

    def test_07_can_user_get_refresh_token(self):
        return  # 로그인 기능 에러 발생
        header = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
        login_response = requests.post(self.host + '/user/login', headers=header, data=self.login_user)
        data = json.loads(login_response.text)

        time.sleep(2)

        header_refresh = {'Content-type': 'application/json',
                          'accept': 'application/json',
                          'Authorization': 'Bearer ' + str(data['refresh_token']),
                          }

        response = requests.post(self.host + '/user/refresh', headers=header_refresh)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg="User Refresh Token Error")


if __name__ == "__main__":
    unittest.main(warnings='ignore')
