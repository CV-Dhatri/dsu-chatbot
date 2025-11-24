# DSU Student Helper Chatbot

A domain-specific Retrieval-Augmented Generation (RAG) chatbot designed to assist students and parents with queries related to **Dayananda Sagar University (DSU)**.

This project uses **Google Gemini 1.5 Flash** for reasoning and **HuggingFace embeddings (locally-run)** for efficient, cost-effective retrieval from a local vector store.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
6. [Configuration / API Keys](#configuration--api-keys)
7. [Build the Knowledge Base (Ingest)](#build-the-knowledge-base-ingest)
8. [Run the Chatbot (Streamlit)](#run-the-chatbot-streamlit)
9. [Troubleshooting](#troubleshooting)
10. [Development notes & tips](#development-notes--tips)
11. [Contributing](#contributing)
12. [License](#license)

---

## Project Overview

The **DSU Student Helper Chatbot** is a Streamlit web application that answers DSU-related questions by combining a local vector database (built from `knowledge.txt`) with generative reasoning from Google Gemini 1.5 Flash. It is designed to be lightweight, private (data is stored locally), and easy to run for students and parents.

Key design decisions:
- Use local HuggingFace embeddings to avoid repeated external embedding costs.
- Use a lightweight local vector DB (SQLite-backed) for retrieval.
- Offload reasoning and answer generation to Google Gemini 1.5 Flash.

---

## Features

- Answer common DSU queries (admissions, departments, contacts, events, hostel info, etc.)
- Retrieval-Augmented Generation (RAG): retrieve relevant context from `knowledge.txt` and generate grounded answers
- Streamlit-based UI for quick local deployment
- Easy to update knowledge base by editing `knowledge.txt` and re-running `ingest.py`

---

## Project Structure

```
dsu-chatbot/
├── .streamlit/
│   └── secrets.toml      # API Keys (Create this file manually)
├── db/                   # Local Vector Database (Created by ingest.py)
├── venv/                 # Virtual Environment folder
├── app.py                # Main Application Code (Streamlit UI)
├── ingest.py             # Data Processing Script (Builds the DB)
├── knowledge.txt         # The Source Data (Facts about DSU)
└── requirements.txt      # List of Python Dependencies
```

---

## Prerequisites

- Python **3.10** or higher
- A Google AI Studio API Key (Gemini). The free tier is sufficient for development.
- (Optional) A working local installation of any libraries required by `requirements.txt` — see below.

---

## Installation

1. Clone or download this project folder and open it in VS Code (or your preferred IDE).

2. Create a virtual environment and activate it:

```bash
# Create the environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Mac / Linux)
source venv/bin/activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration / API Keys

Create a `.streamlit` folder inside the project root and add a `secrets.toml` file.

**Important:** Do **not** commit this file to version control. Treat it like any other secret.

Example `secrets.toml` content:

```toml
GOOGLE_API_KEY = "AIzaSy.....(Your Key Here)....."
```

If you need additional configuration (e.g., local HF model paths or embedding options), add them to `secrets.toml` or read environment variables in `app.py`/`ingest.py` as appropriate.

---

## Build the Knowledge Base (Ingest)

First-time setup (or after editing `knowledge.txt`) — build the vector DB by running the ingest script.

```bash
python ingest.py
```

What `ingest.py` does (typical flow):
1. Reads `knowledge.txt`.
2. Chunks the content into smaller passages.
3. Computes embeddings (using local HuggingFace embedding model).
4. Stores vectors + metadata into a local vector DB located under `db/`.

Wait for the success message, e.g. `Successfully added X chunks to the database`.

---

## Run the Chatbot (Streamlit)

Once the DB is built, start the Streamlit application:

```bash
streamlit run app.py
```

This will open your default browser to the local Streamlit UI. If it doesn't open automatically, visit the URL printed in the terminal (usually `http://localhost:8501`).

---

## Troubleshooting

### Issue 1: `RuntimeError: Your system has an unsupported version of sqlite3`

**Cause:** Python's bundled `sqlite3` version is older or incompatible.

**Fix:**
1. Download the precompiled Windows sqlite3 DLL from https://sqlite.org/download.html.
2. Extract `sqlite3.dll` and paste it into `dsu-chatbot/venv/Scripts/` (for a Windows virtual environment).
3. Re-run the project.

### Issue 2: `404 Model Not Found` (Gemini model error)

**Cause:** Model name used when calling the Google API is not exact.

**Fix:** Use the full model name in `app.py` such as:

```py
model = "gemini-1.5-flash-001"
```

Make sure your `GOOGLE_API_KEY` is valid and has the necessary API access.

### Issue 3: Blank screen in Streamlit

- Check the terminal where `streamlit run` is executing for traceback and error messages.
- Make sure `ingest.py` has been run at least once to create the `db/` folder with vectors.
- Try refreshing the browser (Ctrl + R) or clearing browser cache.

---

## Development notes & tips

- To update the knowledge base, edit `knowledge.txt` and re-run `python ingest.py`.
- Keep `knowledge.txt` concise and well-structured — use headings and short paragraphs for better chunking/retrieval.
- For privacy, keep the vector DB local and avoid sending `knowledge.txt` contents to third-party services.
- If you plan to scale, replace the local vector store with a hosted vector DB and consider rate limits for the Gemini API.

---

## Contributing

Contributions are welcome. Suggested steps:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feat/some-feature`.
3. Make changes and add tests where appropriate.
4. Submit a pull request with a clear description of the change.

Please ensure you do not commit API keys or other secrets.

---

## License

This project is provided as-is. Add an appropriate license file (for example, `MIT`) if you plan to publish this repository publicly.

---

## Contact / Author

For questions about this project, reach out to the maintainer (add your contact details here).


---

_Last updated: 2025-11-24_

