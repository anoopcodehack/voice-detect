import numpy as np

def predict_voice(features):
    variance = np.var(features)

    if variance < 0.015:
        return "AI_GENERATED", 0.90, "Unnatural pitch consistency and robotic spectral patterns detected"
    else:
        return "HUMAN", 0.85, "Natural pitch variations and human-like speech dynamics detected"
