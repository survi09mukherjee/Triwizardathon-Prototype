import streamlit as st
import librosa
import numpy as np
import soundfile as sf
import joblib
import os
from datetime import datetime
import mysql.connector
import os
os.system('pip install resampy')
from resampy import resample
# === Load model ===
model = joblib.load("voice_tone_model.pkl")  # Trained SVM or MLP model

# === Extract features from audio ===
def extract_features(audio_file):
    X, sample_rate = librosa.load(audio_file, res_type='kaiser_fast')
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(y=X, sr=sample_rate).T, axis=0)
    mel = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T, axis=0)
    return np.hstack([mfccs, chroma, mel])

# === Log to MySQL ===
def log_to_mysql(detected_emotion):
    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="survi09mukh", database="mentis_mirror"
        )
        cursor = conn.cursor()
        query = "INSERT INTO emotion_logs (timestamp, emotion) VALUES (%s, %s)"
        cursor.execute(query, (datetime.now(), detected_emotion))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Error logging to DB: {e}")

# === Streamlit UI ===
st.set_page_config(page_title="Voice Tone Mirror", layout="centered")

st.title("🔮 Mentis Mirror – Voice Tone Detection")
st.markdown("Speak your feelings... let the mirror reflect your voice.")

uploaded_audio = st.file_uploader("🎤 Upload a voice recording (.wav)", type=["wav"])

if uploaded_audio:
    st.audio(uploaded_audio, format="audio/wav")

    with open("temp_audio.wav", "wb") as f:
        f.write(uploaded_audio.read())

    features = extract_features("temp_audio.wav").reshape(1, -1)
    prediction = model.predict(features)[0]

    st.success(f"🗣️ Detected Tone: **{prediction}**")

    # Mirror magic effect
    if prediction.lower() in ["happy", "excited", "cheerful"]:
        st.image("images/glow_magic.gif", caption="The Mirror Glows Brightly!", use_column_width=True)
    elif prediction.lower() in ["sad", "fearful", "angry"]:
        st.image("images/dark_fog.gif", caption="A Dark Mist Surrounds the Mirror...", use_column_width=True)

    log_to_mysql(prediction)
