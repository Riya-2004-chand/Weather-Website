from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("OPENWEATHER_API_KEY")


@app.route("/")
def home():
    return jsonify({
        "message": "Weather Dashboard API Running"
    })




@app.route("/weather")
def weather():

    city = request.args.get("city")

    if not city:
        return jsonify({"error": "City is required"}), 400

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "City not found"}), 404

    data = response.json()

    return jsonify({

        "city": data["name"],
        "country": data["sys"]["country"],

        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "temp_min": data["main"]["temp_min"],
        "temp_max": data["main"]["temp_max"],

        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],

        "visibility": data["visibility"]/1000,

        "wind_speed": data["wind"]["speed"],

        "condition": data["weather"][0]["main"],
        "description": data["weather"][0]["description"].title(),

        "icon": data["weather"][0]["icon"],

        "sunrise": data["sys"]["sunrise"],
        "sunset": data["sys"]["sunset"],

        "latitude": data["coord"]["lat"],
        "longitude": data["coord"]["lon"]

    })




@app.route("/weather/location")
def weather_location():

    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Latitude and Longitude required"}), 400

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Location not found"}), 404

    data = response.json()

    return jsonify({

        "city": data["name"],
        "country": data["sys"]["country"],

        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "temp_min": data["main"]["temp_min"],
        "temp_max": data["main"]["temp_max"],

        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],

        "visibility": data["visibility"]/1000,

        "wind_speed": data["wind"]["speed"],

        "condition": data["weather"][0]["main"],
        "description": data["weather"][0]["description"].title(),

        "icon": data["weather"][0]["icon"],

        "sunrise": data["sys"]["sunrise"],
        "sunset": data["sys"]["sunset"],

        "latitude": data["coord"]["lat"],
        "longitude": data["coord"]["lon"]

    })





@app.route("/forecast/location")
def forecast_location():

    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error":"Latitude and Longitude required"}),400

    url=f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    response=requests.get(url)

    if response.status_code!=200:
        return jsonify({"error":"Location not found"}),404

    data=response.json()

    forecast=[]

    for item in data["list"]:

        if "12:00:00" in item["dt_txt"]:

            forecast.append({

                "date":item["dt_txt"].split()[0],

                "temperature":item["main"]["temp"],

                "description":item["weather"][0]["description"].title(),

                "icon":item["weather"][0]["icon"]

            })

            if len(forecast)==5:
                break

    return jsonify(forecast)

if __name__ == "__main__":
    app.run(debug=True)