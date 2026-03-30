from langchain.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()

# Try Tavily first, fall back to DuckDuckGo only if unavailable
TAVILY_KEY = os.getenv("TAVILY_API_KEY")

if TAVILY_KEY:
    from langchain_community.tools.tavily_search import TavilySearchResults
    _search_engine = TavilySearchResults(
        max_results=3,              # 3 results is enough — fewer = faster
        tavily_api_key=TAVILY_KEY
    )
    def _run_search(query):
        results = _search_engine.invoke(query)
        if not results:
            return "No results found."
        return "\n\n".join(
            f"Result {i+1}: {r['content']}\nSource: {r['url']}"
            for i, r in enumerate(results)
        )
else:
    # Fallback — basic DuckDuckGo with timeout protection
    from langchain_community.tools import DuckDuckGoSearchRun
    _ddg = DuckDuckGoSearchRun()
    def _run_search(query):
        try:
            return _ddg.run(query)
        except Exception:
            return "Search unavailable right now. Using general knowledge instead."


@tool
def web_search(query: str) -> str:
    """Searches the internet for real-time travel information.
    Use ONLY for: current visa requirements, live travel advisories,
    recent news, upcoming events at a destination.
    Do NOT use for general destination info — use destination_info instead.

    Args:
        query: Specific search e.g. 'visa requirements Indians visiting Japan 2025'
    """
    try:
        return _run_search(query)
    except Exception as e:
        return f"Search failed: {str(e)}. Using general knowledge instead."