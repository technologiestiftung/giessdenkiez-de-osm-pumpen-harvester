FROM python:3.6.8-stretch
WORKDIR /scripts
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY fetch_osm_pumps.py fetch_osm_pumps.py

ENTRYPOINT [ "./fetch_osm_pumps.py" ]