from flight_search import FlightSearch
flight_search = FlightSearch()


class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self):
        self.price = "N/A"
        self.origin_airport_code = "N/A"
        self.destination_airport_code = "N/A"
        self.outbound_date = "N/A"
        self.return_date = "N/A"
        self.stops = 0

    def process_flight_data(self, flight_data):
        try:
            if not flight_data:
                flight_data = flight_search.get_flight_data(self.destination_airport_code, is_direct="false")

        except ValueError:
            if not flight_data:
                print("Flight data is empty")
            else:
                self.process_flight_data(flight_data)
                self.stops = flight_data['itinerary'][0]['numberOfStops']

        finally:
            self.price = flight_data[0]["price"]["total"]
            self.origin_airport_code = flight_data[0]["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            self.destination_airport_code = flight_data[0]["itineraries"][0]["segments"][0]["arrival"]["iataCode"]

            outbound_date = flight_data[0]["itineraries"][0]["segments"][0]["departure"]["at"]
            return_date = flight_data[0]["itineraries"][1]["segments"][0]["departure"]["at"]
            self.outbound_date = outbound_date.split("T")[0]
            self.return_date = return_date.split("T")[0]
