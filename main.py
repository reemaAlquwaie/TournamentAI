from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydub import AudioSegment
import openai
import os
import base64
import tempfile

from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def convert_audio_to_wav(file: UploadFile):
    audio = AudioSegment.from_file(file.file)
    wav_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)  # 16kHz, mono, 16-bit
    audio.export(wav_path, format="wav")
    return wav_path

@app.post("/chat")
async def chat(text: str = Form(...), audio: UploadFile = None):
    audio_b64 = None

    if audio:
        wav_path = convert_audio_to_wav(audio)
        with open(wav_path, "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode("utf-8")
        os.remove(wav_path)

    content = []
    if text:
        content.append({"type": "text", "text": text})
    if audio_b64:
        content.append({"type": "audio", "audio": {"data": audio_b64, "format": "wav"}})

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": content}]
    )

    return {"text": response["choices"][0]["message"]["content"]}
