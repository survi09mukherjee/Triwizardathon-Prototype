#include <DHT.h>

#define DHTPIN 15         // DHT22 connected to GPIO 15
#define DHTTYPE DHT22

#define LDR_PIN 34        // LDR connected to GPIO 34
#define SOUND_PIN 36      // Sound potentiometer to GPIO 36
#define GAS_PIN 39        // Gas potentiometer to GPIO 39
#define CUSTOM1_PIN 32    // Potentiometer 1
#define CUSTOM2_PIN 35    // Potentiometer 2

#define LED_PIN 2         // LED connected to GPIO 2

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
}

void loop() {
  float temp = dht.readTemperature();
  float humidity = dht.readHumidity();

  int ldrVal = analogRead(LDR_PIN);
  int soundVal = analogRead(SOUND_PIN);
  int gasVal = analogRead(GAS_PIN);
  int custom1Val = analogRead(CUSTOM1_PIN);
  int custom2Val = analogRead(CUSTOM2_PIN);

  // Print sensor values
  Serial.println("----- Sensor Readings -----");
  Serial.print("Temperature (°C): "); Serial.println(temp);
  Serial.print("Humidity (%): "); Serial.println(humidity);
  Serial.print("Light Intensity (LDR): "); Serial.println(ldrVal);
  Serial.print("Sound Level: "); Serial.println(soundVal);
  Serial.print("Gas Level: "); Serial.println(gasVal);
  Serial.print("Custom Sensor 1 (POT1): "); Serial.println(custom1Val);
  Serial.print("Custom Sensor 2 (POT2): "); Serial.println(custom2Val);

  // Control LED if gas level is high (example threshold)
  if (gasVal > 2000) {
    digitalWrite(LED_PIN, HIGH);
    Serial.println("⚠️ Gas level HIGH! LED ON.");
  } else {
    digitalWrite(LED_PIN, LOW);
    Serial.println("✅ Gas level normal. LED OFF.");
  }

  Serial.println("-----------------------------\n");
  delay(2000);
}
