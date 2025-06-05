# 🧠 AI-Powered Product Discovery System

PulseNeuro is an intelligent, full-stack beauty product recommendation platform that combines LLM agentic workflows (`neuron/`), a FastAPI backend (`pulse/`), a Vite + React frontend (`echo/`), and a SQLite3 database (`db.sqlite3`). It’s built for fast experimentation, user interaction, and AI-enhanced product reasoning.

---

## 🗂️ Project Structure

```
.
├── db.sqlite3                # SQLite database with products and reviews
├── echo/                    # Frontend (Vite + React)
├── neuron/                  # Agentic LLM logic using CrewAI (deprecated)
├── pulse/                   # FastAPI backend (includes actual neuron agents)
├── scripts/                 # Data ingestion and review CSV generation
```

---

## 🚀 Quickstart

### 🧪 Option 1: Local Dev (Manual)

#### 1. Install backend dependencies

```bash
cd pulse
uv venv --seed
source .venv/bin/activate
uv sync
```

#### 2. Run the backend

```bash
cd pulse
uvicorn main:app --reload
```

#### 3. Install frontend dependencies and start dev server

```bash
cd echo
npm install
npm run dev
```

#### 4. Set up the database

Note: This step can be omitted if you already have the `db.sqlite3` file

Use the scripts in `scripts/data_ingestion/` to populate the SQLite database.

```bash
python insert_beauty_products.py
python insert_user_reviews.py
```

---

### 🐳 Option 2: One-Click Docker Compose Setup

Make sure Docker and Docker Compose are installed. Then, run:

```bash
docker compose up --build
```

This will start:

- 🧠 Redis (or Valkey)
- 🔙 FastAPI backend at [http://localhost:8000](http://localhost:8000)
- 🌐 Vite frontend at [http://localhost:5173](http://localhost:5173)

SQLite is mounted from the host at `./db.sqlite3`.

---

## 🧠 Neuron Agents

The `pulse/neuron/` directory contains autonomous agents orchestrated via [CrewAI](https://docs.crewai.com/). These agents retrieve product data, parse user context, and generate intelligent justifications for recommendations.

### Configuration

- `pulse/neuron/config/agents.yaml` – Defines agent roles
- `pulse/neuron/config/tasks.yaml` – Task flows

Run Neuron independently or as part of the backend:

```bash
cd pulse
python main.py
```

---

## 💻 Frontend (`echo/`)

- Built with Vite + React
- Components live in `src/components/`
- `HomePage.jsx` renders search, results, and AI explanations

---

## 📦 Scripts

Some script that you most probably don’t require.

- `insert_beauty_products.py` — Ingests beauty product data
- `insert_user_reviews.py` — Loads verified user reviews
- `reviews_csv_generation.py` — Generates formatted CSVs

---

## 🔐 Env Files

Make sure you have an `.env` file in the `pulse/` directory with the following content:

```env
NEURON_PACKAGE_ROOT_DIR="../neuron/src"
PRODUCTS_SQLITE_DATABASE_PATH="../db.sqlite3"
PRODUCTS_DB_PATH="../db.sqlite3"
PRODUCTS_TABLE_NAME="beauty_products"
REVIEWS_DB_PATH="../db.sqlite3"
REVIEWS_TABLE_NAME="user_reviews"
MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
REDIS_URL=redis://redis:6379
```

In `echo/.env`:

```env
VITE_API_URL="http://localhost:8000"
```

---

## 🧼 TODO

- Add tests for LLM agents
- Improve error handling on frontend
- Add user login & saved recommendations

---

## 🧊 License

MIT License – do whatever you want but don’t sue me if your AI becomes sentient.

---
