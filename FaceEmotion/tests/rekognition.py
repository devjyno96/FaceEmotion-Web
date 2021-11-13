import unittest
from pathlib import Path

import requests
import json
import os

from fastapi import status


class Order_01_Rekognition(unittest.TestCase):

    def setUp(self):
        self.file_folder = str(Path(os.path.realpath(__file__)).parent.absolute()) + '/resource/'
        self.host = 'http://localhost:8000'

    def test_01_get_html(self):
        response = requests.get(self.host + "/rekognition/")
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Rekognition HTML Load Error")

    def test_02_request_rekognition(self):
        image = open(self.file_folder + 'image/test_image.jpeg', 'rb')
        image_read = image.read()
        files = {'file': image_read}

        response = requests.post(self.host + '/rekognition', files=files)

        with open("resource/request_result.json", "w") as json_file:
            json.dump(json.loads(response.text), json_file)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg="Rekognition HTML Load Error")

    def test_03_request_rekognition_multi(self):
        for i in range(5):
            image = open(self.file_folder + 'image/test_image.jpeg', 'rb')
            image_read = image.read()
            files = {'file': image_read}

            response = requests.post(self.host + '/rekognition', files=files)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg="Rekognition HTML Load Error")

    def test_04_get_rekognition_result_all_by_user_id(self):
        user_id = 1
        response = requests.get(self.host + '/rekognition/result/all', params={'user_id': user_id})

        with open("resource/request_result_all.json", "w") as json_file:
            json.dump(json.loads(response.text), json_file)

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Rekognition Result Get All Error")

    def test_05_get_rekognition_result_list_in_duration(self):
        user_id = 1
        response = requests.get(self.host + '/rekognition/result/duration', params={'user_id': user_id})

        with open("resource/request_result_all_duration.json", "w") as json_file:
            json.dump(json.loads(response.text), json_file)

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Rekognition Result Get All Error")


if __name__ == "__main__":
    unittest.main(warnings='ignore')
