FROM python:3.6.8-slim-stretch
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY fetch_osm_pumps.py fetch_osm_pumps.py
RUN chmod +x fetch_osm_pumps.py
ENTRYPOINT ["python", "./fetch_osm_pumps.py" ]