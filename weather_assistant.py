"""
at this part I call json library so python can handle json format
then I call datetime to take a real time
finally I call request to connect with internet
"""
import json
from datetime import datetime
import requests #external module

"""
basics & collection
I declaring configuration constants the latitude and longitude of cities in Vietnam
at here I use API from open-meteo.com because it's free and easy to use
"""
API_URL = "https://api.open-meteo.com/v1/forecast"
FILE_NAME = "outfit_suggestions.txt"

CITIES = {
    "Hanoi": {"lat": 21.0285, "lon": 105.8542},
    "Ho Chi Minh": {"lat": 10.8231, "lon": 106.6297},
    "Dalat": {"lat": 11.9404, "lon": 108.4583}
}


"""
Conditional statements
I create a simple condition logic for the app so it can know if the weather is hot or cold and if it is raining
I use "+=" to add more suggestion into give_suggestions if it's raining
"""
def give_suggestions(temperature, rainfall):
    if temperature < 15:
        suggestions = "It's cold! Wear a thick sweater, a windbreaker, and a scarf."
    elif temperature < 22:
        suggestions = "It's getting chilly. Long-sleeved T-shirts and a light jacket are a good choice."
    elif temperature < 30:
        suggestions = "The weather is cool. T-shirts, jeans, or skirts are perfect."
    else:
        suggestions = "It's very hot! Wear light, breathable clothing and remember to apply sunscreen."

    if rainfall > 0:
        suggestions += f" ⚠️ It's raining ({rainfall} mm), remember to bring an umbrella/raincoat!"

    return suggestions


"""
Internet & JSON
"def weather_conditions" is responsible for calling API, receiving the connection session and coordinates
from line 58 to 64 I use AI to create a function that if the internet is lost during the taking weather inform
-ation action, the app won't be crash
"""
def weather_conditions(session, lat, lon):
    parameters = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,wind_speed_10m,precipitation"
    }
    try:
        response = session.get(API_URL, params=parameters, timeout=10)
        response.raise_for_status()
        return response.json().get("current", {})
    except requests.exceptions.RequestException as loi:
        print(f"❌ no connections with internet: {loi}")
        return None


"""
Writing and reading file
"""
def save_file(list_of_reports):
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(FILE_NAME, "a", encoding="utf-8") as file:
        file.write(f"=== REPORT AT {time} ===\n")
        file.writelines(list_of_reports)
        file.write("\n")


def read_file():
    print("\n📂 HISTORICAL CONTENT IN FILE:")
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            print(file.read())
    except FileNotFoundError:
        print("No history file has been created yet.")


"""
Main fucntion
"""
# this function creates an empty list that acts as a basket containing news from each city after each loop
def run_app():
    print("🌤️ Weather data is being collected...\n")
    # collections
    list_of_reports = []

    with requests.Session() as session: # open a connection with internet, faster than calling request.get() one by one
        # loops to seperate city and coordinate
        for city, coordinate in CITIES.items():
            data = weather_conditions(session, coordinate["lat"], coordinate["lon"])

            if not data: # if the current city has a network error, pass that city
                continue

            temperature = data.get("temperature_2m") # take number from dictionary
            rainfall = data.get("precipitation")

            suggests = give_suggestions(temperature, rainfall)

            news = (
                f"📍 {city}: {temperature}°C  | Rainfall: {rainfall} mm\n"
                f"💡 Suggestions: {suggests}\n"
            )
            list_of_reports.append(news) # place the completed news article at the end of the list.
#AI suggest me from line 115 to 121 to help the app run smoothly
    if list_of_reports: #check if there are missing any file. if no, the program then save history to a file and read it back
        save_file(list_of_reports)
        read_file()


if __name__ == "__main__": #Python's standard launch port
    run_app()
