import requests
from pydantic import BaseModel, Field
import datetime
import openai
from langchain.agents import tool
from dotenv import load_dotenv, find_dotenv
import os
import wikipedia
from pydantic import BaseModel, Field
from config import *

from langchain_community.tools import BraveSearch




load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
BRAVESEARCH_API_KEY = os.getenv("BRAVESEARCH_API_KEY")


# the input schema
class OpenMeteoInput(BaseModel):
    latitude: float = Field(..., description="Latitude of the location to fetch weather data for")
    longitude: float = Field(..., description="Longitude of the location to fetch weather data for")

@tool
def search_wikipedia(query: str) -> str:
    """Run Wikipedia search and get page summaries."""
    page_titles = wikipedia.search(query)
    summaries = []
    for page_title in page_titles[: 3]:
        try:
            wiki_page =  wikipedia.page(title=page_title, auto_suggest=False)
            summaries.append(f"Page: {page_title}\nSummary: {wiki_page.summary}")
        except (
            self.wiki_client.exceptions.PageError,
            self.wiki_client.exceptions.DisambiguationError,
        ):
            pass
    if not summaries:
        return "No good Wikipedia Search Result was found"
    return "\n\n".join(summaries)

@tool(args_schema=OpenMeteoInput)
def get_current_weather(latitude: float, longitude: float) -> dict:

    """Fetch current temperature for given coordinates."""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    # Parameters for the request
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m',
        'forecast_days': 1,
    }

    # Make the request
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        results = response.json()
    else:
        raise Exception(f"API Request failed with status code: {response.status_code}")

    current_utc_time = datetime.datetime.utcnow()
    time_list = [datetime.datetime.fromisoformat(time_str.replace('Z', '+00:00')) for time_str in results['hourly']['time']]
    temperature_list = results['hourly']['temperature_2m']
    
    closest_time_index = min(range(len(time_list)), key=lambda i: abs(time_list[i] - current_utc_time))
    current_temperature = temperature_list[closest_time_index]
    
    return f'The current temperature is {current_temperature}°C'


def get_current_time(location: str) -> str:
    try:
        timezone = pytz.timezone(f"America/{location}")
        current_time = datetime.now(timezone)
        return f"The current time in {location} is {current_time.strftime('%I:%M %p')}"
    except pytz.exceptions.UnknownTimeZoneError:
        return f"Error: Unable to find timezone for {location}"


def get_weather(location: str) -> str:
    weather_data = {
        "location": location,
        "local_time": "2024-12-27 18:07",
        "current_temperature_f": 48,
        "current_temperature_c": 9,
        "current_humidity": 86,
        "current_condition": {
            "text": "Light rain",
            "icon": "drizzle",
            "code": "1183"
        },
        "current_wind_mph": 9,
        "current_wind_direction": "SSW",
        "current_visibility_miles": 9,
        "current_pressure_inches": 29,
        "current_precipitation_inches": 0,
        "current_cloud_cover_percentage": 100,
        "forecast": {
            "today": "Moderate rain",
            "tomorrow": "Overcast",
            "day_after_tomorrow": "Heavy rain"
        }
    }

    output = (
        f"Weather in {weather_data['location']}:\n"
        f"Local time: {weather_data['local_time']}\n"
        f"Current temperature: {weather_data['current_temperature_f']}°F ({weather_data['current_temperature_c']}°C)\n"
        f"Current humidity: {weather_data['current_humidity']}%\n"
        f"Condition: {weather_data['current_condition']['text']}\n"
        f"Wind: {weather_data['current_wind_mph']} mph to the {weather_data['current_wind_direction']}\n"
        f"Visibility: {weather_data['current_visibility_miles']} miles\n"
        f"Pressure: {weather_data['current_pressure_inches']} inches\n"
        f"Cloud cover: {weather_data['current_cloud_cover_percentage']}%\n"
        f"Forecast for today: {weather_data['forecast']['today']}\n"
        f"Forecast for tomorrow: {weather_data['forecast']['tomorrow']}\n"
        f"Forecast for the day after tomorrow: {weather_data['forecast']['day_after_tomorrow']}"
    )

    return output


@tool 
def get_brave_online_search(query : str) -> str : 
    """Run Brave search and get page summaries."""
    tool = BraveSearch.from_api_key(api_key=BRAVESEARCH_API_KEY, search_kwargs={"count": 3})
    output = tool.run(query)
    return output 



class TavilyDBChecker:
    def __init__(self):
        self.tavily_api = TavilySearchAPIWrapper()

    def check_query(self, query: str) -> tuple:
        print(f"Performing Tavily Web Search for query: {query}")
        try:
            response = self.tavily_api.search(query)
            if response and response.get("relevant_count", 0) > 0:
                return True, response.get("relevance_score", 0.0)
        except Exception as e:
            print(f"Tavily search error: {e}")
        return False, 0.0
