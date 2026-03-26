from langchain.tools import tool

@tool
def destination_info(destination: str) -> str:
    """Returns comprehensive travel information about a destination.
    Use this when the user asks about a place, wants to know about 
    a destination, or needs general travel information.

    Args:
        destination: The name of the travel destination (city or country)
    """
    return (
        f"Provide a comprehensive travel guide for {destination} covering: "
        f"1) Overview and why visit "
        f"2) Top 5 must-visit attractions with brief descriptions "
        f"3) Local cuisine and best dishes to try "
        f"4) Best time to visit and weather overview "
        f"5) How to get there and getting around locally "
        f"6) Accommodation areas to stay in "
        f"7) Hidden gems most tourists miss "
        f"8) Essential travel tips specific to {destination}"
    )