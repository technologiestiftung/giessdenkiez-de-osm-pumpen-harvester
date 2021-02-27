#!/usr/bin/env python3
import requests
import pandas as pd
import geopandas as gp
from shapely.geometry import Point
from utils import get_overpass_gdf, transform_dataframe

import os
import sys
import json

# TODO: [GDK-12] how to properly use coverage

# TODO: [GDK-13] move folder creation into own function
def folder_creation(path):
    path.parent.mkdir(parents=True, exist_ok=True)

# TODO: [GDK-17] Wrap requests into a new function and test that it gives us back a JSON
def get_raw_data(query):
    """Get raw text data of pumps from Overpass API."""
    response = requests.get(query)
    return response

# TODO: [GDK-14] move file writing into own function
    # save result as geojson
def write_df_to_json(cleaned_gdf, outpath):
    """Save resulting geodataframe to a .json-file in outpath directory."""
    cleaned_gdf.to_file(outpath, driver="GeoJSON")
    geojson = cleaned_gdf.to_json(na="null")
    minified = open(outpath + ".min.json", "w+")
    minified.write(json.dumps(json.loads(geojson), separators=(",", ":")))
    minified.close()
    print("::set-output name=file::" + outpath)

def fetch_osm_pumps(path, outpath):

    folder_creation(path)

    # specify query
    # (area["ISO3166-2"="DE-BE"][admin_level=4]; )->.searchArea;(node["man_made"="water_well"]["description"="Berliner Straßenbrunnen"](area.searchArea););
    query_string = "http://overpass-api.de/api/interpreter?data=%5Bout%3Ajson%5D%3B%28area%5B%22ISO3166%2D2%22%3D%22DE%2DBE%22%5D%5B%22admin%5Flevel%22%3D%224%22%5D%3B%29%2D%3E%2EsearchArea%3B%28node%5B%22man%5Fmade%22%3D%22water%5Fwell%22%5D%5B%22description%22%3D%22Berliner%20Straßenbrunnen%22%5D%28area%2EsearchArea%29%3B%29%3Bout%3B%3E%3Bout;"

    # get data and write to json
    raw_data = get_raw_data(query_string)
    json = raw_data.json()
    
    # transform and write to dataframe
    gdf = get_overpass_gdf(json)
    cleaned_gdf = transform_dataframe(gdf)

    write_df_to_json(cleaned_gdf,outpath)
