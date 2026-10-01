from flask import Flask, jsonify
from weather_client import fetch_weather
from weather_client import CityNotFoundError, WeatherAPIError, WeatherAPITimeout

app = Flask(__name__)


@app.errorhandler(CityNotFoundError)
def handle_city_not_found_error(error):
    return jsonify({"error": str(error)}), 404 

@app.errorhandler(WeatherAPIError)
def handle_weather_api_error(error):
    return jsonify({"error": str(error)}), 502

@app.errorhandler(WeatherAPITimeout)
def handle_weather_api_timeout(error):
    return jsonify({"error": str(error)}), 504

@app.route("/weather/<city>", methods=["GET"])
def get_weather(city):
    weather_data = fetch_weather(city)
    return jsonify(weather_data)
        
    
if __name__ == "__main__":
    app.run(debug=True)