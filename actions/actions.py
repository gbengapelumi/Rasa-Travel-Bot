# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from cgitb import text
from operator import ge
from urllib import response


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import os, requests
from utils.flight_api import get_flights_data


class ActionWeather(Action):

    def name(self) -> Text:
        return "action_weather"

    def run(self, dispatcher, tracker, domain):

        loc = tracker.get_slot("GPE")
        print(loc)
        degree_sign = "\N{DEGREE SIGN}"
        # print(dir(os.environ))

        payload = {
            "q": loc,
            "units": "metric",
            "appid": "3f79294bc2bbc47983009bceb73ee9bb",
        }
        response = requests.get(
            "http://api.openweathermap.org/data/2.5/find", params=payload
        )

        try:
            data = response.json()
            print(data)
            print(type(data))
            x = data["list"][0]

            temp = x["main"]["temp"]
            desc = x["weather"][0]["description"]
            city = x["name"]
            humidity = x["main"]["humidity"]
            wind_speed = x["wind"]["speed"]
            clouds = x["clouds"]["all"]

            weather_data = """It is {}{}C in {}. The humidity is {}%, wind speed is {} meter/sec, cloudiness in the sky is {}%, and it is {} at the moment.""".format(
                temp, degree_sign, city, humidity, wind_speed, clouds, desc
            )
            dispatcher.utter_message(weather_data)

            return [SlotSet("GPE", None)]

        except requests.exceptions.HTTPError as e:
            dispatcher.utter_message(text="City not found!")

        except Exception as e:
            dispatcher.utter_message(text="Could not find the city!")


class ActionGreetName(Action):

    def name(self) -> Text:
        return "action_greet_name"

    def run(self, dispatcher, tracker, domain):

        name = tracker.get_slot("PERSON")
        if name is not None:
            dispatcher.utter_message(text="Nice to meet you, {}!".format(name))
            return [SlotSet("PERSON", None)]

        else:
            dispatcher.utter_message(text="I see , carry on !")


class ActionFeedback(Action):
    def name(self) -> Text:
        return "action_feedback"

    def run(self, dispatcher, tracker, domain):

        intent = tracker.get_intent_of_latest_message()

        if intent == "affirm":
            return [SlotSet("feedback", True)]

        elif intent == "deny":
            return [SlotSet("feedback", False)]

        return []


class ActionGetData(Action):
    """Funtion for returning action_get_flight"""

    def name(self) -> Text:
        return "action_get_data"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Extracting the values from slots"""
        source = tracker.get_slot("source")
        destination = tracker.get_slot("destination")
        date = tracker.get_slot("date")
        """Storing the flight data into result"""
        result = get_flights_data(source, destination, date)

        if source == destination:
            dispatcher.utter_template(
                "utter_same_locations", tracker, board=source, dest=destination
            )
        """Getting only the 1st value among the list of data"""
        if len(result) > 0:
            dispatcher.utter_template(
                "utter_book_slots",
                tracker,
                date=result[0],
                arrival=result[1],
                departure=result[2],
                flight=result[3],
                board=result[4],
                dest=result[5],
                price=result[6],
                day=result[7],
                month=result[8],
            )
        else:
            """If no flights data matched"""
            dispatcher.utter_template(
                "utter_no_flight", tracker, date=date, board=source, dest=destination
            )
        return []


"""
import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionLocalSearch(Action):

    def name(self) -> Text:
        return "action_local_search"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Get the city and place_type from the slots
        city = tracker.get_slot("city")
        place_type = tracker.get_slot("place_type")
        search = tracker.get_slot(
            "search_term"
        )  # You can also fetch a specific search term if available

        access_token = "pk.eyJ1IjoicGt1bmR1MjUiLCJhIjoiY2xoaWwwNDBrMDFyaDNrcGNvMmhrZXlsaCJ9.sOxWZOMT9vWN-YyhQm4cwg"  # Replace with your actual access token

        # Construct the Mapbox API URL
        url = (
            f"https://api.mapbox.com/geocoding/v5/mapbox.places/{search}.json?"
            f"limit=10&country=in&proximity=ip&types={place_type}&access_token={access_token}"
        )

        try:
            # Make the API request
            local_search_data = requests.get(url).json()
            features = local_search_data.get("features", [])

            # Defining a list of center coordinates
            center_list = []
            city_lower = city.lower()

            # Loop through features and check if city is in place_name
            for feature in features:
                place_name = feature["place_name"].lower()
                if city_lower in place_name:
                    center_list.append(feature["center"])

            if center_list:
                # Inform the user and set the slot
                dispatcher.utter_message(
                    text=f"Found the following locations in {city}: {center_list}"
                )
                return [SlotSet("location_coordinates", center_list)]
            else:
                dispatcher.utter_message(
                    text=f"Sorry, no locations found for {search} in {city}."
                )
                return [SlotSet("location_coordinates", None)]

        except Exception as e:
            dispatcher.utter_message(
                text="There was an error retrieving the location data."
            )
            return [SlotSet("location_coordinates", None)]
            
"""
