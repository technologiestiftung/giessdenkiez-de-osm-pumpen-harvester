import json
import os

import pandas as pd
import geopandas as gp
import requests
from shapely.geometry import Point
import urllib.parse


def create_folder(path):
    """Create empty directory if outpath does not already exist."""
    path.parent.mkdir(parents=True, exist_ok=True)


def get_raw_data(query):
    """Get raw text data of pumps from Overpass API."""
    url = "http://overpass-api.de/api/interpreter?data=" + urllib.parse.quote_plus(query)
    response = requests.get(url)
    return response


def write_df_to_json(cleaned_gdf, outpath):
    """Save resulting geodataframe to a .json-file in outpath directory."""
    cleaned_gdf.to_file(outpath, driver="GeoJSON")
    geojson = cleaned_gdf.to_json(na="null")
    minified = open(outpath + ".min.json", "w+")
    minified.write(json.dumps(json.loads(geojson), separators=(",", ":")))
    minified.close()

    try:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
            print(f'file={outpath}', file=fh)
    except (KeyError):
        # not executed on a github CI runner; ignore this error when executed locally
        pass


def get_overpass_gdf(json):
    """Create dataframe

    Args:
        json (json): Results from OSM API as json

    Returns:
       df (dataframe): Results from OSM API request as geodataframe with coordinates
    """

    df = pd.DataFrame(json["elements"])
    df = df.dropna(subset=['lon', 'lat'])
    df["geometry"] = [Point(xy) for xy in zip(df.lon, df.lat)]
    df = gp.GeoDataFrame(df, geometry="geometry")
    return df


def transform_dataframe(gdf):
    """Takes geo data frame and cleans out unused values and does a reclassification.

    Args:
        gdf (GeoDataFrame): GeoDataFrame created by method get_overpass_gdf

    Returns:
        cleaned_gdf (GeoDataFrame): Contains only data to the pumps we actually need
    """
    gdf = pd.concat([gdf.drop(["tags"], axis=1), gdf["tags"].apply(pd.Series)], axis=1)

    # ceep only required tags
    cleaned_gdf = gdf.filter(["id", "addr:full", "image", "pump:style", "check_date","pump:status", "geometry"])
    # list of dropped columns
        #     "lat",
        #     "lon",
        #     "type",
        #     "description",
        #     "emergency",
        #     "man_made",
        #     "pump",
        #     "pump:type",
        #     "ref",
        #     "water_well",
        #     "playground",
        #     "addr:city",
        #     "addr:postcode",
        #     "fixme",
        #     "name",
        #     "website",
        #     "colour",
        #     "wheelchair",
        #     "tourism",
        #     "addr:housenumber",
        #     "wikipedia",
        #     "alt_ref",
        #     "note",
        #     "addr:street",
        #     "heritage:website",
        #     "lda:criteria",
        #     "depth",
        #     "access",
        #     "historic",
        #     "mapillary",
        #     "drinking_water:legal",
        #     "operator",
        #     "official_ref",
        #     "ref:lda",
        #     "heritage",
        #     "artist_name",
        #     "heritage:operator",
        #     "drinking_water",
        #     "start_date",
        #     "survey:date",
        #     "pump:style:Lauchhammer"
        # ]

    # TODO: [GDK-16] Notify when this happens. Since this would mean that the output from osm did change
    if "check_date" not in cleaned_gdf:
        cleaned_gdf["check_date"] = pd.Series(dtype=str)
    if "addr:full" not in cleaned_gdf:
        cleaned_gdf["addr:full"] = pd.Series(dtype=str)
    if "pump:style" not in cleaned_gdf:
        cleaned_gdf["pump:style"] = pd.Series(dtype=str)
    # rename tag content
    cleaned_gdf["pump:status"] = cleaned_gdf["pump:status"].fillna("unbekannt")
    cleaned_gdf["pump:status"] = cleaned_gdf["pump:status"].replace("broken", "defekt")

    cleaned_gdf["pump:status"] = cleaned_gdf["pump:status"].replace(
        "missing_beam", "defekt"
    )
    cleaned_gdf["pump:status"] = cleaned_gdf["pump:status"].replace(
        "out_of_order", "defekt"
    )

    cleaned_gdf["pump:status"] = cleaned_gdf["pump:status"].replace(
        "ok", "funktionsfähig"
    )

    cleaned_gdf["pump:status"] = cleaned_gdf["pump:status"].replace(
        "locked", "verriegelt"
    )
    cleaned_gdf["pump:status"] = cleaned_gdf["pump:status"].replace(
        "blocked", "verriegelt"
    )

    cleaned_gdf["check_date"] = cleaned_gdf["check_date"].fillna("unbekannt")
    cleaned_gdf["addr:full"] = cleaned_gdf["addr:full"].fillna("unbekannt")
    cleaned_gdf["pump:style"] = cleaned_gdf["pump:style"].fillna("unbekannt")
    # set crs
    cleaned_gdf.crs = "EPSG:4326"
    return cleaned_gdf
