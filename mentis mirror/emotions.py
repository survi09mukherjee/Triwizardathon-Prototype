from deepface import DeepFace
import cv2
import time
import pandas as pd
from datetime import datetime
import os
from db import log_to_mysql
import numpy as np
import random

# === Paths ===
IMAGE_DIR = "emotion_snapshots"
CSV_PATH = "emotion_logs.csv"

os.makedirs(IMAGE_DIR, exist_ok=True)
emotion_log = []

def detect_emotion(image):
    try:
        result = DeepFace.analyze(
            image,
            actions=['emotion'],
            enforce_detection=False,
            detector_backend='opencv'
        )
        emotion_data = result[0]['emotion']
        dominant_emotion = result[0]['dominant_emotion']
        confidence = emotion_data[dominant_emotion]
        return dominant_emotion, confidence
    except Exception as e:
        print("❌ Detection failed:", e)
        return "Unknown", 0.0

def draw_gradient_box(img, x, y, w, h, text):
    # Gradient edges (rainbow)
    colors = [
        (255, 0, 0),     # Red
        (255, 127, 0),   # Orange
        (255, 255, 0),   # Yellow
        (0, 255, 0),     # Green
        (0, 255, 255),   # Cyan
        (0, 0, 255),     # Blue
        (139, 0, 255)    # Purple
    ]
    for i in range(len(colors)):
        col = colors[i]
        cv2.rectangle(img, (x + i, y + i), (x + w - i, y + h - i), col, 1)

    # Sparkles
    for _ in range(15):
        sx = random.randint(x, x + w)
        sy = random.randint(y, y + h)
        cv2.circle(img, (sx, sy), 1, (255, 255, 255), -1)

    # Emotion label (ASCII only)
    cv2.putText(img, f"Emotion: {text}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

def log_emotions():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Could not open webcam.")
        return

    print("🎥 Webcam is running. Press 'c' to capture, 'q' to quit.")

    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame.")
            break

        display_frame = frame.copy()

        try:
            result = DeepFace.analyze(
                display_frame,
                actions=['emotion'],
                enforce_detection=False,
                detector_backend='opencv'
            )
            faces = DeepFace.extract_faces(display_frame, enforce_detection=False, detector_backend='opencv')

            for i, face in enumerate(faces):
                region = face['facial_area']
                x, y, w, h = region['x'], region['y'], region['w'], region['h']
                emotion = result[i]['dominant_emotion']
                draw_gradient_box(display_frame, x, y, w, h, emotion)

        except Exception as e:
            print("⚠️ Real-time face detection failed:", e)

        # Show live feed
        cv2.imshow("Mentis Mirror - Press 'c' to Capture | 'q' to Quit", display_frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('c'):
            count += 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file_ts = timestamp.replace(":", "-").replace(" ", "_")
            filename = f"{IMAGE_DIR}/emotion_{file_ts}.jpg"

            print(f"\n📸 Capturing image {count}...")

            # Detect emotion for original (clean) frame
            emotion, confidence = detect_emotion(frame)
            print(f"✅ {emotion.upper()} ({confidence:.2f}%) at {timestamp}")

            # Save plain frame (no boxes)
            cv2.imwrite(filename, frame)

            # Log to memory and DB
            emotion_log.append({
                "timestamp": timestamp,
                "emotion": emotion,
                "confidence": confidence,
                "image_path": filename
            })

            log_to_mysql(emotion, confidence, filename, timestamp)

    cap.release()
    cv2.destroyAllWindows()

    # Save to CSV
    df = pd.DataFrame(emotion_log)
    df.to_csv(CSV_PATH, index=False)
    print(f"\n💾 Emotion logs saved to {CSV_PATH}")

if __name__ == "__main__":
    log_emotions()
