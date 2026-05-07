## Multi-Agent Supply Chain Management System

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?style=plastic&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-ff4b4b?style=plastic&logo=streamlit&logoColor=white)
![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-32CD32?style=plastic)
![LangSmith](https://img.shields.io/badge/Monitoring-LangSmith-FFFF00?style=plastic)

A minimal, educational **Multi-Agent Supply Chain Management System** built with Python, LangGraph, SQLAlchemy, and SQLite.  
The system focuses on **explainable decisions**, **simple architecture**, and a **thin UI for inspection** (not production use).

This project is designed as a **thin, elegant UI** on top of a **well-structured multi-agent backend**, ideal for demos, interviews, and experimentation with agentic workflows in real-world operations.

---

## Features

- **Multi-agent architecture** with distinct responsibilities:
  - **Demand Agent** – Classifies demand risk and explains its reasoning.
  - **Inventory Agent** – Decides whether to reorder and how much.
  - **Risk Agent** – Evaluates supplier and logistics risk.
  - **Logistics Agent** – Decides whether to expedite shipments.
  - **Coordinator Agent** – Synthesizes all signals into a final decision.
- **LangGraph workflow** (`create_supply_chain_graph`) that:
  - Ingests a database snapshot.
  - Runs agents in a structured flow.
  - Routes through a **decision gate** and **human approval** when needed.
- **Governance & safety layer**:
  - Risk-aware decision routing.
  - Optional human-in-the-loop approval before execution.
- **Streamlit UI**:
  - One-click “Run Supply Chain Decision Cycle”.
  - Rich visualization of state, reasoning, and final outcomes.
  - Governance metrics clearly surfaced.

---

## Project Structure

At a high level:

- **`src/`** – Core backend logic (LangGraph + agents + DB)
  - **`agents/`** – LLM agents (demand, inventory, risk, logistics, coordinator)
  - **`nodes/`** – Non-agent workflow nodes (data ingestion, decision gate, human approval, execution)
  - `graph.py` – LangGraph wiring
  - `state.py` – Shared typed workflow state
  - `llm_config.py` – Gemini + (optional) LangSmith tracing config
  - `db_init.py` / `db_service.py` / `models.py` – SQLite schema + read/write helpers
  - `backend_interface.py` – Single entry point used by the UI (`run_one_cycle`)
  - `main.py` – CLI runner (seeds DB + runs async cycles)
- **`ui/`** – Streamlit UI
  - `app.py` – Control tower UI
  - `helpers.py` – UI formatting helpers
- **`data/`** – Local SQLite database (auto-created)
  - `supply_chain.db`
- **Root**
  - `requirements.txt` – Dependencies (backend + UI)
  - `.env.example` – Environment template
  - `.env` – Your local keys/config (not committed)

---

## Architecture Overview

<p align="center">
  <img src="ui/arch_diagram.png" alt="Multi-Agent Supply Chain Management System Architecture" width="800"/>
</p>

## Getting Started

### 1. Set up environment

```bash
python3 -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows (PowerShell)
# .\\venv\\Scripts\\Activate.ps1

python3 -m pip install -r requirements.txt
```

> **Note:** `requirements.txt` includes both backend + Streamlit UI dependencies.

### 2. Configure environment variables

Create a `.env` file in the project root (same folder as `requirements.txt`) and set your model / tracing keys, e.g.:

```bash
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-1.5-flash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT="supply-chain-control-tower"
LANGCHAIN_API_KEY=your_langsmith_key_here
```

This repo uses Gemini via `langchain-google-genai` (configured in `src/llm_config.py`).

### 3. Run the Streamlit UI (recommended)

From the project root:

```bash
streamlit run ui/app.py
```

Then open the browser tab Streamlit launches (typically `http://localhost:8501`).

**First run note:** the UI calls `backend_interface.run_one_cycle`, which will automatically:
- Create the `data/` folder if missing
- Initialize the SQLite schema
- Seed demo data (only if the DB is empty)

---

## Using the UI

In the UI you can:

- Select a **Product** from the dropdown.
- Click **Run Supply Chain Decision Cycle**.
- Inspect:
  - **Supply Chain State** – inventory, suppliers, POs, shipments.
  - **Agent Reasoning** – collapsible sections for each agent’s output.
  - **Final Decision** – decision type, quantity, supplier, expedite flag, and explanation.
  - **Governance & Safety** – decision risk, whether human approval was required, and approval status.

This makes it very clear *why* the system chose a certain action, not just *what* it decided.

---

## Architecture & Flow

1. **Data Ingestion**
   - Reads the current snapshot from `supply_chain.db` (product, inventory, suppliers, POs, shipments).
2. **Agent Layer**
   - Each agent receives the shared state and writes its own reasoning / recommendations into `agent_outputs`.
3. **Coordinator Agent**
   - Consumes the individual agent outputs and produces a **final decision** and natural-language explanation.
4. **Decision Gate**
   - Evaluates risk and decides whether to:
     - **Auto-execute**, or
     - Route to **Human Approval**.
5. **Human Approval Node**
   - Represents a governance checkpoint where a human can approve or block execution.
6. **Execution Node**
   - On approval (or low-risk auto-execution), updates downstream state (e.g., placing orders) and returns execution status.

All of this is assembled into a **LangGraph `StateGraph`** in `graph.py`, which the UI calls via `backend_interface.run_one_cycle`.

---

## CLI / Backend-Only Usage

If you prefer to run the decision system without the UI (e.g., for testing or demos in a terminal), you can use:

```bash
python src/main.py
```

This will:

- Initialize + seed the SQLite database (idempotent).
- Build the LangGraph workflow.
- Run the cycle for multiple products in parallel.
- Print a structured summary to the console for each product.

---

##  Governance & Safety Notes

- The **decision gate** and **human approval node** model real-world governance:
  - High-risk decisions can require a human approver.
  - Metrics surface whether a decision needed approval and the final status.
- The UI exposes:
  - **Decision risk level**.
  - Whether **human approval was required**.
  - The **approval status** / human feedback.


---

##  Technologies Used

- **Python 3.10+** (recommended: 3.12+)
- **LangGraph** for graph-based multi-agent orchestration.
- **LangChain / langchain-google-genai** for Gemini integration.
- **SQLite + SQLAlchemy** for the supply chain data model.
- **Streamlit** for the interactive control tower UI.
- **Pydantic** for typed models and validation.

---

##  Next Steps / Ideas

- Plug into a real transactional system instead of the demo SQLite database.
- Add more products, suppliers, and realistic lead-time / risk modeling.
- Integrate external signals (e.g., logistics disruption feeds, pricing APIs).
- Add a scenario selector in the UI (e.g., “port strike”, “supplier outage”, “demand spike”).


