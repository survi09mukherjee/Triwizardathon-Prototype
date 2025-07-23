import streamlit as st
import base64
from datetime import datetime
from streamlit.components.v1 import html
from db_utils import insert_data, fetch_logs
import ast
import json
import os

FALLBACK_LOG_FILE = "emotion_log_fallback.txt"

# -------------- Background Video Setup --------------
def get_base64_video(video_path):
    with open(video_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

video_base64 = get_base64_video("mentis video.mp4")

# -------------- Hogwarts Quote Mapping --------------
hogwarts_quotes = {
    "happy": ("Gryffindor", "Happiness can be found even in the darkest of times."),
    "sad": ("Ravenclaw", "Understanding is the first step to acceptance."),
    "angry": ("Slytherin", "Power resides where men believe it resides."),
    "neutral": ("Hufflepuff", "Loyalty and patience are a virtue."),
    "surprise": ("Gryffindor", "Every great wizard started as what you are now."),
    "fear": ("Ravenclaw", "Fear of a name increases fear of the thing itself.")
}

# -------------- Streamlit Config --------------
st.set_page_config(page_title="Mentis Mirror", layout="wide")

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Macondo&display=swap');
    .video-background {{
        position: fixed; right: 0; bottom: 0; min-width: 100%; min-height: 100%;
        z-index: -1; opacity: 0.6; object-fit: cover;
    }}
    .content {{
        position: relative; z-index: 1; font-family: 'Macondo', cursive;
        color: white; text-shadow: 1px 1px 3px black;
    }}
    .title-text {{
        font-size: 50px; text-align: center; color: #ffd700; padding-top: 30px;
        animation: glow 2s ease-in-out infinite alternate;
    }}
    .subtitle {{ text-align: center; font-size: 24px; margin-bottom: 20px; color: #f0e6d2; }}
    .house {{ font-size: 28px; color: #e0b0ff; text-align: center; }}
    .quote {{ font-style: italic; color: #fdd835; font-size: 20px; text-align: center; }}
    @keyframes glow {{
        from {{ text-shadow: 0 0 10px #ffd700; }} to {{ text-shadow: 0 0 20px #ffff00; }}
    }}
    </style>
    <video autoplay muted loop class="video-background">
        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
    </video>
""", unsafe_allow_html=True)

# -------------- Header --------------
st.markdown("<div class='content'>", unsafe_allow_html=True)
st.image("logo.png", width=100) 
st.markdown("<div class='title-text'> Welcome to Mentis Mirror</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>✨ A magical reflection of your mind ✨</div>", unsafe_allow_html=True)

# -------------- Emotion Selector --------------
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    detected_emotion = st.selectbox("🧠 How are you feeling today?", list(hogwarts_quotes.keys()))
    house, quote = hogwarts_quotes[detected_emotion]
    st.markdown(f"<div class='house'>🏰 House: {house}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='quote'>“{quote}”</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='quote'>📅 {datetime.now().strftime('%A, %d %B %Y | %I:%M %p')}</div>", unsafe_allow_html=True)

# -------------- Sensor Inputs --------------
with st.expander("🔮 Enchanted Sensor Scroll"):
    temp = st.number_input("🌡️ Temperature (°C)", min_value=-10.0, max_value=50.0, value=28.3, step=0.1)
    sound_level = st.number_input("🎧 Sound Level (dB)", min_value=0.0, max_value=150.0, value=52.1, step=0.1)
    tvoc = st.number_input("🧪 TVOC", min_value=0, max_value=1000, value=120)
    co2 = st.number_input("🧪 CO2", min_value=0, max_value=2000, value=450)

# -------------- Emotion Result Display --------------
confidence = 1.00
st.markdown(f"### 🧠 Detected Emotion: `{detected_emotion}` with {confidence * 100:.2f}% confidence")

# -------------- Log Button --------------
if st.button("📝 Log this emotion"):
    try:
        insert_data(detected_emotion, confidence, temp, sound_level, tvoc, co2,)
        st.success("✨ Emotion log saved to database!")
    except Exception as e:
        fallback_entry = {
            "emotion": detected_emotion,
            "confidence": confidence,
            "sensor_data": {
                "temperature": temp,
                "sound_level": sound_level,
                "tvoc": tvoc,
                "co2": co2
            },
            "timestamp": str(datetime.now())
        }
        with open(FALLBACK_LOG_FILE, "a") as f:
            f.write(json.dumps(fallback_entry) + "\n")
        st.warning("⚠️ DB failed, saved to local fallback log file.")

# -------------- Magical Creatures Modal --------------
creatures = {
    "🧙‍♂️ Dumbledore": "The wisest wizard who guides you through wisdom.",
    "🧹 Nimbus 2000": "A flying broomstick for those feeling adventurous.",
    "✉️ Hogwarts Letter": "A magical invitation awaits!",
    "🧢 Sorting Hat": "Reveals your house based on your emotion.",
    "🐍 Basilisk": "Fear unlocks the serpent’s gaze.",
    "🪤 Invisibility Cloak": "For those who feel unnoticed or want to disappear.",
    "⚡ Harry’s Scar": "Symbol of strength in pain."
}

modal_html = """
<style>
.creature-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; justify-items: center; margin-top: 20px;}
.creature {background-color: rgba(255,255,255,0.1); border-radius: 12px; padding: 10px; text-align: center; color: white; font-size: 20px; font-family: 'Macondo', cursive; cursor: pointer;}
.creature:hover {transform: scale(1.1); background-color: #ffd70099;}
.modal {position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(30,30,30,0.95); padding: 25px; border-radius: 15px; box-shadow: 0 0 20px black; z-index: 9999;}
.overlay {position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.5); z-index: 9998;}
</style>
<div class="creature-grid">
"""
for emoji, desc in creatures.items():
    modal_html += f"<div class='creature' onclick=\"showModal('{emoji}', '{desc}')\">{emoji}</div>"
modal_html += "</div><div id='modal' style='display:none;'><div class='overlay' onclick='hideModal()'></div><div class='modal' id='modalContent'></div></div>"
modal_html += """
<script>
function showModal(title, text) {
    document.getElementById("modal").style.display = "block";
    document.getElementById("modalContent").innerHTML = `<h2 style='color:#ffd700;'>${title}</h2><p>${text}</p>`;
}
function hideModal() {
    document.getElementById("modal").style.display = "none";
}
</script>
"""
html(modal_html, height=600)

# -------------- Log Viewer --------------
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("📖 Emotion Log Viewer")

with st.expander("📜 Logged Emotions"):
    all_logs = []

    # Try DB logs
    try:
        logs = fetch_logs()
        for log in logs:
            log_id, timestamp, emotion, confidence, temperature, sound_level, tvoc, co2 = log
            sensor_data = {
                "temperature": temperature,
                "sound_level": sound_level,
                "tvoc": tvoc,
                "co2": co2
            }
            all_logs.append((emotion, confidence, sensor_data, timestamp))
    except Exception as e:
        print("DB error:", e)

    # Try Fallback file logs
    if os.path.exists(FALLBACK_LOG_FILE):
        with open(FALLBACK_LOG_FILE, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    all_logs.append((
                        entry["emotion"],
                        entry["confidence"],
                        entry["sensor_data"],
                        entry["timestamp"]
                    ))
                except:
                    pass

    if not all_logs:
        st.info("No logs available.")
    else:
        # Emotion-based card colors
        emotion_colors = {
            "happy": "rgba(1, 52, 13, 0.85)",     # Dark green with opacity
            "sad": "rgba(59, 2, 6, 0.85)",        # Dark pinkish
            "angry": "rgba(143, 13, 2, 0.85)",    # Deep red
            "surprise": "rgba(80, 62, 3, 0.85)",  # Mustard yellow
            "fear": "rgba(2, 38, 65, 0.85)",      # Dark blue
            "neutral": "rgba(2, 18, 49, 0.85)",   # Grey-blue
            "disgust": "rgba(0, 0, 0, 0.85)",     # Black
        }

        # Inject global styles
        st.markdown("""
            <style>
                .emotion-card {
                    border: 1px solid #ccc;
                    padding: 15px;
                    margin-bottom: 12px;
                    border-radius: 12px;
                    color: white;
                    box-shadow: 0 0 12px rgba(255, 255, 255, 0.4);
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                }
                .emotion-card:hover {
                    transform: scale(1.02);
                    box-shadow: 0 0 24px rgba(255, 255, 255, 0.8);
                }
            </style>
        """, unsafe_allow_html=True)

        # Render each log as glowing semi-transparent card
        for emotion, confidence, sensor_data, timestamp in sorted(all_logs, key=lambda x: x[3], reverse=True):
            cleaned_emotion = emotion.strip().lower()
            bg_color = emotion_colors.get(cleaned_emotion, "rgba(255, 255, 255, 0.8)")  # Fallback

            st.markdown(f"""
                <div class="emotion-card" style="background-color:{bg_color};">
                    <h4 style="margin-top:0;">🧠 <b>Emotion:</b> {emotion.title()}</h4>
                    <b>✅ Confidence:</b> {confidence:.2f}<br>
                    <b>📟 Sensors:</b> Temp: {sensor_data.get("temperature")}°C |
                    Sound: {sensor_data.get("sound_level")} dB |
                    TVOC: {sensor_data.get("tvoc")} |
                    CO₂: {sensor_data.get("co2")}<br>
                    <b>🕒 Timestamp:</b> {timestamp}
                </div>
            """, unsafe_allow_html=True)

st.markdown("""
    <a href="http://localhost:8501/streamlog.py" target="_self">
        <button style='font-size:18px;padding:8px 16px;border-radius:10px;background:#6c63ff;color:white;border:none;cursor:pointer;'>📊 Open StreamLog Viewer</button>
    </a>
""", unsafe_allow_html=True)
