import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("TWILIO_TOKEN")
phone_number = os.getenv("PHONE_NUMBER")


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, stops):
        self.price = price
        self.origin_airport_code = origin_airport
        self.destination_airport_code = destination_airport
        self.outbound_date = out_date
        self.return_date = return_date
        self.stops = stops

    def send_sms(self):
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=f"- Low price alert! Only £{self.price} to fly from {self.origin_airport_code} "
                 f"to {self.destination_airport_code}, on {self.outbound_date} until {self.return_date} "
                 f"number of stops: {self.stops}",
            to=phone_number
        )

        print(message.sid)
