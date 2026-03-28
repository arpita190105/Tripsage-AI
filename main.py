import streamlit as st
from graph.agent_graph import create_agent, run_agent

st.set_page_config(
    page_title="TripSage — AI Travel Planner",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 TripSage")
st.caption("Powered by TIA — Tourism Intelligence Agent")

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.header("✈️ Plan a Trip")

    destination = st.text_input("Destination", placeholder="e.g. Tokyo, Japan")
    days = st.slider("Duration (days)", min_value=1, max_value=30, value=7)
    travel_style = st.selectbox("Travel Style", ["Budget", "Mid-range", "Luxury"])
    interests = st.multiselect(
        "Your Interests",
        ["History", "Food", "Adventure", "Beach", "Nature",
         "Culture", "Shopping", "Photography", "Nightlife", "Wellness"]
    )

    if st.button("🗺️ Plan My Trip", use_container_width=True):
        if not destination.strip():
            st.warning("Please enter a destination first.")
        else:
            interest_str = ", ".join(interests) if interests else "general sightseeing"
            st.session_state.auto_query = (
                f"Plan a complete {days}-day {travel_style.lower()} trip to {destination}. "
                f"My interests are: {interest_str}. "
                f"Give me a full day-by-day itinerary, cultural tips, and a budget estimate."
            )

    st.divider()
    st.markdown("**Quick questions:**")

    quick = [
        "Best time to visit Santorini?",
        "Budget hotels in Bali for 5 nights",
        "Flights from Delhi to Bangkok in December",
        "Cultural dos and don'ts in Japan",
        "5-day Paris itinerary on a budget",
    ]
    for q in quick:
        if st.button(q, use_container_width=True, key=q):
            st.session_state.auto_query = q

    st.divider()

    # Show context indicator
    if st.session_state.get("messages"):
        msg_count = len(st.session_state.messages)
        st.caption(f"💬 {msg_count} messages in context")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ── Session state init ────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

@st.cache_resource
def load_agent():
    return create_agent()

agent = load_agent()

# ── Chat history display ──────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Response helper ───────────────────────────────────────────
LOADING_MESSAGES = [
    "Checking destinations...",
    "Consulting travel databases...",
    "Planning your trip...",
    "Finding best options...",
    "Almost ready...",
]

def handle_query(prompt: str):
    prompt = prompt.strip()

    # Input validation
    if not prompt:
        return
    if len(prompt) < 3:
        st.warning("Please ask a more detailed travel question!")
        return
    if len(prompt) > 2000:
        st.warning("Your question is too long. Please keep it under 2000 characters.")
        return

    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response — pass history BEFORE current message was appended
    # so we pass all messages except the one we just added
    history_for_context = st.session_state.messages[:-1]

    with st.chat_message("assistant"):
        import random
        loading_msg = random.choice(LOADING_MESSAGES)
        with st.spinner(f"TIA — {loading_msg}"):
            response = run_agent(agent, prompt, chat_history=history_for_context)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# ── Auto query from sidebar ───────────────────────────────────
if "auto_query" in st.session_state:
    prompt = st.session_state.pop("auto_query")
    handle_query(prompt)

# ── Chat input ────────────────────────────────────────────────
if prompt := st.chat_input("Ask TIA anything about travel..."):
    handle_query(prompt)