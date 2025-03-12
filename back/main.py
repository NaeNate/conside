import shutil
import uuid
from pathlib import Path

import whisper
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
)

model = whisper.load_model("base")


@app.post("/api/transcribe")
async def transcribe(audio: UploadFile):
    filename = f"{uuid.uuid4()}.webm"
    audio_path = Path("audio_chunks") / filename
    audio_path.parent.mkdir(exist_ok=True)

    with audio_path.open("wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    transcription = model.transcribe(str(audio_path))
    audio_path.unlink()

    return {"text": transcription["text"]}
