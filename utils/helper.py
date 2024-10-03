from datetime import datetime as dt
import requests


def Weather(city):
    API_key = "3f79294bc2bbc47983009bceb73ee9bb"  # "Your API Key here"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    Final_url = base_url + "appid=" + API_key + "&q=" + city + "&units=metric"
    weather_data = requests.get(Final_url).json()
    # print("_________________")
    # print(Final_url)
    # print(weather_data)
    # print("_________________")

    # return weather_data['main']
    return weather_data.get("main")


def LocalSearch(search, city, place_type):
    access_token = "pk.eyJ1IjoicGt1bmR1MjUiLCJhIjoiY2xoaWwwNDBrMDFyaDNrcGNvMmhrZXlsaCJ9.sOxWZOMT9vWN-YyhQm4cwg"
    # Search text could be "city" or "place" if place_type="place" or it could be "beach", "hotel", "hospital" etc. if place_type="poi" (point of interest)
    # `proximity` is set to the coordinates of the campus
    # `bbox` is set to encompass the place/city such as Berkeley CA
    # Final_url = "https://api.mapbox.com/geocoding/v5/mapbox.places/place.json?proximity=-122.25948,37.87221&bbox=-122.30937,37.84214,-122.23715,37.89838&access_token=" + access_token
    # print(Final_url)
    # Final_url = "https://api.mapbox.com/geocoding/v5/mapbox.places/" + city + ".json" + "?proximity=ip" + "&access_token=" + access_token
    url = (
        "https://api.mapbox.com/geocoding/v5/mapbox.places/"
        + search
        + ".json?limit=10&country=in&proximity=ip&types="
        + place_type
        + "&access_token="
        + access_token
    )

    # print(url)
    local_search_data = requests.get(url).json()
    features = local_search_data["features"]
    # print(features)

    # return local_search_data['features']

    # return local_search_data['features'][0]['center'], local_search_data['features'][0]['bbox']

    # Defining a list of center coordinates
    city = city.lower()
    center_list = []
    for i in features:
        place_name = i["place_name"].lower()

        if place_name.find(city) != -1:
            # print(place_name)
            center_list.append(i["center"])
    # print("_____________________")
    # print(center_list)

    return center_list


if __name__ == "__main__":

    place_list = ["Lagos", "Ile-Ife", "Dallas", "Ontario"]

    for p in place_list:
        l = Weather(p)
        if l is None:
            print("not found")
        else:
            print(l)
