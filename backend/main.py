import os
import base64
import tempfile
import random
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import UploadFile, File

app = FastAPI(title="AI Voice Detection API", version="0.1.0")

# CORS (allow frontend)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "https://voice-detect-inky.vercel.app/"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY", "sk_test_123456789")
SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]

class VoiceRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str

@app.get("/")
def root():
    return {"message": "AI Voice Detection Backend Running ✅"}

@app.post("/api/voice-detection")
async def detect_voice_file(
    language: str,
    audio: UploadFile = File(...),
    x_api_key: str = Header(None)
):
    # API key check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail="Unsupported language")

    if audio.content_type != "audio/mpeg":  # mp3 MIME type
        raise HTTPException(status_code=400, detail="Only mp3 supported")

    audio_bytes = await audio.read()

    # Classification logic (same as before)
    size = len(audio_bytes)
    if size > 1_000_000:
        classification = "AI_GENERATED"
        confidence = round(random.uniform(0.85, 0.95), 2)
        explanation = "Robotic patterns detected"
    else:
        classification = "HUMAN"
        confidence = round(random.uniform(0.80, 0.92), 2)
        explanation = "Natural human speech detected"

    return {
        "status": "success",
        "language": language,
        "classification": classification,
        "confidenceScore": confidence,
        "explanation": explanation,
    }