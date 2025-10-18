import json
import datetime


with open("../data/data.json", "r") as file:
    weather_data = json.load(file)


wind_points = weather_data["observationalGraphs"]["wind"]["dataConfig"]["series"]["groups"][0]["points"]


first_timestamp = wind_points[0]["x"]
last_timestamp = wind_points[-1]["x"]

# fix timestamp issues later.
first_date = datetime.datetime.fromtimestamp(first_timestamp)
last_date = datetime.datetime.fromtimestamp(last_timestamp)

print("Station:", weather_data["location"]["name"])
print("First reading:", first_date)
print("Last reading:", last_date)
