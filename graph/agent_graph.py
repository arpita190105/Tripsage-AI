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

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT
    )

    return agent


def build_messages_with_history(chat_history: list, current_prompt: str) -> list:
    """
    Converts Streamlit session messages into LangGraph message format
    and appends the current user message.
    Keeps last 10 exchanges max to avoid token overflow.
    """
    messages = []

    # Take last 10 messages (5 exchanges) for context window safety
    recent_history = chat_history[-10:] if len(chat_history) > 10 else chat_history

    for msg in recent_history:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            messages.append(("user", content))
        elif role == "assistant":
            messages.append(("assistant", content))

    # Add current message
    messages.append(("user", current_prompt))
    return messages


def run_agent(agent, user_message: str, chat_history: list = None) -> str:
    """
    Run the agent with full conversation history for context awareness.
    Falls back gracefully on any error.
    """
    try:
        if chat_history is None:
            chat_history = []

        messages = build_messages_with_history(chat_history, user_message)
        result = agent.invoke({"messages": messages})
        return result["messages"][-1].content

    except Exception as e:
        error_msg = str(e).lower()
        if "rate limit" in error_msg:
            return "I'm getting too many requests right now. Please wait a moment and try again."
        elif "api key" in error_msg or "authentication" in error_msg:
            return "There's a connection issue. Please check the API key setup."
        elif "timeout" in error_msg:
            return "The request timed out. Please try a shorter question."
        elif "context" in error_msg or "token" in error_msg:
            # History too long — retry with just current message
            try:
                result = agent.invoke({"messages": [("user", user_message)]})
                return result["messages"][-1].content
            except Exception:
                return "Something went wrong. Please try again."
        else:
            return f"Something went wrong: Please try rephrasing your question."