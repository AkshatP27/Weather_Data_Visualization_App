import requests
import streamlit as st

# OpenWeatherMap API Key - Use secrets for deployment
try:
    API_KEY = st.secrets["OPENWEATHER_API_KEY"]
except:
    API_KEY = "843e9c13211ccb7d50123f309ef15457"  # Fallback for local testing

def fetch_weather_data(city=None, lat=None, lon=None):
    """
    Fetches weather and forecast data based on the city name or latitude and longitude.

    Args:
        city (str): Name of the city.
        lat (float): Latitude (optional).
        lon (float): Longitude (optional).

    Returns:
        dict: Dictionary containing weather and forecast data.
    """
    try:
        # Base URLs
        weather_url = "https://api.openweathermap.org/data/2.5/weather"
        forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

        params = {"appid": API_KEY, "units": "metric"}
        
        # Determine query parameters
        if city:
            params["q"] = city
        elif lat and lon:
            params["lat"] = lat
            params["lon"] = lon
        else:
            return {"error": "Please provide a city name or latitude and longitude."}

        # Fetch current weather data
        print("Fetching weather data...")
        weather_response = requests.get(weather_url, params=params)
        print("Weather API Response:", weather_response.json())  # Debugging print

        if weather_response.status_code != 200:
            return {"error": f"Error fetching weather data: {weather_response.json().get('message')}"}
        weather_data = weather_response.json()

        # Extract latitude and longitude from weather data
        latitude = weather_data["coord"]["lat"]
        longitude = weather_data["coord"]["lon"]

        # Fetch forecast data
        print("Fetching forecast data...")
        forecast_params = params.copy()
        forecast_response = requests.get(forecast_url, params=forecast_params)
        print("Forecast API Response:", forecast_response.json())  # Debugging print

        forecast_data = forecast_response.json() if forecast_response.status_code == 200 else None

        # Convert wind speed from m/s to km/h and round to 2 decimal places
        wind_speed_kmh = round(weather_data["wind"]["speed"] * 3.6, 2)

        # Prepare the final data dictionary
        data = {
            "main": weather_data["main"],
            "weather": weather_data["weather"],
            "wind": {"speed": wind_speed_kmh},
            "forecast": forecast_data["list"] if forecast_data else None,
        }
        print("Final Data Prepared:", data)  # Debugging print
        return data

    except Exception as e:
        print("An unexpected error occurred:", str(e))  # Debugging print
        return {"error": f"An unexpected error occurred: {str(e)}"}
