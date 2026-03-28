from langchain.tools import tool

@tool
def flight_guidance(origin: str, destination: str, travel_month: str, travel_class: str) -> str:
    """Provides flight planning guidance, tips, and cost estimates for a trip.
    Use this when the user asks about flights, airlines, getting there,
    air travel, airports, or transport to the destination.

    Args:
        origin: Departure city or country e.g. 'Mumbai, India'
        destination: Arrival city or country e.g. 'Tokyo, Japan'
        travel_month: Month of travel e.g. 'October'
        travel_class: One of 'economy', 'business', or 'first'
    """
    return (
        f"Provide flight planning guidance from {origin} to {destination} "
        f"for {travel_class} class travel in {travel_month}. Structure as:\n\n"
        f"**Estimated fare:** Price range in USD and INR (round trip).\n\n"
        f"**Best airlines:** Top 2-3 airlines for this route with one reason each.\n\n"
        f"**Airports:** Main airports at origin and destination, terminals if notable.\n\n"
        f"**Booking tips:**\n"
        f"- Best time to book for lowest prices\n"
        f"- Direct vs connecting flights tradeoff\n"
        f"- Any budget airline options\n\n"
        f"**Getting from airport to city:** Main options (metro, taxi, bus) with cost.\n\n"
        f"Keep the entire response under 250 words."
    )