FROM python:3.7.5
COPY . /usr/app/data-catalog
WORKDIR /usr/app/data-catalog
RUN cd /usr/app/data-catalog; pip install -r requirements.txt
ENTRYPOINT cd /usr/app/data-catalog; python manage.py runserver 0:8000
EXPOSE 8000:8000
