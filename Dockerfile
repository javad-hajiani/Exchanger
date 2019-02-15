FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
EXPOSE 8000
RUN python manage.py makemigrations && python manage.py migrate
ENTRYPOINT ["python","manage.py","runserver","0.0.0.0:8000"]