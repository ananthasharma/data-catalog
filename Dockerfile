FROM python:3.6.9-buster

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
COPY . /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000:8000/tcp

CMD [ "python", "python manage.py runserver 0:8000" ]