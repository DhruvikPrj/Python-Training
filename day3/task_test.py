# day3/test_task.sh.py
import pytest
from unittest.mock import patch
from day3.task import get_weather, extract_info, save_to_file, read_from_file
import json

import json
from pathlib import Path

# Fake API response
fake_api_response = {
    "location": {"name": "Ahmedabad", "country": "India"},
    "current": {"temp_c": 32, "condition": {"text": "Sunny"}}
}

def test_extract_info():
    result = extract_info(fake_api_response)
    assert result["location"] == "Ahmedabad"
    assert result["country"] == "India"
    assert result["temp"] == 32
    assert result["condition"] == "Sunny"

@patch("day3.task.requests.get")
def test_get_weather(mock_get):
    # Mock the API response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = fake_api_response

    result = get_weather("Ahmedabad", "fake_api_key")
    assert result["location"]["name"] == "Ahmedabad"
    assert result["current"]["temp_c"] == 32

def test_save_and_read_file(tmp_path):
    # Use temporary file for test
    file_path = tmp_path / "weather.json"

    save_to_file(fake_api_response, file_path)
    read_data = read_from_file(file_path)
    assert read_data["location"]["name"] == "Ahmedabad"
    assert read_data["current"]["condition"]["text"] == "Sunny"
