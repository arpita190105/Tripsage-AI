import requests
import os
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
@tool
def get_weather(city: str) -> str:
    """
    Fetch weather data for a given city
    """
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return f"Error: {data.get('message', 'Unable to fetch weather')}"

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]

        return (
            f"Weather in {city}:\n"
            f"Condition: {weather}\n"
            f"Temperature: {temp}°C\n"
            f"Humidity: {humidity}%"
        )

    except Exception as e:
        return f"Weather error: {str(e)}"