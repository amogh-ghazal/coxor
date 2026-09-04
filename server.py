"""Coxor: an unnecessarily Morse-coded chat server."""

import json
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from audio import write_wav
from morse import morse_to_text, text_to_morse

ROOT = Path(__file__).parent
AUDIO_DIR = ROOT / "generated_audio"
MESSAGES: dict[str, dict[str, str]] = {}
CLIENTS: set[WebSocket] = set()
MAX_MESSAGE_LENGTH = 500

app = FastAPI(title="Coxor")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")


@app.get("/")
async def home() -> FileResponse:
    return FileResponse(ROOT / "static" / "index.html")


@app.get("/audio/{filename}")
async def audio_file(filename: str) -> FileResponse:
    safe_name = Path(filename).name
    path = AUDIO_DIR / safe_name
    if not path.is_file() or path.suffix.lower() != ".wav":
        raise HTTPException(status_code=404, detail="Audio not found.")
    return FileResponse(path, media_type="audio/wav", filename=safe_name)


async def broadcast(event: dict) -> None:
    disconnected = set()
    for client in CLIENTS:
        try:
            await client.send_text(json.dumps(event))
        except Exception:
            disconnected.add(client)
    CLIENTS.difference_update(disconnected)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    CLIENTS.add(websocket)
    try:
        while True:
            try:
                request = json.loads(await websocket.receive_text())
            except json.JSONDecodeError:
                await websocket.send_json({"type": "error", "message": "Invalid message format."})
                continue
            request_type = request.get("type")

            if request_type == "send_message":
                text = request.get("text", "")
                if not isinstance(text, str):
                    await websocket.send_json({"type": "error", "message": "Message must be text."})
                    continue
                text = text.strip()
                if not text:
                    continue
                if len(text) > MAX_MESSAGE_LENGTH:
                    await websocket.send_json({"type": "error", "message": "Message is too long."})
                    continue
                message_id = uuid.uuid4().hex[:10]
                morse = text_to_morse(text)
                filename = f"{message_id}.wav"
                write_wav(morse, AUDIO_DIR / filename)
                MESSAGES[message_id] = {"morse": morse, "filename": filename}
                await broadcast({
                    "type": "message",
                    "message_id": message_id,
                    "audio_url": f"/audio/{filename}",
                })

            elif request_type == "decode":
                message_id = request.get("message_id")
                message = MESSAGES.get(message_id)
                if message is None:
                    await websocket.send_json({"type": "error", "message": "Message not found."})
                else:
                    await websocket.send_json({
                        "type": "decoded",
                        "message_id": message_id,
                        "text": morse_to_text(message["morse"]),
                    })
    except WebSocketDisconnect:
        CLIENTS.discard(websocket)
