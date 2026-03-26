from langchain.tools import tool

@tool
def budget_estimator(destination: str, days: int, travel_style: str) -> str:
    """Estimates a travel budget for a trip with category-wise breakdown.
    Use this when the user asks about cost, budget, expenses, or money needed.

    Args:
        destination: Travel destination
        days: Number of days (integer)
        travel_style: One of 'budget', 'mid-range', or 'luxury'
    """
    return (
        f"Create a detailed {travel_style} travel budget for {days} days in {destination}. "
        f"Break down daily and total costs for: "
        f"1) Accommodation (per night) "
        f"2) Food (breakfast, lunch, dinner separately) "
        f"3) Local transportation "
        f"4) Attraction entry fees "
        f"5) Shopping and souvenirs "
        f"6) Miscellaneous and emergency buffer "
        f"Provide totals in both USD and INR. "
        f"Add 2-3 money-saving tips specific to {destination}."
    )