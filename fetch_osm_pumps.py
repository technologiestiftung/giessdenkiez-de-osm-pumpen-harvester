#!/usr/bin/env python3
import requests
import pandas as pd
import geopandas as gp
from shapely.geometry import Point
from module.utils import get_overpass_gdf, transform_dataframe
from pathlib import Path
import argparse
import os
import sys
import json

# TODO: [GDK-12] how to properly use coverage
parser = argparse.ArgumentParser(
    description="Process OSM pumps data for giessdenkiez.de"
)
parser.add_argument(
    "outpath", metavar="O", help="The outputpath for the pumps.geojson file"
)

args = parser.parse_args()

path = Path(args.outpath)


def fetch_osm_pumps(path, outpath):
    # TODO: [GDK-13] move folder creation into own function
    path.parent.mkdir(parents=True, exist_ok=True)

    # specify query
    # (area["ISO3166-2"="DE-BE"][admin_level=4]; )->.searchArea;
    # (node["man_made"="water_well"]["description"="Berliner Straßenbrunnen"](area.searchArea););
    query_string = "http://overpass-api.de/api/interpreter?data=%5Bout%3Ajson%5D%3B%28area%5B%22ISO3166%2D2%22%3D%22DE%2DBE%22%5D%5B%22admin%5Flevel%22%3D%224%22%5D%3B%29%2D%3E%2EsearchArea%3B%28node%5B%22man%5Fmade%22%3D%22water%5Fwell%22%5D%5B%22description%22%3D%22Berliner%20Straßenbrunnen%22%5D%28area%2EsearchArea%29%3B%29%3Bout%3B%3E%3Bout;"

    # get data
    r = requests.get(query_string)

    gdf = get_overpass_gdf(r.json())
    cleaned_gdf = transform_dataframe(gdf)
    # transform tag-dictionary to columns
    # TODO: [GDK-14] move file writing into own function
    # save result as geojson
    cleaned_gdf.to_file(outpath, driver="GeoJSON")
    geojson = cleaned_gdf.to_json(na="null")
    minified = open(outpath + ".min.json", "w+")
    minified.write(json.dumps(json.loads(geojson), separators=(",", ":")))
    minified.close()
    print("::set-output name=file::" + outpath)
    # sys.exit()


if __name__ == "__main__":
    fetch_osm_pumps(path, args.outpath)
