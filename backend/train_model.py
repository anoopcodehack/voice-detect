import os
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from feature_extractor import extract_features_from_file

X, y = [], []

for label, folder in [(1, "human"), (0, "ai")]:
    for root, _, files in os.walk(f"dataset/{folder}"):
        for f in files:
            if f.endswith((".mp3", ".wav")):
                X.append(extract_features_from_file(os.path.join(root, f)))
                y.append(label)

X = np.array(X)
y = np.array(y)

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier(n_estimators=300)
model.fit(Xtr, ytr)

joblib.dump(model, "voice_detector.pkl")
print("✅ Model trained & saved")
