Quickstart Checklist

Files included:

- create-synova-project.py # creates project structure under synova-ai-platform/
- requirements.txt # Python dependencies
- main.py # FastAPI demo backend
- terrestrial.html # Simple front-end UI (open in browser)
- start.sh # Unix start script (uses uvicorn)
- start.bat # Windows start script

Quick steps (Windows):

1. Install Python 3.11+ and add to PATH
2. Open PowerShell in this folder: cd c:\Users\Fuzzy\synova-ai-project
3. (optional) python -m venv synova-env; synova-env\Scripts\activate
4. pip install -r requirements.txt
5. start.bat (or) python -m uvicorn main:app --host 0.0.0.0 --port 8000
6. Open terrestrial.html in your browser and use the chat UI
