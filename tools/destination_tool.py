from langchain.tools import tool

@tool
def destination_info(destination: str) -> str:
    """Get overview, attractions, cuisine, and travel tips for a destination.
    Args: destination: city or country name"""
    return (
        f"Provide a concise travel guide for {destination}: "
        f"top 5 attractions, must-try local foods, best areas to stay, "
        f"getting around, and 3 insider tips. Keep it structured and brief."
    )