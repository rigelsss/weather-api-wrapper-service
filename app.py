from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from weather_client import fetch_weather
from weather_client import CityNotFoundError, WeatherAPIError, WeatherAPITimeout
from cache import get_cached_weather, set_cached_weather
from config import REDIS_HOST, REDIS_PORT

app = Flask(__name__)


limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per hour"],
    storage_uri=f"redis://{REDIS_HOST}:{REDIS_PORT}",
)


@app.errorhandler(CityNotFoundError)
def handle_city_not_found_error(error):
    return jsonify({"error": str(error)}), 404 

@app.errorhandler(WeatherAPIError)
def handle_weather_api_error(error):
    return jsonify({"error": str(error)}), 502

@app.errorhandler(WeatherAPITimeout)
def handle_weather_api_timeout(error):
    return jsonify({"error": str(error)}), 504

@app.errorhandler(429)
def handle_rate_limit_exceeded(error):
    return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429

@app.route("/weather/<city>", methods=["GET"])
@limiter.limit("5 per minute")
def get_weather(city):
    cached_weather = get_cached_weather(city)
    if cached_weather is not None:
        return jsonify(cached_weather)
    
    weather_data = fetch_weather(city)
    set_cached_weather(city, weather_data)
    
    return jsonify(weather_data)
        
    
if __name__ == "__main__":
    app.run(debug=True)