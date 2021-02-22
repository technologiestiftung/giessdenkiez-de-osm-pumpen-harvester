import pytest
from utils import get_overpass_gdf, transform_dataframe
import pandas as pd
from shapely.geometry import Point


@pytest.fixture
def setup_response():
    data = {
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
            {"tags": {"pump:status": "missing_beam"}},
            {"tags": {"pump:status": "out_of_order"}},
            {"tags": {"pump:status": "ok"}},
            {"tags": {"pump:status": "locked"}},
            {"tags": {"pump:status": "blocked"}},
        ]
    }
    return data


def test_get_overpass_gdf(setup_response):
    result = get_overpass_gdf(setup_response)
    assert result["type"] is not None
    assert result["id"] is not None
    assert result["lat"] is not None
    assert result["lon"] is not None
    assert result["tags"] is not None
    assert result["geometry"] is not None
    assert isinstance(result, pd.DataFrame) == True
    assert isinstance(result["geometry"][0], Point) == True


def test_transform_dataframe(setup_response):

    gdf = get_overpass_gdf(setup_response)
    cleaned_gdf = transform_dataframe(gdf)
    assert cleaned_gdf["pump:status"][1] == "defekt"
    assert cleaned_gdf["pump:status"][0] == "unbekannt"
    assert cleaned_gdf["pump:status"][2] == "defekt"
    assert cleaned_gdf["pump:status"][3] == "defekt"
    assert cleaned_gdf["pump:status"][4] == "funktionsfähig"
    assert cleaned_gdf["pump:status"][5] == "verriegelt"
    assert cleaned_gdf["pump:status"][6] == "verriegelt"
    assert cleaned_gdf["check_date"][3] == "unbekannt"
    assert cleaned_gdf["addr:full"][0] == "unbekannt"
    assert cleaned_gdf["pump:style"][0] == "unbekannt"
    assert cleaned_gdf["check_date"][1] != "unbekannt"
    assert cleaned_gdf["addr:full"][1] != "unbekannt"
    assert cleaned_gdf["pump:style"][1] != "unbekannt"
