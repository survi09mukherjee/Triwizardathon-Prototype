import mysql.connector
from datetime import datetime
import json

# ✅ Connect to MySQL Database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",                  
        password="survi09mukh",      
        database="mentis_mirror"     
    )

# ✅ Create table with all required fields
def create_table_if_not_exists():
    try:
        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mirror_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME,
                emotion VARCHAR(255),
                confidence FLOAT,
                sensor_data TEXT,
                temperature FLOAT,
                sound_level FLOAT,
                tvoc FLOAT,
                co2 FLOAT
            )
        """)
        db.commit()
    except Exception as e:
        print("Error creating table:", e)
    finally:
        cursor.close()
        db.close()

# ✅ Insert emotion + sensor data (both JSON and separate columns)
def insert_data(emotion, confidence, temp, sound_level, tvoc, co2):
    try:
        db = connect_to_db()
        cursor = db.cursor()
        timestamp = datetime.now()

        cursor.execute("""
            INSERT INTO mirror_logs (emotion, confidence, temperature, sound_level, tvoc, co2, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (emotion, confidence, temp, sound_level, tvoc, co2, timestamp))

        db.commit()
        print("✅ Data inserted into database")
    except Exception as e:
        print("❌ Error inserting data:", e)
    finally:
        cursor.close()
        db.close()


# ✅ Fetch logs for viewer tab
def fetch_logs():
    try:
        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM mirror_logs ORDER BY timestamp DESC")
        result = cursor.fetchall()
        return result
    except Exception as e:
        print("❌ Error fetching logs:", e)
        return []
    finally:
        cursor.close()
        db.close()
