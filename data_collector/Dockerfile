FROM python:3.8

WORKDIR /

COPY requirements.txt .
COPY / data_collector

RUN pip install -r requirements.txt

CMD ["python3", "-u", "data_collector/main.py"]