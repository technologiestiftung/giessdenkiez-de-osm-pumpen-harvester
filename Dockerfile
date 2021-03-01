FROM python:3.6.8-slim-stretch
WORKDIR /usr
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY harvester/* harvester/
RUN chmod +x /usr/harvester/main.py
ENTRYPOINT ["python", "/usr/harvester/main.py" ]