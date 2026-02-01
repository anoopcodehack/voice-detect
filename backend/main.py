from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import base64
import io
import os
import random
import numpy as np
import librosa

app = FastAPI(title="AI Voice Detection API", version="1.0.0")

# ================= CONFIG =================
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY environment variable must be set")

SUPPORTED_LANGUAGES = [
    "Tamil",
    "English",
    "Hindi",
    "Malayalam",
    "Telugu",
]

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= SCHEMA =================
class VoiceRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str

# ================= UTILS =================
def extract_features(audio_bytes: bytes):
    y, sr = librosa.load(io.BytesIO(audio_bytes), sr=None)

    pitch = librosa.yin(y, fmin=50, fmax=400)
    pitch_var = np.nanstd(pitch)

    spectral_flatness = np.mean(librosa.feature.spectral_flatness(y=y))
    zcr = np.mean(librosa.feature.zero_crossing_rate(y))
    rms = np.mean(librosa.feature.rms(y=y))

    return pitch_var, spectral_flatness, zcr, rms


def classify_voice(pitch_var, flatness, zcr, rms):
    """
    Heuristic-based signal analysis:
    AI voices tend to have:
    - Very stable pitch
    - Higher spectral flatness
    - Lower energy variation
    """

    ai_score = 0

    if pitch_var < 15:
        ai_score += 1
    if flatness > 0.25:
        ai_score += 1
    if zcr < 0.05:
        ai_score += 1
    if rms < 0.03:
        ai_score += 1

    confidence = min(0.55 + (ai_score * 0.1), 0.95)

    if ai_score >= 3:
        return "AI_GENERATED", confidence, "Unnaturally stable pitch and synthetic spectral patterns detected"
    else:
        return "HUMAN", confidence, "Natural pitch variation and human speech dynamics detected"


def is_mp3(data: bytes) -> bool:
    """Basic MP3 validity check: ID3 header or MP3 frame sync.

    This is a lightweight check to catch obvious non-MP3 payloads without full decoding.
    """
    if not data or len(data) < 100:
        return False
    # ID3v2 tag
    if data[:3] == b"ID3":
        return True
    # Frame sync (0xFFF) check: first byte 0xFF and top 3 bits of second byte set
    if data[0] == 0xFF and (data[1] & 0xE0) == 0xE0:
        return True
    return False

# ================= ROUTES =================
@app.get("/")
def root():
    return {"message": "AI Voice Detection API Running"}

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"status": "error", "message": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"status": "error", "message": "Invalid request payload"})


@app.post("/api/voice-detection")
def detect_voice(payload: VoiceRequest, x_api_key: str = Header(None)):
    # API key check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key or malformed request")

    if payload.language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail="Unsupported language")

    if payload.audioFormat.lower() != "mp3":
        raise HTTPException(status_code=400, detail="Only mp3 format supported")

    try:
        audio_bytes = base64.b64decode(payload.audioBase64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Base64 audio")

    # Validate it's an MP3 file before trying to analyze
    if not is_mp3(audio_bytes):
        raise HTTPException(status_code=400, detail="Invalid MP3 file")

    try:
        pitch_var, flatness, zcr, rms = extract_features(audio_bytes)
        classification, confidence, explanation = classify_voice(pitch_var, flatness, zcr, rms)
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to process audio")

    return {
        "status": "success",
        "language": payload.language,
        "classification": classification,
        "confidenceScore": round(confidence, 2),
        "explanation": explanation,
    }

