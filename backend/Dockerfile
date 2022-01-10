FROM python:3.7
COPY requirements.txt /
RUN pip3 install -r /requirements.txt
COPY . /app
WORKDIR /app
CMD gunicorn app:app -w 2 --threads 2 -b 0.0.0.0:8000