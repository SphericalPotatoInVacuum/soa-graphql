FROM python:3.9.12

WORKDIR /root

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY client.py ./
CMD ["python3", "client.py"]
