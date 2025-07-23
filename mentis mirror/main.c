#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "driver/adc.h"
#include "esp_adc_cal.h"

// Pin definitions
#define DHT_PIN        15  // Simulated, value will be mocked
#define MQ_PIN         ADC1_CHANNEL_6 // GPIO34
#define MIC_PIN        ADC1_CHANNEL_7 // GPIO35
#define LED_RED        14
#define LED_GREEN      26
#define LED_BLUE       27
#define BUZZER_PIN     13

// Fake DHT22 temperature and humidity values (for simulation)
float read_temperature() {
  return 28.5 + (esp_random() % 50) / 10.0; // 28.5 - 33.5°C
}

float read_humidity() {
  return 60 + (esp_random() % 20); // 60% - 80%
}

// Read analog value from ADC channel
int read_adc(adc1_channel_t channel) {
  return adc1_get_raw(channel);
}

// Control LED state
void set_leds(bool red, bool green, bool blue) {
  gpio_set_level(LED_RED, red);
  gpio_set_level(LED_GREEN, green);
  gpio_set_level(LED_BLUE, blue);
}

// Control buzzer
void buzz_once() {
  gpio_set_level(BUZZER_PIN, 1);
  vTaskDelay(200 / portTICK_PERIOD_MS);
  gpio_set_level(BUZZER_PIN, 0);
}

void app_main() {
  // Configure GPIOs
  gpio_set_direction(LED_RED, GPIO_MODE_OUTPUT);
  gpio_set_direction(LED_GREEN, GPIO_MODE_OUTPUT);
  gpio_set_direction(LED_BLUE, GPIO_MODE_OUTPUT);
  gpio_set_direction(BUZZER_PIN, GPIO_MODE_OUTPUT);

  // ADC setup
  adc1_config_width(ADC_WIDTH_BIT_12);
  adc1_config_channel_atten(MQ_PIN, ADC_ATTEN_DB_11);
  adc1_config_channel_atten(MIC_PIN, ADC_ATTEN_DB_11);

  while (1) {
    float temp = read_temperature();
    float hum = read_humidity();
    int gas = read_adc(MQ_PIN);
    int sound = read_adc(MIC_PIN);

    printf("📊 Temperature: %.2f°C | Humidity: %.2f%% | Gas: %d | Sound: %d\n", temp, hum, gas, sound);

    // Emotion logic
    if (temp > 32 || gas > 2000 || sound > 3000) {
      printf("😠 Emotion: ANGRY detected! (🔥)\n");
      set_leds(1, 0, 0);
      buzz_once();
    } else if (hum > 70 && temp < 30) {
      printf("😊 Emotion: HAPPY detected! (🟢)\n");
      set_leds(0, 1, 0);
    } else {
      printf("😢 Emotion: SAD or NEUTRAL detected. (🔵)\n");
      set_leds(0, 0, 1);
    }

    vTaskDelay(3000 / portTICK_PERIOD_MS);
  }
}
