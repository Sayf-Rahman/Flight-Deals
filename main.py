# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the
# program requirements.

from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

data_manager = DataManager()  # Initialises the Class
data_manager.get_data()  # Runs the method within its Class
flight_search = FlightSearch()
flight_data = FlightData()

sheet_data = data_manager.prices

for row in sheet_data:
    if row["iataCode"] == "":
        airport_data = flight_search.get_airport_code(row["city"])
        iataCode = airport_data["data"][0]["iataCode"]
        row["iataCode"] = iataCode
        data_manager.update_iatacode(row["id"], iataCode)
    else:
        iataCode = row["iataCode"]

    flights = flight_search.get_flight_data(iataCode, is_direct="true")
    flight_data.process_flight_data(flights)

    if float(flight_data.price) <= 300:
        notification_manager = NotificationManager(
            flight_data.price,
            flight_data.origin_airport_code,
            flight_data.destination_airport_code,
            flight_data.outbound_date,
            flight_data.return_date,
            flight_data.stops,
        )
        notification_manager.send_sms()
