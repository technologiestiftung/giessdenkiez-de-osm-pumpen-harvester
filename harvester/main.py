from pathlib import Path
import argparse
from fetch import fetch_osm_pumps

# TODO: [GDK-12] how to properly use coverage
parser = argparse.ArgumentParser(
    description="Process OSM pumps data for giessdenkiez.de"
)
parser.add_argument(
    "outpath", metavar="O", help="The outputpath for the pumps.geojson file"
)
parser.add_argument(
     "-q", "--query", nargs='?', required=False, help="The overpass query that is used to retrieve pumps data from OSM"
)

args = parser.parse_args()
path = Path(args.outpath)

if __name__ == "__main__":
    fetch_osm_pumps(path, args.outpath, args.query)
