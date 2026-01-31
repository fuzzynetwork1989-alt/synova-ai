# How to create the Synova AI demo app

This guide explains how to set up, run, and extend the Synova AI demo app included in this repository.

## Prerequisites

- Python 3.10+ installed and available on PATH
- Optional: virtualenv / venv for a clean environment

## Files in the project

- `main.py` — FastAPI demo server (sqlite persistence)
- `requirements.txt` — Python dependencies
- `terrestrial.html` — Single-file frontend demo (localStorage persistence, export/import)
- `start.sh` / `start.bat` — helper scripts to start the server
- `tests/test_main.py` — pytest unit tests for the backend

## Quick start (Windows)

1. Open PowerShell and cd into the project folder:

   cd C:\Users\Fuzzy\synova-ai-project

2. (Optional) Create and activate a virtual environment:

   python -m venv synova-env
   .\synova-env\Scripts\Activate.ps1

3. Install dependencies:

   python -m pip install --upgrade pip
   pip install -r requirements.txt

4. Start the backend server:

   python -m uvicorn main:app --host 0.0.0.0 --port 8000

5. Open the frontend:

- Double-click `terrestrial.html` (may be subject to file:// CORS restrictions)
- Or serve the folder and open `http://localhost:8080/terrestrial.html`:

  python -m http.server 8080

## Running tests

From project root:

    pytest -q

## Exporting and importing chat history

- Use the Export button in the UI to download `synova_chat_history.json`.
- Use Import to select a JSON file and reload the UI with the imported conversation.

## Extending the app

- Integrate a real LLM (OpenAI, Anthropic): modify `main.py` to call APIs in `generate_response()`.
- Add authentication, user accounts and per-user databases.
- Improve the frontend look and accessibility.

---

If you want this guide as a PDF, run the included mkpdf.py script which uses ReportLab to render the markdown to a simple PDF.
