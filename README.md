🎓 DSU Student Helper Chatbot

A domain-specific Retrieval-Augmented Generation (RAG) chatbot designed to assist students and parents with queries related to Dayananda Sagar University (DSU).

It uses Google Gemini 1.5 Flash for reasoning and HuggingFace Embeddings (running locally) for accurate, cost-effective data retrieval.

📂 Project Structure

dsu-chatbot/
├── .streamlit/
│   └── secrets.toml      # API Keys (Create this file manually)
├── db/                   # Local Vector Database (Created by ingest.py)
├── venv/                 # Virtual Environment folder
├── app.py                # Main Application Code (Streamlit UI)
├── ingest.py             # Data Processing Script (Builds the DB)
├── knowledge.txt         # The Source Data (Facts about DSU)
└── requirements.txt      # List of Python Dependencies


⚙️ Prerequisites

Python 3.10 or higher installed on your system.

A Google AI Studio API Key (Free tier is sufficient). Get it here.

🚀 Installation Guide

Step 1: Clone or Download

Download this project folder to your computer and open it in VS Code.

Step 2: Create a Virtual Environment

Open your terminal (Ctrl + `) and run the following commands:

# 1. Create the environment
python -m venv venv

# 2. Activate it
# On Windows:
.\venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate


Step 3: Install Dependencies

With the environment activated (venv), install the required libraries:

pip install -r requirements.txt


Step 4: Set up API Keys (Security)

Create a new folder named .streamlit inside the main project folder.

Inside that folder, create a file named secrets.toml.

Open secrets.toml and paste your Google API key like this:

GOOGLE_API_KEY = "AIzaSy.....(Your Key Here)....."


🏃‍♂️ How to Run the Project

1. Build the Knowledge Base (One-Time Setup)

Run this script to read your knowledge.txt, chunk the data, and create the vector database. You only need to do this once (or if you edit the text file).

python ingest.py


Wait until you see the message: "Successfully added... chunks to the database".

2. Launch the Chatbot

Run the main web application:

streamlit run app.py


Your default web browser should automatically open with the chatbot running!

🛠️ Troubleshooting Common Issues

Issue 1: "sqlite3" error on Windows

If the app crashes with RuntimeError: Your system has an unsupported version of sqlite3:

Go to sqlite.org/download.html.

Download sqlite-dll-win-x64-....zip.

Extract the sqlite3.dll file.

Paste it into this folder in your project: dsu-chatbot/venv/Scripts/.

Issue 2: "404 Model Not Found"

If the chatbot says the model is not found:

Open app.py.

Ensure the model name is specific: model="gemini-1.5-flash-001" (instead of just gemini-1.5-flash).

Issue 3: Blank Screen

Check your terminal for errors.

Try refreshing the browser page (Ctrl + R).

Ensure you have run python ingest.py at least once before running the app.