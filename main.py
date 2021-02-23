from pathlib import Path
import argparse
from harvester.fetch import fetch_osm_pumps

# TODO: [GDK-12] how to properly use coverage
parser = argparse.ArgumentParser(
    description="Process OSM pumps data for giessdenkiez.de"
)
parser.add_argument(
    "outpath", metavar="O", help="The outputpath for the pumps.geojson file"
)

args = parser.parse_args()
path = Path(args.outpath)

if __name__ == "__main__":
    fetch_osm_pumps(path, args.outpath)
