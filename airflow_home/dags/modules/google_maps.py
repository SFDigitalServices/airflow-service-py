# pylint: disable=fixme
"""Functions related to interacting with Form.io forms."""
import os
import requests

from modules.core import Core

# pylint: disable=too-few-public-methods
class GoogleMaps(Core):
    """Functions related to interacting with Form.io forms."""

    @staticmethod
    def geocode(
            city,
            state,
            api_key=os.environ.get('GOOGLE_MAPS_API_KEY'),
            url='https://maps.googleapis.com/maps/api/geocode/json'
        ):
        """Get geocoded city and state."""

        params = {
            'address': '{city},{state}'.format(city=city, state=state),
            'key': api_key
        }
        try:
            response = requests.get(
                url,
                params=params
            )
            response.raise_for_status()
        except requests.HTTPError:
            print('Error with GoogleMaps request: ', response.text)
            # We don't want getting county to break the flow.
            return None

        results = response.json().get('results', None)

        return results[0] if results else None

    @staticmethod
    def get_county_from_geocode(geocode_result):
        """Given a geocoded address, retreive the county."""
        item = [
            val for val in geocode_result['address_components']
            if 'administrative_area_level_2' in val['types']
        ]
        return item[0]['long_name']
