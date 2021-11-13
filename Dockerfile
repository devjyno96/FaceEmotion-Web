FROM python:3.9

WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

EXPOSE 8000

COPY ./FaceEmotion /code/FaceEmotion
COPY ./TestCode /code/TestCode
COPY ./.env /code/.env
COPY ./init.sh /code/init.sh


CMD [ "sh" , "init.sh"]

