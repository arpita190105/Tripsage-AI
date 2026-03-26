from langgraph.prebuilt import create_react_agent
from utils.helpers import get_llm
from tools.destination_tool import destination_info
from tools.itinerary_tool import build_itinerary
from tools.cultural_guide_tool import cultural_guide
from tools.budget_tool import budget_estimator
from prompts.system_prompt import SYSTEM_PROMPT

def create_agent():
    llm = get_llm()
    
    tools = [
        destination_info,
        build_itinerary,
        cultural_guide,
        budget_estimator,
    ]
    
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT
    )
    
    return agent