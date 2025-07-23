from datetime import datetime
import json

def log_to_txt(emotion, confidence, temp, sound, tvoc, co2, filename="mirror_logs.txt"):
    try:
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "emotion": emotion,
            "confidence": round(confidence, 2),
            "temperature": temp,
            "sound_level": sound,
            "tvoc": tvoc,
            "co2": co2
        }

        with open(filename, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        print("[LOGGED TO FILE]", log_entry)

    except Exception as e:
        print("[ERROR LOGGING TO FILE]", e)
