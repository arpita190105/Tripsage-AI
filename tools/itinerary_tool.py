from langchain.tools import tool

@tool
def build_itinerary(destination: str, days: int, interests: str) -> str:
    """Build a day-by-day travel itinerary.
    Args: destination: city/country, days: number of days, interests: comma-separated"""
    return (
        f"Create a {days}-day itinerary for {destination} "
        f"focused on: {interests}. "
        f"Format: Day N → Morning / Afternoon / Evening, one line each. "
        f"End with packing tips and 2 pro tips."
    )