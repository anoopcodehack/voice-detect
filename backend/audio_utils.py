import base64
import numpy as np

def decode_base64_audio(audio_base64: str):
    # Just a dummy waveform
    audio_bytes = base64.b64decode(audio_base64)
    waveform = np.zeros(16000)  # fake 1-second audio at 16kHz
    sr = 16000
    return waveform, sr

def extract_features(waveform, sr):
    # Return fake features
    mfcc = np.random.rand(13, 32)
    pitch = np.random.rand(32)
    return mfcc, pitch

