FROM python:3.11-slim

RUN pip install tinytuya paho-mqtt

COPY run.py /run.py

CMD ["python", "/run.py"]
