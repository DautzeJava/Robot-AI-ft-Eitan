#include <Arduino.h>
#include <Wire.h>
#include <VL53L1X.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

const int motorPin = 9;
VL53L1X lidar;
Adafruit_MPU6050 mpu;
String inputString = "";

void setup() {
  Serial.begin(115200);
  pinMode(motorPin, OUTPUT);
  
  Wire.begin();
  Wire.setClock(100000); 

  // Initialisation silencieuse
  lidar.init();
  lidar.setDistanceMode(VL53L1X::Long);
  lidar.startContinuous(50);
  
  mpu.begin();
  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);

  // Le signal que Python attend pour savoir que tout est OK
  Serial.println("SYSTEM_READY");
}

void loop() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n' || inChar == '\r') {
      inputString.trim();
      
      if (inputString == "GO") {
        digitalWrite(motorPin, HIGH);
        Serial.println("ACK:MOTEUR_ON");
      } 
      else if (inputString == "STOP" || inputString == "QUIT") {
        digitalWrite(motorPin, LOW);
        Serial.println("ACK:MOTEUR_OFF");
      }
      else if (inputString == "DATA") {
        // --- On génère la ligne CSV ---
        int d = lidar.read();
        sensors_event_t a, g, t;
        mpu.getEvent(&a, &g, &t);

        // Format : Temps, Distance, AccX, AccY, AccZ
        Serial.print(millis()); Serial.print(",");
        Serial.print(d);        Serial.print(",");
        Serial.print(a.acceleration.x, 2); Serial.print(",");
        Serial.print(a.acceleration.y, 2); Serial.print(",");
        Serial.println(a.acceleration.z, 2);
      }
      inputString = ""; 
    } else {
      inputString += inChar;
    }
  }
}