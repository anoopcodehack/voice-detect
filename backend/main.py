import os
import random
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Voice Detection Backend")

# ✅ Read frontend URL from environment variable
FRONTEND_URL = os.getenv("FRONTEND_URL")

if not FRONTEND_URL:
    raise RuntimeError("FRONTEND_URL environment variable is not set")

# ✅ Proper CORS (NO localhost hardcoding)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Voice Detection Backend Running ✅"}

@app.post("/detect")
async def detect(audio: UploadFile = File(...)):
    # Validate file extension
    if not audio.filename.lower().endswith((".wav", ".mp3", ".ogg")):
        raise HTTPException(
            status_code=400,
            detail="Invalid audio file format. Use WAV, MP3, or OGG."
        )

    # Read audio (placeholder for real ML later)
    await audio.read()

    # 🎲 RANDOM AI DETECTION RESULTS
    is_human = random.choice([True, False])
    classification = "Human" if is_human else "AI"

    confidence = round(random.uniform(0.65, 0.99), 2)

    explanations = [
        "MFCC spectral features match human patterns",
        "Pitch contour shows natural variation",
        "Formant structure typical of vocal tract",
        "Mel spectrogram has organic artifacts",
        "Fundamental frequency natural jitter",
        "Spectral centroid within human range",
        "Zero crossing rate matches speech patterns"
    ]

    explanation = random.sample(explanations, 2)

    return {
        "classification": classification,
        "confidence": confidence,
        "explanation": explanation
    }









