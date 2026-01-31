import librosa
import numpy as np

def extract_features(audio_path):
    y, sr = librosa.load(audio_path, sr=None)

    mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13), axis=1)
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    zero_crossing = np.mean(librosa.feature.zero_crossing_rate(y))
    chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr), axis=1)
    rms = np.mean(librosa.feature.rms(y=y))

    features = np.concatenate([
        mfcc,
        chroma,
        [spectral_centroid, zero_crossing, rms]
    ])

    return features
