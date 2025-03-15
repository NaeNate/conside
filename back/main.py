# import shutil
# import uuid
# from pathlib import Path

# import ollama
# import whisper
# from fastapi import FastAPI, UploadFile
# from fastapi.middleware.cors import CORSMiddleware
# from ollama import ChatResponse, chat

# # response: ChatResponse = chat(
# #     model="llama3.2",
# #     messages=[
# #         {
# #             "role": "user",
# #             "content": "Why is the sky blue?",
# #         },
# #     ],
# # )
# # print(response["message"]["content"])
# # or access fields directly from the response object
# # print(response.message.content)

# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
# )

# model = whisper.load_model("base")
# logs = []

# # x = ollama.embed(
# #     model="llama3.2", input="The sky is blue because of rayleigh scattering"
# # )

# # print(x)


# @app.post("/api/transcribe")
# async def transcribe(audio: UploadFile):
#     filename = f"{uuid.uuid4()}.webm"
#     audio_path = Path("audio_chunks") / filename
#     audio_path.parent.mkdir(exist_ok=True)

#     with audio_path.open("wb") as buffer:
#         shutil.copyfileobj(audio.file, buffer)

#     transcription = model.transcribe(str(audio_path))
#     audio_path.unlink()

#     logs.append(transcription["text"])

#     return {"text": transcription["text"]}


import shutil
import uuid
from pathlib import Path

import ollama
import whisper
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
)

model = whisper.load_model("base")
logs = []


def check_for_claim(log_entries):
    if not log_entries:
        return ""

    prompt = f"Determine if there is a claim in the following log entries:\n\n{log_entries}\n\nIf a claim is made, extract and return the claim and weather it is true. Otherwise, return an empty string."

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.message.content.strip()


@app.post("/api/transcribe")
async def transcribe(audio: UploadFile):
    filename = f"{uuid.uuid4()}.webm"
    audio_path = Path("audio_chunks") / filename
    audio_path.parent.mkdir(exist_ok=True)

    with audio_path.open("wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    transcription = model.transcribe(str(audio_path))
    audio_path.unlink()

    logs.append(transcription["text"])

    # Get the last three logs
    recent_logs = "\n".join(logs[-3:])

    # Check for claims in the logs
    claim = check_for_claim(recent_logs)

    return {"text": transcription["text"], "claim": claim}
