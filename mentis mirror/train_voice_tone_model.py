import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline

# === Simulated Data (You can replace this later with actual extracted MFCCs) ===
# Format: [mfcc1, mfcc2, ..., mfcc13]
X = np.array([
    [0.6, 0.8, 0.4, 0.5, 0.7, 0.6, 0.9, 0.6, 0.8, 0.7, 0.5, 0.4, 0.3],  # happy
    [0.2, 0.1, 0.3, 0.4, 0.2, 0.1, 0.3, 0.3, 0.2, 0.4, 0.1, 0.2, 0.2],  # sad
    [0.9, 0.8, 0.7, 0.6, 0.8, 0.7, 0.9, 0.8, 0.9, 0.7, 0.6, 0.7, 0.8],  # angry
    [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]   # neutral
])
y = ['happy', 'sad', 'angry', 'neutral']

# === Label Encoding ===
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)  # converts to 0,1,2,3

# === Model Pipeline: StandardScaler + MLPClassifier ===
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('mlp', MLPClassifier(hidden_layer_sizes=(32,), max_iter=1000, random_state=42))
])

# === Train Model ===
pipeline.fit(X, y_encoded)

# === Predict on training data (since dataset is small) ===
y_pred = pipeline.predict(X)
print("Classification Report:\n", classification_report(
    y_encoded, y_pred, target_names=label_encoder.classes_, zero_division=0
))

# === Save Model and LabelEncoder ===
with open("voice_tone_model.pkl", "wb") as f:
    pickle.dump({
        'model': pipeline,
        'label_encoder': label_encoder
    }, f)

print("✅ voice_tone_model.pkl saved successfully.")
