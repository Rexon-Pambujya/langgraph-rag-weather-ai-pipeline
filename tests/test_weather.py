import pytest
from unittest.mock import patch
from src.weather import fetch_weather_by_city


@patch('src.weather.requests.get')
def test_fetch_weather_by_city(mock_get):
    class FakeResp:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "name": "London",
                "sys": {"country": "GB"},
                "main": {"temp": 15, "humidity": 80},
                "weather": [{"description": "light rain"}],
                "wind": {"speed": 5}
            }
    mock_get.return_value = FakeResp()
    result = fetch_weather_by_city("London")
    assert result['city'] == "London"
    assert result['country'] == "GB"
    assert result['temperature'] == 15
    assert result['description'] == "light rain"
    assert result['humidity'] == 80
    assert result['wind_speed'] == 5
    