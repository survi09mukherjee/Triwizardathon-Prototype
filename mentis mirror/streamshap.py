import streamlit as st
import shap
import joblib
import pandas as pd
import matplotlib.pyplot as plt

# Load trained model
model = joblib.load("model.pkl")

# UI inputs
st.image("logo.png", width=200)
st.title(" Mentis Mirror: Magical Emotion Reflection")
temp = st.slider("🌡️ Temperature", 20, 40, 34)
co2 = st.slider("🌫️ CO₂", 300, 1000, 720)
tvoc = st.slider("🧪 TVOC", 50, 500, 250)
sound = st.slider("🔊 Sound Level", 20, 100, 85)

data = pd.DataFrame([{
    "temperature": temp,
    "co2": co2,
    "tvoc": tvoc,
    "sound_level": sound
}])

# Prediction
pred = model.predict(data)[0]
emotion = "😰 High Stress" if pred == 1 else "😌 Calm"
st.markdown(f"### 💫 Emotion Detected by Mirror: **{emotion}**")

# SHAP Explainability
explainer = shap.Explainer(model, data)
shap_values = explainer(data)

# Magic Mirror Reflection UI
with st.expander("🪞 Mirror Reflection (Click to Reveal Mystical Clues)"):
    for i, feature in enumerate(data.columns):
        shap_val = shap_values[0].values[i]
        mag_sentence = ""
        if shap_val > 0:
            mag_sentence = f"✨ The rising `{feature}` added to your tension... *(+{shap_val:.2f})*"
        else:
            mag_sentence = f"🍃 The calmness of `{feature}` helped ease your state. *({shap_val:.2f})*"
        st.markdown(f"**🔍 {feature.capitalize()}**: {mag_sentence}")

    # Optional: Show full SHAP waterfall plot
    st.markdown("#### 📊 Mystical Force Breakdown")
    shap.plots.waterfall(shap_values[0], max_display=4, show=False)
    st.pyplot(plt.gcf())

