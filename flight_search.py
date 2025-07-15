import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
AMADEUS_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_SEARCH_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self._api_key = os.environ["AMADEUS_API_KEY"]
        self._api_secret = os.environ["AMADEUS_SECRET"]
        self.header = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self._token = self._get_new_token()

    def _get_new_token(self):
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret,
        }

        response = requests.post(url=TOKEN_ENDPOINT, data=body, headers=self.header)
        return response.json()["access_token"]

    def get_airport_code(self, city):
        airport_details = {
            "keyword": city,
            "max": 1,
            "include": "AIRPORTS"
        }

        self.header["Authorization"] = f"Bearer {self._token}"
        response = requests.get(url=AMADEUS_ENDPOINT, params=airport_details, headers=self.header)
        return response.json()

    def get_flight_data(self, city_code, is_direct):
        tomorrow_date = datetime.now().date() + timedelta(days=1)
        return_date = tomorrow_date + timedelta(days=7)
        tomorrow_date_str = tomorrow_date.strftime("%Y-%m-%d")
        return_date_str = return_date.strftime("%Y-%m-%d")
        flight_details = {
            "originLocationCode": "LON",
            "destinationLocationCode": city_code,
            "departureDate": tomorrow_date_str,
            "returnDate": return_date_str,
            "adults": 1,
            "nonStop": is_direct,
            "currencyCode": "GBP",
            "max": 1,
        }
        self.header["Authorization"] = f"Bearer {self._token}"
        response = requests.get(url=FLIGHT_SEARCH_ENDPOINT, params=flight_details, headers=self.header)

        # print(f"Update status code: {response.status_code}")
        if response.status_code == 200:
            return response.json()["data"]
        else:
            print(f"Failed to get any data. Response: {response.text}")
