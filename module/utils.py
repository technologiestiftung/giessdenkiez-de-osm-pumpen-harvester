import pandas as pd
import geopandas as gp
from shapely.geometry import Point


def get_overpass_gdf(json):
    """create dataframe

    Args:
        json (dict): [description]

    Returns:
       df (dataframe): Results from OSM API request as geodataframe with coordinates
    """
    # retrieve URL contents
    # r = requests.get(query_string)
    # create dataframe
    df = pd.DataFrame(json["elements"])
    # create geodataframe
    # TODO: [GDK-15] Remove rows that dont have lat or lon
    # since this wont be useful for us
    df["geometry"] = [Point(xy) for xy in zip(df.lon, df.lat)]
    df = gp.GeoDataFrame(df, geometry="geometry")
    return df


def transform_dataframe(gdf):
    """Takes geo data frame and cleans out unused values and does a reclassification,

    Args:
        gdf (DataFrame): DataFrame crated by method get_overpass_gdf

    Returns:
        DataFrame: Contains data to the pumps we actually need
    """
    gdf = pd.concat([gdf.drop(["tags"], axis=1), gdf["tags"].apply(pd.Series)], axis=1)

    # drop not required tags
    cleaned_gdf = gdf.drop(
        columns=[
            "lat",
            "lon",
            "type",
            "description",
            "emergency",
            "man_made",
            "pump",
            "pump:type",
            "ref",
            "water_well",
            "playground",
            "addr:city",
            "addr:postcode",
            "fixme",
            "name",
            "website",
            "colour",
            "wheelchair",
            "tourism",
            "addr:housenumber",
            "wikipedia",
            "alt_ref",
            "note",
            "addr:street",
            "heritage:website",
            "lda:criteria",
            "depth",
            "access",
            "historic",
            "mapillary",
            "drinking_water:legal",
            "operator",
            "official_ref",
            "ref:lda",
            "heritage",
            "artist_name",
            "heritage:operator",
            "drinking_water",
            "start_date",
            "survey:date",
        ],
        axis=1,
        errors="ignore",
    )
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
