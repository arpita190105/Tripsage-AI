from langchain.tools import tool

@tool
def cultural_guide(destination: str) -> str:
    """Provides cultural etiquette, customs, dos and don'ts, and safety 
    advice for a travel destination. Use this when the user asks about 
    culture, customs, etiquette, local rules, or safety.

    Args:
        destination: The travel destination
    """
    return (
        f"Provide a detailed cultural guide for {destination} covering: "
        f"1) Local customs and social etiquette "
        f"2) Dress code (general and for religious/cultural sites) "
        f"3) Dos and Don'ts — at least 5 of each "
        f"4) Tipping culture and norms "
        f"5) Common tourist mistakes to avoid "
        f"6) Useful local phrases (greetings, thank you, help, excuse me) "
        f"7) Religious and cultural sensitivities "
        f"8) General safety tips and areas to be cautious about"
    )