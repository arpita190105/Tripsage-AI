import streamlit as st
from graph.agent_graph import create_agent

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="TripSage — AI Travel Planner",
    page_icon="🌍",
    layout="wide"
)

# ── Header ────────────────────────────────────────────────────
st.title("🌍 TripSage")
st.caption("Powered by TIA — Tourism Intelligence Agent")

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.header("Plan a Trip")
    st.markdown("Fill in your preferences and click the button, or just chat below.")

    destination = st.text_input("Destination", placeholder="e.g. Tokyo, Japan")
    days = st.slider("Duration (days)", min_value=1, max_value=30, value=7)
    travel_style = st.selectbox(
        "Travel Style",
        ["Budget", "Mid-range", "Luxury"]
    )
    interests = st.multiselect(
        "Your Interests",
        ["History", "Food", "Adventure", "Beach", "Nature",
         "Culture", "Shopping", "Photography", "Nightlife", "Wellness"]
    )

    if st.button("Plan My Trip", use_container_width=True):
        if destination:
            interest_str = ", ".join(interests) if interests else "general sightseeing"
            auto_query = (
                f"Plan a complete {days}-day {travel_style.lower()} trip to {destination}. "
                f"My interests are: {interest_str}. "
                f"Give me a full day-by-day itinerary, cultural tips, and a budget estimate."
            )
            st.session_state.auto_query = auto_query
        else:
            st.warning("Please enter a destination first.")

    st.divider()
    st.markdown("**Quick questions to try:**")
    
    quick_questions = [
        "Best time to visit Santorini?",
        "Is Bali safe for solo female travelers?",
        "5-day itinerary for Paris on a budget",
        "Cultural dos and don'ts in Japan",
    ]
    
    for q in quick_questions:
        if st.button(q, use_container_width=True, key=q):
            st.session_state.auto_query = q

    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ── Initialize session state ──────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    with st.spinner("Loading TIA..."):
        st.session_state.agent = create_agent()

# ── Display chat history ──────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Handle sidebar button queries ─────────────────────────────
if "auto_query" in st.session_state:
    prompt = st.session_state.pop("auto_query")

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("TIA is planning your trip... 🌏"):
            result = st.session_state.agent.invoke(
                {"messages": [("user", prompt)]}
            )
            response = result["messages"][-1].content
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# ── Chat input ────────────────────────────────────────────────
if prompt := st.chat_input("Ask TIA anything about travel..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🌍"):
            result = st.session_state.agent.invoke(
                {"messages": [("user", prompt)]}
            )
            response = result["messages"][-1].content
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()