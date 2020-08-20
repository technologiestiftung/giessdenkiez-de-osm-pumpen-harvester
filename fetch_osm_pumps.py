import requests
import pandas as pd
import geopandas as gp
from shapely.geometry import Point

def get_overpass_gdf(query_string):

    # retrieve URL contents
    r = requests.get(query_string)
    # create dataframe
    df = pd.DataFrame(r.json()['elements'])
    # create geodataframe
    df['geometry'] = [Point(xy) for xy in zip(df.lon, df.lat)]
    df = gp.GeoDataFrame(df, geometry='geometry')

    return df


# specify query
#(area["ISO3166-2"="DE-BE"][admin_level=4]; )->.searchArea;
#(node["man_made"="water_well"]["description"="Berliner Straßenbrunnen"](area.searchArea););
query_string = "http://overpass-api.de/api/interpreter?data=%5Bout%3Ajson%5D%3B%28area%5B%22ISO3166%2D2%22%3D%22DE%2DBE%22%5D%5B%22admin%5Flevel%22%3D%224%22%5D%3B%29%2D%3E%2EsearchArea%3B%28node%5B%22man%5Fmade%22%3D%22water%5Fwell%22%5D%5B%22description%22%3D%22Berliner%20Straßenbrunnen%22%5D%28area%2EsearchArea%29%3B%29%3Bout%3B%3E%3Bout;"

# get data
gdf = get_overpass_gdf(query_string)
# transform tag-dictionary to columns
gdf = pd.concat([gdf.drop(['tags'], axis=1), gdf['tags'].apply(pd.Series)], axis=1)
# drop not required tags
gdf = gdf.drop(['lat','lon','type','description','emergency','man_made','pump','pump:type','pump:style',
    'ref','water_well','playground','addr:city','addr:postcode','fixme','name','website', 'addr:full','colour',
    'wheelchair', 'tourism', 'addr:housenumber','wikipedia', 'image','alt_ref','note','addr:street','heritage:website','lda:criteria',
    'depth', 'access', 'historic', 'mapillary','drinking_water:legal', 'operator', 'official_ref', 'ref:lda', 'heritage','artist_name',
    'heritage:operator','drinking_water','start_date','survey:date'], axis=1)
# rename tag content
gdf['pump:status'] = gdf['pump:status'].fillna('unbekannt')
gdf['pump:status'] = gdf['pump:status'].replace('broken','defekt')
gdf['pump:status'] = gdf['pump:status'].replace('ok','funktionsfähig')
# set crs
gdf.crs = 'EPSG:4326'


# save result as geojson
gdf.to_file("out/pumps.geojson", driver="GeoJSON")
