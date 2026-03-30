import streamlit as st
import random
from graph.agent_graph import create_agent, run_agent, extract_trip_memory

st.set_page_config(
    page_title="TripSage — AI Travel Planner",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 TripSage")
st.caption("Powered by TIA — Tourism Intelligence Agent")

# ── Session state ─────────────────────────────────────────────
if "messages"       not in st.session_state:
    st.session_state.messages       = []
if "is_processing"  not in st.session_state:
    st.session_state.is_processing  = False
if "trip_memory"    not in st.session_state:
    st.session_state.trip_memory    = {}   # stores destination/days/style/interests

# ── Agent (cached) ────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading TIA...")
def load_agent():
    return create_agent()

agent = load_agent()

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.header("✈️ Plan a Trip")

    destination  = st.text_input("Destination", placeholder="e.g. Kolkata, India",
                                  disabled=st.session_state.is_processing)
    days         = st.slider("Duration (days)", 1, 30, 7,
                              disabled=st.session_state.is_processing)
    travel_style = st.selectbox("Travel Style", ["Budget", "Mid-range", "Luxury"],
                                 disabled=st.session_state.is_processing)
    interests    = st.multiselect("Your Interests",
                                   ["History", "Food", "Adventure", "Beach", "Nature",
                                    "Culture", "Shopping", "Photography", "Nightlife", "Wellness"],
                                   disabled=st.session_state.is_processing)

    if st.button("🗺️ Plan My Trip", use_container_width=True,
                 disabled=st.session_state.is_processing):
        if not destination.strip():
            st.warning("Please enter a destination first.")
        else:
            interest_str = ", ".join(interests) if interests else "general sightseeing"
            query = (
                f"Plan a complete {days}-day {travel_style.lower()} trip to {destination}. "
                f"My interests are: {interest_str}. "
                f"Give me a full day-by-day itinerary, cultural tips, and a budget estimate."
            )
            # ── Store trip memory explicitly ──────────────────
            st.session_state.trip_memory = {
                "destination": destination.strip().title(),
                "days":        str(days),
                "style":       travel_style.lower(),
                "interests":   interest_str,
            }
            st.session_state.pending_query = query

    st.divider()

    # Show current trip memory in sidebar
    if st.session_state.trip_memory:
        st.markdown("**Current trip context:**")
        mem = st.session_state.trip_memory
        if mem.get("destination"):
            st.caption(f"📍 {mem['destination']}")
        if mem.get("days"):
            st.caption(f"📅 {mem['days']} days · {mem.get('style','')}")
        if mem.get("interests"):
            st.caption(f"❤️ {mem['interests']}")
        st.divider()

    st.markdown("**Quick questions:**")
    quick_questions = [
        "Best time to visit Santorini?",
        "Budget hotels in Bali for 5 nights",
        "Flights from Delhi to Bangkok in December",
        "Cultural dos and don'ts in Japan",
    ]
    for q in quick_questions:
        if st.button(q, use_container_width=True, key=q,
                     disabled=st.session_state.is_processing):
            st.session_state.pending_query = q

    st.divider()
    msg_count = len(st.session_state.messages)
    if msg_count:
        st.caption(f"💬 {msg_count} messages in session")

    if st.button("🗑️ Clear Chat", use_container_width=True,
                 disabled=st.session_state.is_processing):
        st.session_state.messages      = []
        st.session_state.trip_memory   = {}
        st.session_state.is_processing = False
        st.rerun()

# ── Display chat history ──────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Query handler ─────────────────────────────────────────────
LOADING_MESSAGES = [
    "Consulting travel databases...",
    "Planning your trip...",
    "Finding best options...",
    "Checking destinations...",
]

def handle_query(prompt: str):
    prompt = prompt.strip()
    if not prompt or len(prompt) < 3:
        st.warning("Please ask a more detailed question!")
        return
    if len(prompt) > 2000:
        st.warning("Question too long — keep it under 2000 characters.")
        return
    if st.session_state.is_processing:
        return

    st.session_state.is_processing = True

    # If this message contains a new destination, update trip memory
    new_mem = extract_trip_memory(prompt)
    if new_mem.get("destination"):
        st.session_state.trip_memory.update(new_mem)

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"TIA — {random.choice(LOADING_MESSAGES)}"):
            response = run_agent(
                agent,
                prompt,
                trip_memory=st.session_state.trip_memory
            )
        st.markdown(response)

    st.session_state.messages.append({"role": "user",      "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.is_processing = False

# ── Handle pending query ──────────────────────────────────────
if "pending_query" in st.session_state and not st.session_state.is_processing:
    query = st.session_state.pop("pending_query")
    handle_query(query)

# ── Chat input ────────────────────────────────────────────────
if not st.session_state.is_processing:
    if prompt := st.chat_input("Ask TIA anything about travel..."):
        handle_query(prompt)
else:
    st.chat_input("TIA is thinking...", disabled=True)