# 🌍 TripSage — AI Travel Planner

<div align="center">

![TripSage Banner](https://img.shields.io/badge/TripSage-AI%20Travel%20Planner-blue?style=for-the-badge&logo=airplane&logoColor=white)

**Powered by TIA — Tourism Intelligence Agent**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.3%2B-1C3C3C?style=flat-square&logo=langchain&logoColor=white)](https://langchain.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2%2B-FF6B35?style=flat-square)](https://langchain-ai.github.io/langgraph/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.4%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3-F55036?style=flat-square)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [Roadmap](#-roadmap)

</div>

---

## 📖 Overview

**TripSage** is an intelligent AI-powered travel planning assistant built using **LangChain**, **LangGraph**, and **Groq's ultra-fast LLM inference**. It brings together the expertise of a seasoned trip planner, tour operator, and cultural guide into a single conversational interface.

At its core, TripSage runs **TIA (Tourism Intelligence Agent)** — a multi-tool ReAct agent that reasons across your travel query, picks the right tools, and delivers personalized, structured travel plans in seconds.

Whether you're a solo backpacker, a family planner, or a travel agency needing intelligent automation — TripSage handles it all.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🗺️ **Destination Insights** | History, top attractions, local food, hidden gems, best time to visit |
| 📅 **Itinerary Builder** | Personalized day-by-day plans with Morning / Afternoon / Evening breakdowns |
| 🏛️ **Cultural Guide** | Dos & don'ts, etiquette, dress codes, local phrases, safety tips |
| 💰 **Budget Estimator** | Category-wise cost breakdown in USD and INR for budget / mid-range / luxury travel |
| 💬 **Conversational UI** | Streamlit chat interface with session memory |
| ⚡ **Fast Inference** | Powered by Groq (LLaMA 3.3 70B) — responses in 1-3 seconds |
| 🧠 **Multi-step Reasoning** | LangGraph ReAct agent chains multiple tools intelligently |

---

## 🎬 Demo

> Coming soon — screenshot and demo GIF will be added here after first deployment.

**Example prompts to try:**
- *"Plan a 7-day budget trip to Bali for a solo traveler interested in culture and food"*
- *"What are the cultural dos and don'ts in Japan?"*
- *"How much does a 5-day mid-range trip to Paris cost?"*
- *"Give me a 3-day itinerary for Rajasthan focused on history and photography"*

---

## 🏗️ Architecture

```
tripsage/
├── main.py                    # Streamlit app entry point
├── graph/
│   └── agent_graph.py         # LangGraph ReAct agent setup
├── tools/
│   ├── destination_tool.py    # Destination insights tool
│   ├── itinerary_tool.py      # Day-by-day itinerary builder
│   ├── cultural_guide_tool.py # Cultural etiquette & safety
│   └── budget_tool.py         # Budget estimation tool
├── prompts/
│   └── system_prompt.py       # TIA system personality & instructions
├── utils/
│   └── helpers.py             # LLM loader (Groq)
├── .env                       # API keys (not committed)
├── .gitignore
└── requirements.txt
```

### How it works

```
User Input
    │
    ▼
Streamlit Chat UI (main.py)
    │
    ▼
LangGraph ReAct Agent (agent_graph.py)
    │
    ├──► destination_info tool
    ├──► build_itinerary tool
    ├──► cultural_guide tool
    └──► budget_estimator tool
    │
    ▼
Groq LLM (LLaMA 3.3 70B)
    │
    ▼
Structured Travel Response
```

The agent uses a **ReAct (Reasoning + Acting)** pattern — it thinks about which tools to use, calls them in sequence if needed, and synthesizes a final coherent response.

---

## ⚙️ Installation

### Prerequisites
- Python 3.10 or higher
- A free [Groq API key](https://console.groq.com) (takes 2 minutes to get)
- A free [Tavily API key](https://app.tavily.com) (for web search — Phase 5)

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/your-username/tripsage.git
cd tripsage
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

> ⚠️ Never commit your `.env` file. It's already in `.gitignore`.

**5. Run the app**
```bash
streamlit run main.py
```

Open your browser at `http://localhost:8501` 🚀

---

## 📦 Dependencies

```
langchain
langgraph
langchain-groq
streamlit
python-dotenv
tavily-python
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 🧰 Tools

TripSage's agent has access to 4 core tools:

### 1. `destination_info`
Returns a comprehensive travel guide for any destination — overview, top attractions, cuisine, best time to visit, accommodation areas, hidden gems, and practical tips.

### 2. `build_itinerary`
Takes a destination, number of days, and traveler interests — returns a structured day-by-day itinerary with Morning / Afternoon / Evening breakdown, local tips, and packing suggestions.

### 3. `cultural_guide`
Covers local customs, etiquette, dress codes, dos & don'ts, tipping culture, useful local phrases, religious sensitivities, and safety advice.

### 4. `budget_estimator`
Estimates travel costs by category (accommodation, food, transport, activities, shopping, buffer) for budget / mid-range / luxury styles, in both USD and INR.

---

## 🗺️ Roadmap

- [x] Phase 1 — Project setup, folder structure, Groq LLM integration
- [x] Phase 2 — Core tools (destination, itinerary, culture, budget)
- [x] Phase 3 — LangGraph ReAct agent
- [x] Phase 4 — Streamlit chat UI with sidebar controls
- [ ] Phase 5 — Web search tool (Tavily) for real-time visa & advisory info
- [ ] Phase 5 — Weather tool (OpenWeatherMap API)
- [ ] Phase 5 — Destination scoring engine (safety, cost, crowd, weather)
- [ ] Phase 6 — PDF itinerary export (FPDF2)
- [ ] Phase 6 — Deploy on Streamlit Cloud / Hugging Face Spaces

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

Built with ❤️ as a first LangGraph agent project.

> *TripSage is an actively developed project. Star ⭐ the repo to follow along!*

---

<div align="center">
  <sub>Built with LangChain · LangGraph · Groq · Streamlit</sub>
</div>
