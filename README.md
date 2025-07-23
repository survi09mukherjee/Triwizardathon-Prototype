
## 🧙‍♂️🔍 Mentis Mirror: The Mind Revealer 🧠💭
  <img width="1024" height="1024" alt="1" src="https://github.com/user-attachments/assets/37117f03-0998-497c-bc4f-cbfd8930be23" />
Mentis Mirror is an intelligent emotion-aware smart mirror, inspired by the wizarding world of Harry Potter. It detects the user's facial emotions in real-time, logs environmental sensor data (temperature, sound, TVOC, CO₂), and reflects back personalized magical feedback. The prototype combines Machine Learning, Streamlit UI, DeepFace emotion recognition, and MySQL database integration.
  <img width="1024" height="1536" alt="2" src="https://github.com/user-attachments/assets/72441660-9c13-4ebf-9e48-6777218d6605" />
  <img width="1024" height="1536" alt="3" src="https://github.com/user-attachments/assets/f148ced5-bbbd-411e-b816-f8e37cba5fa1" />

## ✨ Project Highlights

- 🧠 *Emotion Detection* using DeepFace and OpenCV.  
- 📊 *Sensor Data Logging* (temperature, sound, CO₂, TVOC).  
- 🪄 *Harry Potter-Themed UI* with magical creatures and animations.  
- 🗃 *MySQL Integration* for logging and reviewing emotion-sensor data.  
- 🧾 *Interactive Viewer Tab* to explore historical data entries.  

---

## 🧰 Tech Stack

- *Frontend*: Streamlit (Python), Custom CSS, Animated Effects  
- *Backend*: Python, DeepFace, OpenCV, MySQL  
- *Database*: MySQL (with fallback to local file logging)  
- *Sensors (Simulated)*: ESP32 via Wokwi (for future IoT integration)  

---

## ⚙ Setup Instructions

1. *Clone the repository*:
   ```bash
   git clone https://github.com/your-username/mentis-mirror.git
   cd mentis-mirror

2. **Create and activate virtual environment**:

    ```bash
    python -m venv deepface_env
    source deepface_env/bin/activate  # On Windows: deepface_env\Scripts\activate

3. *Install dependencies*:

    ```bash
    pip install streamlit
    pip install deepface
    pip install opencv-python
    pip install mysql-connector-python
    pip install pandas
    pip install pillow
    pip install matplotlib
    pip install numpy
    pip install plotly
    pip install streamlit-option-menu
    pip install datetime
    pip install pygame
    pip install -r requirements.txt

5. **Run the application:

    ```bash
    streamlit run app.py

##  Key Functionalities

- Real-time Emotion Recognition via webcam.

- Magical Mirror UI: Emotions trigger animations, quotes, and popups.

- Environmental Awareness: Sensor values are displayed and logged.

- Log Viewer: Explore historical logs with timestamped data.

- Fallback Logging: If MySQL is not available, data is stored locally.


## 🔮 Future Enhancements
1. 🌐 IoT Simulation + Physical Prototype 
- Integrate Wokwi-based ESP32 simulation into a physical prototype.

- Use real sensors (DHT11, MQ135, Mic Sensor) for environmental data collection.

- Connect ESP32 data to Streamlit UI via MQTT or RESTful API.

2. 🔊 Sound-Based Emotion Detection 
- Implement voice tone analysis using pyAudioAnalysis, librosa, or speechbrain.

- Fuse facial and audio cues for multi-modal emotion recognition.

- Improve accuracy and response sensitivity with audio-visual analysis.


## Screenshots of the Emotion Detection:
  <img width="804" height="572" alt="3 (2)" src="https://github.com/user-attachments/assets/01ee65e4-635c-42d3-b5b5-bfe5d401efbf" />
  <img width="695" height="550" alt="2 (2)" src="https://github.com/user-attachments/assets/b2b515f2-d376-48a5-871d-b041d19a4303" />
  <img width="417" height="473" alt="5" src="https://github.com/user-attachments/assets/b02f53fd-d666-4672-b021-e727ce678e29" />
  <img width="767" height="572" alt="1 (2)" src="https://github.com/user-attachments/assets/91c45d6a-b1ff-4fc0-a4e3-0a7581ef63d6" />
  <img width="488" height="463" alt="4" src="https://github.com/user-attachments/assets/53386660-52b7-444f-a04b-f8649d80840d" />

## Screenshots of the frontend UI:

- Home Page
  <img width="1887" height="866" alt="10" src="https://github.com/user-attachments/assets/503d234c-4efd-4ef2-af17-bd92683fb948" />
  <img width="929" height="907" alt="11" src="https://github.com/user-attachments/assets/e430d16c-5cd7-41e0-bf09-c29226eabba2" />
  <img width="1787" height="341" alt="12" src="https://github.com/user-attachments/assets/3169f67c-11cd-49fd-bd16-93aa1104647a" />
  <img width="1854" height="737" alt="13" src="https://github.com/user-attachments/assets/16372852-cc2c-413f-86cc-8cc03a6d7db9" />

- Emotion Logs
  <img width="1502" height="681" alt="database" src="https://github.com/user-attachments/assets/47f05b59-9a0e-4a9a-bdc7-5869c1f49173" />
  <img width="1899" height="813" alt="9" src="https://github.com/user-attachments/assets/5fa7b4ac-1760-40ef-b6e9-0217b10144e7" />

- SHAP Explainability
  <img width="1073" height="812" alt="6" src="https://github.com/user-attachments/assets/15dc3395-567b-4edd-a9d3-474a8ace1826" />
  <img width="1013" height="752" alt="7" src="https://github.com/user-attachments/assets/a9bfab13-2edf-4357-9130-6812bd1661d1" />

- Voice Input Emotion Detector
  <img width="1160" height="485" alt="8" src="https://github.com/user-attachments/assets/eefba051-2d3b-4c10-92f2-cb354a86bb03" />

## Screenshot of the IOT device setup in Wokwi Simulation:

- Setup
  <img width="1536" height="1024" alt="ESP32 Circuit with Sensors and Display" src="https://github.com/user-attachments/assets/5528a298-d86c-4a39-a835-c3907b64a810" />
- Output (Outcome)
  ![result](https://github.com/user-attachments/assets/11fb8ff3-80c2-4e06-9323-e4dceecd360f)

## You can enjoy the animation of the UI/UX of this project created
- Scan the QR Code given below.
  <img width="3000" height="3889" alt="frame" src="https://github.com/user-attachments/assets/c7fd46fc-041d-4620-850c-1d8ea369ee40" />

  
## 👩‍💻 Contributors

- *Survi Mukherjee* – Developer, UI Designer, Emotion Logic, Integration
- *Joy Mukherjee* – Developer, UI Designer, Emotion Logic, Integration


## "The Mentis Mirror reveals not the face you wear, but the emotions you dare not share — the truest reflection of your heart and soul, whispered through magic untold."
