from langgraph.prebuilt import create_react_agent
from utils.helpers import get_llm
from tools.destination_tool import destination_info
from tools.itinerary_tool import build_itinerary
from tools.cultural_guide_tool import cultural_guide
from tools.budget_tool import budget_estimator
from tools.hotel_tool import hotel_recommendations
from tools.flight_tool import flight_guidance
from prompts.system_prompt import SYSTEM_PROMPT

try:
    from tools.search_tool import web_search
    WEB_SEARCH_AVAILABLE = True
except Exception:
    WEB_SEARCH_AVAILABLE = False

try:
    from tools.weather_tool import get_weather
    WEATHER_AVAILABLE = True
except Exception:
    WEATHER_AVAILABLE = False

try:
    from tools.scoring_tool import score_destination
    SCORING_AVAILABLE = True
except Exception:
    SCORING_AVAILABLE = False


def create_agent():
    llm = get_llm()

    tools = [
        destination_info,
        build_itinerary,
        cultural_guide,
        budget_estimator,
        hotel_recommendations,
        flight_guidance,
    ]

    if WEB_SEARCH_AVAILABLE:
        tools.append(web_search)
    if WEATHER_AVAILABLE:
        tools.append(get_weather)
    if SCORING_AVAILABLE:
        tools.append(score_destination)

    return create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT
    )


def build_context_prefix(trip_memory: dict) -> str:
    """
    Build a clean context prefix from explicitly stored trip memory.
    This replaces the unreliable regex extraction approach.
    trip_memory is a dict stored in st.session_state.trip_memory
    """
    if not trip_memory:
        return ""

    lines = ["[CURRENT TRIP CONTEXT — always use this for follow-up questions]"]
    if trip_memory.get("destination"):
        lines.append(f"Destination: {trip_memory['destination']}")
    if trip_memory.get("days"):
        lines.append(f"Duration: {trip_memory['days']} days")
    if trip_memory.get("style"):
        lines.append(f"Travel style: {trip_memory['style']}")
    if trip_memory.get("interests"):
        lines.append(f"Interests: {trip_memory['interests']}")
    lines.append("[END CONTEXT]")
    return "\n".join(lines) + "\n\n"


def extract_trip_memory(user_message: str) -> dict:
    """
    Extract trip entities from a message and return as a clean dict.
    Only runs when a new trip plan is explicitly requested.
    Called from main.py when sidebar Plan button is used.
    """
    import re
    memory = {}

    msg = user_message.lower()

    # Destination — look for "trip to X" or "visit X"
    patterns = [
        r"trip to ([a-zA-Z][a-zA-Z\s,]{2,40}?)[\.\,\?]",
        r"visit(?:ing)? ([a-zA-Z][a-zA-Z\s,]{2,40}?)[\.\,\?]",
        r"itinerary.*?for ([a-zA-Z][a-zA-Z\s,]{2,40}?)[\.\,\?]",
        r"plan.*?to ([a-zA-Z][a-zA-Z\s,]{2,40}?)[\.\,\?]",
    ]
    for p in patterns:
        m = re.search(p, msg)
        if m:
            memory["destination"] = m.group(1).strip().title()
            break

    # Days
    m = re.search(r"(\d+)[- ]day", msg)
    if m:
        memory["days"] = m.group(1)

    # Style
    for s in ["budget", "mid-range", "midrange", "luxury"]:
        if s in msg:
            memory["style"] = s
            break

    # Interests
    known = ["food", "history", "culture", "nature", "beach",
             "adventure", "shopping", "photography", "wellness", "nightlife"]
    found = [i for i in known if i in msg]
    if found:
        memory["interests"] = ", ".join(found)

    return memory


def run_agent(agent, user_message: str, trip_memory: dict = None) -> str:
    """
    Run agent with explicit trip memory context.
    Fast — sends only ~100 tokens of context instead of full history.
    """
    try:
        context_prefix = build_context_prefix(trip_memory or {})
        full_message = context_prefix + user_message

        result = agent.invoke({
            "messages": [("user", full_message)]
        })
        return result["messages"][-1].content

    except Exception as e:
        err = str(e).lower()
        if "rate limit" in err:
            return "Rate limit hit — please wait 10 seconds and try again."
        elif "api key" in err or "auth" in err:
            return "API key error — check your GROQ_API_KEY in .env."
        elif "timeout" in err:
            return "Request timed out — try a simpler question."
        else:
            return "Something went wrong. Please try again or clear the chat."