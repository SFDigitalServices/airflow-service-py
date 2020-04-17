"""Test functions from modules/acuity"""
import json

from modules.google_maps import GoogleMaps

def test_get_county():
    """Verify that we can extract county info if present."""
    with open('airflow_home/dags/tests/mocks/sample_geocode_response.json', 'r') as geocode_file:
        mock_response = json.load(geocode_file)
        county = GoogleMaps.get_county_from_geocode(mock_response)
    assert county == 'San Mateo County'
