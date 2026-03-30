from langchain.tools import tool

@tool
def hotel_recommendations(destination: str, budget_level: str, duration: int) -> str:
    """Recommend hotels and accommodation areas.
    Args: destination: city/country, budget_level: budget/mid-range/luxury, duration: nights"""
    return (
        f"Recommend accommodation for {duration} nights in {destination} "
        f"({budget_level}): best 2-3 areas to stay with reasons, "
        f"3 specific hotel/hostel names with price per night in USD and INR, "
        f"and 2 booking tips. Keep under 200 words."
    )