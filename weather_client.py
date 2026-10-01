import requests
from config import VISUAL_CROSSING_API_KEY
from urllib.parse import quote

API_KEY = VISUAL_CROSSING_API_KEY
URL_BASE = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
MAX_TIMEOUT = 10  # seconds

class CityNotFoundError(Exception):
    """A API não reconheceu a cidade informada."""


class WeatherAPIError(Exception):
    """Falha ao falar com a API externa (fora do ar, chave inválida, limite excedido...)."""


class WeatherAPITimeout(WeatherAPIError):
    """A API externa demorou demais para responder."""

def fetch_weather(city):
    
    url = f"{URL_BASE}/{quote(city)}"
    params = {
        "unitGroup": "metric",
        "include": "current",
        "contentType": "json",
        "key":  API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=MAX_TIMEOUT)
    except requests.exceptions.Timeout:
        raise WeatherAPITimeout("Weather provider timed out")
    except requests.exceptions.RequestException:
        raise WeatherAPIError("Could not connect to the weather provider")
    
    if response.status_code == 400:
        raise CityNotFoundError(f"City '{city}' not found")
    if response.status_code in (401, 403):
        raise WeatherAPIError("Weather provider rejected the API key")
    if response.status_code == 429:
        raise WeatherAPIError("Weather provider rate limit exceeded")
    if response.status_code != 200:
        raise WeatherAPIError(f"Weather provider error ({response.status_code})")

    data = response.json()
    current = data["currentConditions"]
    
    return {
        "city": data["resolvedAddress"],
        "temperature": current["temp"],
        "conditions": current["conditions"],
        "humidity": current["humidity"],
        "source": "visualcrossing",
    }