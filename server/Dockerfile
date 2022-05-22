FROM python:3.9.12

WORKDIR /root

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY server.py api.py ./
ENTRYPOINT gunicorn -w 1 -b 0.0.0.0:8000 server:app
