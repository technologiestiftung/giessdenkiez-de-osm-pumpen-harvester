import json

from utils import create_folder, get_raw_data, get_overpass_gdf, transform_dataframe, write_df_to_json


def fetch_osm_pumps(path, outpath):

    create_folder(path)

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
