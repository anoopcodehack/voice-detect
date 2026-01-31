from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import random
import string

app = FastAPI(title="AI Voice Detection Backend")

# CORS middleware for Next.js frontend (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
        raise HTTPException(status_code=400, detail="Invalid audio file format. Use WAV, MP3, or OGG.")

    # Read audio content (we don't process it yet, just validate)
    contents = await audio.read()

    # 🎲 RANDOM AI DETECTION RESULTS (different every time!)
    is_human = random.choice([True, False])  # 50/50 Human vs AI
    classification = "Human" if is_human else "AI"
    
    # Random confidence between 65-99%
    confidence = round(random.uniform(0.65, 0.99), 2)
    
    # Random explanations (pick 2 different ones each time)
    explanations = [
        "MFCC spectral features match human patterns",
        "Pitch contour shows natural variation", 
        "Formant structure typical of vocal tract",
        "Mel spectrogram has organic artifacts",
        "Fundamental frequency natural jitter",
        "Spectral centroid within human range",
        "Zero crossing rate matches speech patterns"
    ]
    
    # Pick 2 random explanations
    explanation = random.sample(explanations, 2)

    result = {
        "classification": classification,
        "confidence": confidence,
        "explanation": explanation
    }

    return result








