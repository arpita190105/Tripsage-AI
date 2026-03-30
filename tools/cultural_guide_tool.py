from langchain.tools import tool

@tool
def cultural_guide(destination: str) -> str:
    """Get cultural etiquette, dos and don'ts, and safety tips.
    Args: destination: city or country name"""
    return (
        f"Give a cultural guide for {destination}: "
        f"top 5 dos, top 5 don'ts, dress code, tipping norms, "
        f"useful local phrases, and key safety tips. Keep it concise."
    )