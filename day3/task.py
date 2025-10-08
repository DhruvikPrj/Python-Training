# day3/task.py
import requests
import json
from pathlib import Path

API_KEY = "043a8ee4bdee48038a564239250110"
CITY = "Ahmedabad"
BASE_URL = "https://api.weatherapi.com/v1"


def get_weather(city: str, api_key: str) -> dict:
    """Call the weather API and return JSON response."""
    url = f"{BASE_URL}/forecast.json?key={api_key}&q={city}&days=1"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def save_to_file(data: dict, filename: str):
    """Save JSON data to a file."""
    path = Path(filename)
    with path.open("w") as f:
        json.dump(data, f, indent=4)


def read_from_file(filename: str) -> dict:
    """Read JSON data from a file."""
    path = Path(filename)
    with path.open() as f:
        return json.load(f)


def extract_info(data: dict) -> dict:
    """Extract location, temp, and condition from API response."""
    return {
        "location": data["location"]["name"],
        "country": data["location"]["country"],
        "temp": data["current"]["temp_c"],
        "condition": data["current"]["condition"]["text"]
    }


# Only run if script is executed directly
if __name__ == "__main__":
    try:
        data = get_weather(CITY, API_KEY)
        print("API Response:", data)

        # Save to file
        save_to_file(data, "weather.json")

        # Read back and extract info
        saved_data = read_from_file("weather.json")
        info = extract_info(saved_data)
        print(f"📍 {info['location']}, {info['country']}")
        print(f"🌡️ Temperature: {info['temp']}°C")
        print(f"🌥️ Condition: {info['condition']}")

    except Exception as e:
        print("Something went wrong:", e)
