import pprint

import boto3
import os, pprint
from dotenv import load_dotenv


def detect_labels_local_file(photo):
    client = boto3.client('rekognition', region_name=os.getenv('region_name'),
                          aws_access_key_id=os.getenv('aws_access_key_id'),
                          aws_secret_access_key=os.getenv('aws_secret_access_key'))

    with open('image.jpeg', 'rb') as image:
        response = client.detect_faces(Image={'Bytes': image.read()}, Attributes=[
            'ALL'
        ])

    # print('Detected labels in ' + photo)
    pprint.pprint(response['FaceDetails'])
    # for label in response['Labels']:
    #     print(label['Name'] + ' : ' + str(label['Confidence']))

    # return len(response['Labels'])


def main():
    load_dotenv()
    photo = 'photo'

    label_count = detect_labels_local_file(photo)
    print("Labels detected: " + str(label_count))


if __name__ == "__main__":
    main()
