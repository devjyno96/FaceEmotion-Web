import boto3
import os
from dotenv import load_dotenv

# Amazon rekognition
load_dotenv()

rekognition = boto3.client('rekognition', region_name=os.getenv('region_name'),
                           aws_access_key_id=os.getenv('aws_access_key_id'),
                           aws_secret_access_key=os.getenv('aws_secret_access_key'))


def run_rekognition_by_byte_image(byte_image):
    response = rekognition.detect_faces(Image={'Bytes': byte_image}, Attributes=[
        'ALL'
    ])
    return response
