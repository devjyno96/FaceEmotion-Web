import random
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg="Rekognition HTML Load Error")

    def test_03_get_rekognition_result_all(self):
        pass

    def test_04_get_rekognition_result_list_in_duration(self):
        pass


if __name__ == "__main__":
    unittest.main(warnings='ignore')
