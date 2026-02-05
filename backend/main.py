from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import base64
import io
import os
import librosa
import numpy as np

# ================= APP =================
app = FastAPI(title="AI Voice Detection API")

# ================= CONFIG =================
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError("API_KEY not set in environment variables")

SUPPORTED_LANGUAGES = ["English", "Hindi", "Tamil", "Telugu", "Malayalam"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= SCHEMA =================
class VoiceRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str

# ================= ERROR HANDLERS =================
@app.exception_handler(HTTPException)
async def http_error(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_error(request, exc):
    return JSONResponse(
        status_code=400,
        content={"status": "error", "message": "Invalid request payload"},
    )

# ================= UTILS =================
def is_mp3(data: bytes) -> bool:
    return data[:3] == b"ID3" or (data[0] == 0xFF and (data[1] & 0xE0) == 0xE0)

def extract_features(audio_bytes):
    y, sr = librosa.load(io.BytesIO(audio_bytes), sr=None)
    pitch = librosa.yin(y, fmin=50, fmax=400)
    pitch_var = np.nanstd(pitch)
    flatness = np.mean(librosa.feature.spectral_flatness(y=y))
    zcr = np.mean(librosa.feature.zero_crossing_rate(y))
    rms = np.mean(librosa.feature.rms(y=y))
    return pitch_var, flatness, zcr, rms

def classify(pitch_var, flatness, zcr, rms):
    score = 0
    if pitch_var < 15: score += 1
    if flatness > 0.25: score += 1
    if zcr < 0.05: score += 1
    if rms < 0.03: score += 1

    confidence = min(0.6 + score * 0.1, 0.95)

    if score >= 3:
        return "AI_GENERATED", confidence, "Synthetic voice characteristics detected"
    return "HUMAN", confidence, "Natural human speech patterns detected"

# ================= ROUTES =================
@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/api/voice-detection")
def detect_voice(
    payload: VoiceRequest,
    x_api_key: str = Header(..., alias="x-api-key")  # 🔥 FORCE HEADER
):
    # AUTH CHECK
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if payload.language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail="Unsupported language")

    if payload.audioFormat.lower() != "mp3":
        raise HTTPException(status_code=400, detail="Only mp3 supported")

    try:
        audio_bytes = base64.b64decode(payload.audioBase64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 audio")

    if not is_mp3(audio_bytes):
        raise HTTPException(status_code=400, detail="Invalid mp3 file")

    try:
        features = extract_features(audio_bytes)
        classification, confidence, explanation = classify(*features)
    except Exception:
        raise HTTPException(status_code=400, detail="Audio processing failed")

    return {
        "status": "success",
        "language": payload.language,
        "classification": classification,
        "confidenceScore": round(confidence, 2),
        "explanation": explanation,
    }

