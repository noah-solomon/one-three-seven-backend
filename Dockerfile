FROM python:3.7
COPY requirements.txt /
RUN pip3 install -r /requirements.txt
COPY . /app
WORKDIR /app

RUN flask db init
RUN flask db migrate
RUN flask db upgrade

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]