import requests
import os
from dotenv import load_dotenv

load_dotenv()


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self._endpoint = os.getenv("SHEET_ENDPOINT")
        self._token = os.getenv("SHEET_TOKEN")
        self.headers = {
            "Authorization": self._token,
        }
        self.prices = self.get_data()

    def get_data(self):
        response = requests.get(self._endpoint, headers=self.headers)
        data = response.json()
        return data["prices"]

    def update_iatacode(self, row_id, airport_code):
        update_data = {
            "prices": {
                "iataCode": airport_code,
            }
        }
        response = requests.put(url=f"{self._endpoint}/{row_id}", json=update_data, headers=self.headers)

        # print(f"Update status code: {response.status_code}")
        if response.status_code == 200:
            print(f"Update successful for row {row_id}")
        else:
            print(f"Failed to update row {row_id}, Response: {response.text}")

