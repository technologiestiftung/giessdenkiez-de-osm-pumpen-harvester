# Giessdenkiez.de Pumpen aggregation from OSM

Build the container and run it.

```bash
docker build --tag technologiestiftung/giessdenkiez-de-osm-pumpen .
docker run -v $PWD/out:/scripts/out technologiestiftung/giessdenkiez-de-osm-pumpen
```