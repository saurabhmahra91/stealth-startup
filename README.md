# 🧠 PulseNeuro: AI-Powered Product Discovery System

PulseNeuro is an intelligent, full-stack beauty product recommendation platform that combines LLM agentic workflows (`neuron/`), a FastAPI backend (`pulse/`), a Vite + React frontend (`echo/`), and a SQLite3 database (`db.sqlite3`). It’s built for fast experimentation, user interaction, and AI-enhanced product reasoning.

---

## 🗂️ Project Structure

```
.
├── db.sqlite3                # SQLite database with products and reviews
├── echo/                    # Frontend (Vite + React)
├── neuron/                  # Agentic LLM logic using CrewAI
├── pulse/                   # FastAPI backend
├── scripts/                 # Data ingestion and review CSV generation
```

---

## 🚀 Quickstart

### 1. Install backend dependencies

```bash
cd pulse
uv venv --seed
source .venv/bin/activate
uv sync
```

### 2. Run the backend

```bash
cd pulse
uvicorn main:app --reload
```


### 3. Install frontend dependencies and start dev server

```bash
cd echo
npm install
npm run dev
```

### 4. Set up the database

Note: This step can be omitted if you already have the db.sqlite3 file

Use the scripts in `scripts/data_ingestion/` to populate the SQLite database.

```bash
python insert_beauty_products.py
python insert_user_reviews.py
```

---

## 🧠 Neuron Agents

The `neuron/` directory contains autonomous agents orchestrated via [CrewAI](https://docs.crewai.com/). These agents retrieve product data, parse user context, and generate intelligent justifications for recommendations.

### Configuration

- `neuron/src/neuron/config/agents.yaml` - Defines agent roles
- `neuron/src/neuron/config/tasks.yaml` - Task flows

Run Neuron independently or as part of the backend:

```bash
cd neuron
python src/neuron/main.py
```

---

## 💻 Frontend (echo/)

- Built with Vite + React
- Components live in `src/components/`
- `HomePage.jsx` renders search, results, and AI explanations

---


## 📦 Scripts

Some script that you most probably dont require.

- `insert_beauty_products.py` — Ingests beauty product data
- `insert_user_reviews.py` — Loads verified user reviews
- `reviews_csv_generation.py` — Generates formatted CSVs

---

## 🔐 Env Files

Make sure you have an .env file in the pulse directory with the following content

```bash

## Path to the root directory of the Neuron package
NEURON_PACKAGE_ROOT_DIR="<parent>/neuron/src"

## Absolute path to the SQLite database storing product info
PRODUCTS_SQLITE_DATABASE_PATH="<parent>/db.sqlite3"

## Relative path to the products database (used by frontend/backend scripts)
products_db_path="../db.sqlite3"

## Table name for products
PRODUCTS_TABLE_NAME="beauty_products"

## Relative path to the reviews database (can be same as products DB)
REVIEWS_DB_PATH="../db.sqlite3"

## Table name for storing user reviews
REVIEWS_TABLE_NAME="user_reviews"

## Model name for LLM (used in backend tasks or agents)
MODEL=gpt-4o-mini

## OpenAI API key for accessing GPT models (keep this secret!)
OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```


- `google.env` and `openai.env` store respective API keys (ignored in git)

---

## 🧼 TODO

- Add tests for LLM agents
- Improve error handling on frontend
- Add user login & saved recommendations

---

## 🧊 License

MIT License – do whatever you want but don’t sue me if your AI becomes sentient.

---
