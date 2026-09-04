# Coxor

Coxor is a deliberately useless web chat app. It turns every message into Morse code, generates a 1000 Hz WAV file, and makes another browser press **Decode** to get the text back.

## Team

- **Amogh Suresh** — backend, WebSockets, Morse/WAV pipeline, deployment
- **Adish Sai** — frontend interface, PWA experience, testing and presentation

## What to submit

Coxor is a **software project**. The GitHub repository is where the project code and README are kept; it is not the final submission form by itself.

Submit the project through the **TinkerHub Hub app**, using the same account/app used to register for Useless Projects 3.0. In the project submission form, provide both of these:

- **GitHub repository:** https://github.com/amogh-ghazal/coxor
- **Live project:** https://coxor.onrender.com

Open https://useless.tinkerhub.org/ to access the event and Hub app. Choose the Useless Projects 3.0 project submission option, select **Software**, add both team members, paste the GitHub and live links, and submit. The official handbook requires a live link and GitHub repository for software projects.

## Run locally

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py -m unittest
uvicorn server:app --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000` on the host laptop. To use a second laptop on the same Wi-Fi, open `http://HOST-LAN-IP:8000` in its browser. Find the host IP with `ipconfig`.

## Optional free deployment

The included `render.yaml` describes a free Render web service. Create a Render account, connect the `amogh-ghazal/coxor` repository, and deploy the blueprint. The free service may sleep when unused, but it is enough for a demo. The local Wi-Fi setup above remains the simplest zero-account demo.

The message notification contains only a message ID and audio URL. The server keeps the Morse representation in memory, and Decode converts that stored Morse back into text. No database, microphone, cloud service, API key, or paid deployment is required.

## Install on a phone

Coxor is also a responsive PWA. On Android, open the deployed site in Chrome and choose **Add to Home screen**. On iPhone/iPad, open it in Safari, tap **Share**, then **Add to Home Screen**. If an older Coxor tab is open, close it and reopen the link once so Safari receives the latest app shell. Windows and Mac users can continue using the normal browser website. The app shell can load offline, while live messaging still requires an internet connection.

## Structure

- `server.py` — FastAPI routes, WebSocket connections, and in-memory messages.
- `morse.py` — text/Morse conversion.
- `audio.py` — standard-library WAV generation.
- `static/` — the vanilla browser interface.
- `test_morse.py` — small beginner-friendly tests.
