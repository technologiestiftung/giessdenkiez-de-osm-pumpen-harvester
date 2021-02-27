"""This is a gathering of fixtures."""

from pathlib import Path
import pytest
import geopandas as gpd
from shapely.geometry import Point


@pytest.fixture
def path_fixture():
    return Path("test/test.json")

@pytest.fixture
def query_fixture():
    return "http://overpass-api.de/api/interpreter?data=%5Bout%3Ajson%5D%3B%28area%5B%22ISO3166%2D2%22%3D%22DE%2DBE%22%5D%5B%22admin%5Flevel%22%3D%224%22%5D%3B%29%2D%3E%2EsearchArea%3B%28node%5B%22man%5Fmade%22%3D%22water%5Fwell%22%5D%5B%22description%22%3D%22Berliner%20Straßenbrunnen%22%5D%28area%2EsearchArea%29%3B%29%3Bout%3B%3E%3Bout;"

@pytest.fixture
def response_fixture():
    return {
        "elements": [
            {
                "type": "node",
                "id": 1536825810,
                "lat": 52.4946464,
                "lon": 13.2782614,
                "tags": {
                    "colour": "green;blue",
                    "description": "Berliner Straßenbrunnen",
                    "emergency": "drinking_water",
                    "image": "File:Grunewald Trabener Straße 85D Wasserpumpe.jpg",
                    "man_made": "water_well",
                    "pump": "manual",
                    "pump:type": "beam_pump",
                    "ref": "111",
                    "water_well": "pump",
                    "wikipedia": "de:Liste der Straßenbrunnen im Berliner Bezirk Charlottenburg-Wilmersdorf",
                },
            },
            {
                "type": "node",
                "id": 1539525095,
                "lat": 52.4861089,
                "lon": 13.5209044,
                "tags": {
                    "pump:status": "broken",
                    "addr:full": "Dorotheastraße/Karl-Egon-Straße 19",
                    "alt_ref": "262",
                    "depth": "29",
                    "description": "Berliner Straßenbrunnen",
                    "drinking_water:legal": "no",
                    "emergency": "drinking_water",
                    "image": "File:Stra%C3%9FenbrunnenL0055-Karlshorst-Dorotheastra%C3%9Fe-Karl-Egon_(4).jpg",
                    "man_made": "water_well",
                    "official_ref": "L0055",
                    "operator": "Bund",
                    "pump": "manual",
                    "pump:style": "modern",
                    "check_date": "2021-02-22",
                    "pump:type": "beam_pump",
                    "ref": "L55",
                    "start_date": "1993",
                    "water_well": "pump",
                    "wikipedia": "de:Liste der Straßenbrunnen im Berliner Bezirk Lichtenberg",
                },
            },
            {"lat": 52.4861089,
            "lon": 13.5209044,
            "tags": {"pump:status": "missing_beam"}},
            {"lat": 52.4861089,
            "lon": 13.5209044,
            "tags": {"pump:status": "out_of_order"}},
            {"lat": 52.4861089,
            "lon": 13.5209044,
            "tags": {"pump:status": "ok"}},
            {"lat": 52.4861089,
            "lon": 13.5209044,
            "tags": {"pump:status": "locked"}},
            {"lat": 52.4861089,
            "lon": 13.5209044,
            "tags": {"pump:status": "blocked"}},
            {"tags": {"pump_style": "has_no_lat_lon"}}
        ]
    }

@pytest.fixture
def dataframe_fixture():
    df = gpd.GeoDataFrame(data={
        "id": [352734260, 499609652],
        "lat": [52.4861089, 52.5017572],
        "lon": [13.5209044, 13.3104113],
        "addr:full": ["Schragenfeldstraße 25", "Limburger Straße 7"],
        "image": ["File:Plumpe 11 Marzahn Schragenfeldstraße-Bäckerpfuhl (8).jpg", "File:Wedding Limburger Straße Wasserpumpe.jpg"],
        "pump:style": ["Borsig", "Lauchhammer"],
        "check_date": ["unbekannt", "2020"],
        "pump:status": ["unbekannt", "funktionsfähig"]
        }
    )
    df["geometry"] = [Point(xy) for xy in zip(df.lon, df.lat)]
    df = gpd.GeoDataFrame(df, geometry="geometry")
    return df