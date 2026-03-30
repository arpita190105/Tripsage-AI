from langchain.tools import tool

@tool
def flight_guidance(origin: str, destination: str, travel_month: str, travel_class: str) -> str:
    """Get flight tips, airline recommendations, and fare estimates.
    Args: origin: departure city, destination: arrival city,
          travel_month: e.g. October, travel_class: economy/business/first"""
    return (
        f"Flight guide from {origin} to {destination} in {travel_month} ({travel_class}): "
        f"fare range USD and INR, top 2 airlines with reason, "
        f"airport names, best booking timing, airport-to-city transport options. "
        f"Keep under 200 words."
    )