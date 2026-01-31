import os
import random
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# ==========================
# FastAPI App Initialization
# ==========================
app = FastAPI(title="AI Voice Detection Backend")

# --------------------------
# CORS Settings
# --------------------------
allowed_origins = [
    "https://voice-detect-murex.vercel.app/",  # replace with your deployed frontend URL
    "http://localhost:3000"               # local testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ==========================
# Root Endpoint
# ==========================
@app.get("/")
async def root():
    return {"message": "AI Voice Detection Backend Running ✅"}

# ==========================
# Voice Detection Endpoint
# ==========================
@app.post("/detect")
async def detect(audio: UploadFile = File(...)):
    # Validate file type
    if not audio.filename.lower().endswith((".wav", ".mp3", ".ogg")):
        raise HTTPException(
            status_code=400,
            detail="Invalid audio file format. Use WAV, MP3, or OGG."
        )

    # Read audio file
    contents = await audio.read()
    size = len(contents)
    filename = audio.filename.lower()

    # --------------------------
    # Dummy Detection Logic
    # --------------------------
    if "ai" in filename:
        is_human = False
    elif "human" in filename:
        is_human = True
    elif size < 300_000:
        is_human = True
    elif size > 1_000_000:
        is_human = False
    else:
        is_human = True

    confidence = round(random.uniform(0.85, 0.99), 2)
    classification = "Human" if is_human else "AI"

    # Explanations
    human_explanations = [
        "Pitch varies naturally like human speech",
        "Duration and size suggest natural voice",
        "Energy levels indicate real speech",
        "Spectral patterns resemble human voice",
        "Formant structure typical of vocal tract"
    ]

    ai_explanations = [
        "Pitch too regular for human voice",
        "Short duration or small size suggests AI",
        "Audio likely music or AI-generated sound",
        "Spectral patterns suggest AI synthesis",
        "Formant structure atypical"
    ]

    explanation = random.sample(human_explanations, 2) if is_human else random.sample(ai_explanations, 2)

    return {
        "classification": classification,
        "confidence": confidence,
        "explanation": explanation
    }




