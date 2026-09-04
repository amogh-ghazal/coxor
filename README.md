# Coxor

Coxor is a deliberately useless web chat app. It turns every message into Morse code, generates a 1000 Hz WAV file, and makes another browser press **Decode** to get the text back.

## Run locally

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py -m unittest
uvicorn server:app --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000` on the host laptop. To use a second laptop on the same Wi-Fi, open `http://HOST-LAN-IP:8000` in its browser. Find the host IP with `ipconfig`.

The message notification contains only a message ID and audio URL. The server keeps the Morse representation in memory, and Decode converts that stored Morse back into text. No database, microphone, cloud service, API key, or paid deployment is required.

## Structure

- `server.py` — FastAPI routes, WebSocket connections, and in-memory messages.
- `morse.py` — text/Morse conversion.
- `audio.py` — standard-library WAV generation.
- `static/` — the vanilla browser interface.
- `test_morse.py` — small beginner-friendly tests.
