from langchain.tools import tool

@tool
def hotel_recommendations(destination: str, budget_level: str, duration: int) -> str:
    """Recommends hotels, stays, and accommodation options for a destination.
    Use this when the user asks about hotels, stays, hostels, resorts,
    Airbnb, guesthouses, or where to sleep during their trip.

    Args:
        destination: The travel destination e.g. 'Bali, Indonesia'
        budget_level: One of 'budget', 'mid-range', or 'luxury'
        duration: Number of nights staying
    """
    return (
        f"Recommend accommodation for {duration} nights in {destination} "
        f"for a {budget_level} traveler. Structure your response as:\n\n"
        f"**Budget range:** Give nightly cost in USD and INR.\n\n"
        f"**Top 3 areas to stay:** Name the best neighborhoods with one reason each.\n\n"
        f"**Recommended stays:** List 3 specific hotels/hostels/resorts with:\n"
        f"- Name, type (hotel/hostel/resort/guesthouse)\n"
        f"- Approximate price per night\n"
        f"- Why it's good for this traveler\n\n"
        f"**Booking tips:** 2 tips for getting best price (e.g. book direct, best season).\n\n"
        f"Keep the entire response under 250 words."
    )