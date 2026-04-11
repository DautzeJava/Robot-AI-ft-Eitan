// 1. Définition des Pins (Hardware)
#include <Arduino.h>
#include <Wire.h>
#include <VL53L1X.h>

const int motorPin = 9; 
const int lidarPin = A0;
VL53L1X sensor;
int distance;

// 2. Variables de communication
String inputString = "";         
bool commandComplete = false;  
  int dataToSend = 0;  

void setup() {
  Serial.begin(9600); 
  Wire.begin();
  Wire.setClock(400000);
  sensor.setTimeout(500);
  pinMode(motorPin, OUTPUT);
  inputString.reserve(200); // Protection mémoire

  if (!sensor.init()) {
    Serial.println("Lidar initialization failed");
  }

  sensor.setDistanceMode(VL53L1X::Long);
  sensor.setMeasurementTimingBudget(50000);
  sensor.startContinuous(50);
  distance = sensor.read(distance);
}

int setData()
{
  dataToSend = distance;
}

void loop() {
  // On traite la commande dès qu'un '\n' est reçu
  distance = sensor.read();

  if (commandComplete) {
    executeAction(inputString); 
    inputString = "";           
    commandComplete = false;
  }
  dataToSend = setData();

}

// 3. La fonction qui décode les ordres
void executeAction(String command) {
  if (command.startsWith("GO")) {
    digitalWrite(motorPin, HIGH);
    Serial.println("ACK:Moteur_ON"); 
  } 
  else if (command.startsWith("STOP") || command.startsWith("QUIT")) {
    digitalWrite(motorPin, LOW);
    Serial.println("ACK:Moteur_OFF_System_Ready");
  }
  else if (command.startsWith("DATA"))
  {
    setData();
    Serial.println(dataToSend);
  }
}

// 4. L'interruption Série (Asynchrone)
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') { 
      commandComplete = true;
    } else {
      inputString += inChar;
    }
  }
}
