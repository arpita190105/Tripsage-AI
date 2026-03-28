from duckduckgo_search import DDGS
from langchain.tools import tool
@tool
def web_search(query: str, max_results: int = 5) -> str:
    """
    Perform a web search using DuckDuckGo
    """
    try:
        results = []
        
        with DDGS() as ddgs:
            search_results = ddgs.text(query, max_results=max_results)
            
            for res in search_results:
                results.append(
                    f"Title: {res.get('title')}\n"
                    f"Snippet: {res.get('body')}\n"
                    f"Link: {res.get('href')}\n"
                )

        return "\n\n".join(results)

    except Exception as e:
        return f"Search error: {str(e)}"