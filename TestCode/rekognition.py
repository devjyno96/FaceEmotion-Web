import random
import unittest
import requests
import json

from fastapi import status


class Order_01_Rekognition(unittest.TestCase):

    def setUp(self):
        self.host = 'http://localhost:8000'

    def test_01_get_html(self):
        response = requests.get(self.host + "/rekognition/")
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Rekognition HTML Load Error")

    def test_02_request_rekognition(self):

        pass
    def test_0(self):
        pass
    def test_0(self):
        pass
    def test_0(self):
        pass
    def test_0(self):
        pass
    def test_0(self):
        pass
    def test_0(self):
        pass
    def test_0(self):
        pass

if __name__ == "__main__":
    unittest.main(warnings='ignore')
    # Order_01_SampleColumn_Test.run()