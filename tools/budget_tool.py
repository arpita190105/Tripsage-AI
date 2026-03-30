from langchain.tools import tool

@tool
def budget_estimator(destination: str, days: int, travel_style: str) -> str:
    """Estimate travel budget by category.
    Args: destination: city/country, days: integer, travel_style: budget/mid-range/luxury"""
    return (
        f"Create a {travel_style} budget table for {days} days in {destination}. "
        f"Columns: Category | Per Day (USD) | Per Day (INR). "
        f"Rows: Accommodation, Food, Transport, Activities, Misc. "
        f"Add total row. End with 2 money-saving tips."
    )