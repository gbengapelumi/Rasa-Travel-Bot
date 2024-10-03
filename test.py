# test_actions.py
import pytest
from unittest.mock import patch
from actions.actions import ActionWeather  # Adjust based on your file structure
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

"""
def test_action_weather():
    action = ActionWeather()
    dispatcher = CollectingDispatcher()

    # Create a mock response data
    mock_weather_response = {
        "list": [
            {
                "main": {
                    "temp": 15,
                    "humidity": 80,
                },
                "weather": [{"description": "clear sky"}],
                "name": "London",
                "wind": {"speed": 5},
                "clouds": {"all": 0},
            }
        ]
    }

    tracker = Tracker(
        sender_id="test_user",
        slots={"GPE": "London"},
        latest_message={"text": "What is the weather in London?"},
        events=[],
        active_loop=None,
        paused=False,  # Add this parameter
        followup_action=None,  # Add this parameter
        latest_action_name=None,  # Add this parameter
    )

    # Mock the requests.get call to return a predefined response
    with patch("actions.actions.requests.get") as mock_get:  # Ensure correct path
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_weather_response

        # Run the action
        action.run(dispatcher, tracker, domain={})

    # Debug: Print dispatcher messages
    print("Dispatcher Messages:", dispatcher.messages)

    # Check the response
    assert dispatcher.messages  # Ensure the dispatcher sent a message

    # Extract the actual message
    actual_message = dispatcher.messages[0]["text"]

    # Debug: Print actual message for comparison
    print("Actual Message:", actual_message)

    # Check if the expected message contains key phrases
    assert (
        "15°C" in actual_message
    )  # Ensure the response includes the expected temperature
    assert (
        "London" in actual_message
    )  # Ensure the response includes the expected city name
    assert "humidity is 80%" in actual_message  # Check humidity
    assert "wind speed is 5 meter/sec" in actual_message  # Check wind speed
    assert "cloudiness in the sky is 0%" in actual_message  # Check cloudiness
    assert "it is clear sky" in actual_message  # Check description


if __name__ == "__main__":
    test_action_weather()

"""


# test_actions.py
import pytest
from unittest.mock import patch
from actions.actions import ActionLocalSearch  # Adjust based on your file structure
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher


def test_action_local_search():
    action = ActionLocalSearch()
    dispatcher = CollectingDispatcher()

    # Mock response data for Mapbox API
    mock_local_search_response = {
        "features": [
            {"place_name": "Restaurant in New York", "center": [-74.006, 40.7128]},
            {"place_name": "Cafe in New York", "center": [-74.006, 40.7128]},
        ]
    }

    tracker = Tracker(
        sender_id="test_user",
        slots={
            "city": "New York",
            "place_type": "restaurant",  # Adjust as necessary
            "search_term": "restaurant",  # Adjust as necessary
        },
        latest_message={"text": "Find me a restaurant in New York."},
        events=[],
        active_loop=None,
        paused=False,
        followup_action=None,
        latest_action_name=None,
    )

    # Mock the requests.get call to return a predefined response
    with patch(
        "actions.actions.requests.get"
    ) as mock_get:  # Ensure the path matches your actions module
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_local_search_response

        # Run the action
        action.run(dispatcher, tracker, domain={})

    # Debug: Print dispatcher messages
    print("Dispatcher Messages:", dispatcher.messages)

    # Check the response
    assert dispatcher.messages  # Ensure the dispatcher sent a message

    # Extract the actual message
    actual_message = dispatcher.messages[0]["text"]

    # Debug: Print actual message for comparison
    print("Actual Message:", actual_message)

    # Check if the expected message contains key phrases
    assert (
        "Found the following locations in New York:" in actual_message
    )  # Ensure the response indicates found locations
    assert (
        "Restaurant in New York" in actual_message
    )  # Check for a specific restaurant name
    assert "Cafe in New York" in actual_message  # Check for a specific cafe name


if __name__ == "__main__":
    pytest.main()
