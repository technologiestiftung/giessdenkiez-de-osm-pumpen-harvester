FROM python:3.9

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY harvester/* /usr/harvester/
RUN chmod +x /usr/harvester/main.py
ENTRYPOINT ["python", "/usr/harvester/main.py" ]