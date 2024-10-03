import requests


def standardize_city_name(city: str) -> str:
    """Standardize city names to their proper format.

    Args:
        city (str): Input city name.

    Returns:
        str: Standardized city name.
    """
    city = city.lower().strip()  # Normalize case and remove leading/trailing spaces
    city_map = {"delhi": "New Delhi", "bangalore": "Bengaluru", "ben": "Bengaluru"}
    return city_map.get(
        city, city.title()
    )  # Return standardized name or capitalized input


def get_flights_data(source: str, destination: str, date: str) -> list:
    """
    Retrieve flight data from Google Apps Script API.

    Args:
        source (str): Source city
        destination (str): Destination city
        date (str): Date (YYYY-MM-DD)

    Returns:
        list: Filtered flight data or an empty list if no flights are found.
    """
    # Standardize source and destination city names
    source = standardize_city_name(source)
    destination = standardize_city_name(destination)

    # API endpoint for flight data (ensure your API key is included if needed)
    url = "https://script.google.com/macros/s/AKfycbz4UWiBtBs4fm31X7kwcnFa5OT9ci6xU2YVTIOta79VF608Xju9Alg0XrnByvuq/exec?action=getflights"

    try:
        # Send GET request to the API
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.RequestException as e:
        print(f"Error: {e}")
        return []

    try:
        # Parse the JSON response
        data = response.json()
    except ValueError:
        print("Error parsing JSON response")
        return []

    result = []
    # Filter flights based on source, destination, and date
    for flight in data:
        # Uncomment the following line for date filtering
        # if flight.get("Date").split("T")[0] == date:
        if (
            flight.get("Source") == source
            and flight.get("Destination") == destination
            and flight.get("Date").split("T")[0]
            == date  # Ensure this line is uncommented for date filtering
        ):
            # Append relevant flight information to the result list
            result.append(
                [
                    flight["Date"].split("T")[0],
                    flight["ArrivalTime"].split("T")[1].split(".")[0],
                    flight["Departure Time"].split("T")[1].split(".")[0],
                    flight["Flight "],
                    flight["Source"],
                    flight["Destination"],
                    flight["Price"],
                    flight["Day of Week"],
                    flight["Month"],
                ]
            )

    # Return the first flight found if multiple are available, otherwise return all results
    return result[0] if len(result) > 1 else result


# Example call
test = get_flights_data(
    "Mumbai", "Bengaluru", "2023-04-06"
)  # Use the correct date format
print(test)  # Display the flight data
