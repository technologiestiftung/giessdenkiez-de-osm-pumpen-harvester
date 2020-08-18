import requests
import pandas as pd
import geopandas as gp
from shapely.geometry import Point


def get_overpass_gdf(query_string):

    # Retrieve URL contents
    r = requests.get(query_string)
    # print(r.json())
    # Make dataframe
    df = pd.DataFrame(r.json()['elements'])

    # Make geodataframe
    df['geometry'] = [Point(xy) for xy in zip(df.lon, df.lat)]
    df = gp.GeoDataFrame(df, geometry='geometry')

    return df


# Specify query
query_string = "http://overpass-api.de/api/interpreter?data=%5Bout%3Ajson%5D%3B%28area%5B%22ISO3166%2D2%22%3D%22DE%2DBE%22%5D%5B%22admin%5Flevel%22%3D%224%22%5D%3B%29%2D%3E%2EsearchArea%3B%28node%5B%22man%5Fmade%22%3D%22water%5Fwell%22%5D%5B%22description%22%3D%22Berliner%20Straßenbrunnen%22%5D%28area%2EsearchArea%29%3B%29%3Bout%3B%3E%3Bout;"

# Export to GeoJSON
gdf = get_overpass_gdf(query_string)
print(gdf)
gdf.to_file("out/query_results.geojson", driver="GeoJSON")
