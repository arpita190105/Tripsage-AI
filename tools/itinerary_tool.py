from langchain.tools import tool

@tool
def build_itinerary(destination: str, days: int, interests: str) -> str:
    """Creates a detailed day-by-day travel itinerary.
    Use this when the user wants a trip plan, schedule, or itinerary.

    Args:
        destination: The travel destination
        days: Number of days for the trip (integer)
        interests: Traveler's interests e.g. 'history, food, adventure, beach'
    """
    return (
        f"Create a detailed {days}-day travel itinerary for {destination}. "
        f"Traveler interests: {interests}. "
        f"For each day provide: "
        f"- Morning activity with timing and location "
        f"- Afternoon activity with timing and location "
        f"- Evening activity or dinner recommendation "
        f"- One local tip or insider advice for that day "
        f"End with: packing suggestions, best transport options, "
        f"and 3 pro tips for this specific destination."
    )