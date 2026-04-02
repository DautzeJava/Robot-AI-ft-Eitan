// 1. Définition des Pins (Hardware)
#include <Arduino.h>

const int motorPin = 9; 

// 2. Variables de communication
String inputString = "";         
bool commandComplete = false;  
  int dataToSend = 0;  

void setup() {
  Serial.begin(9600); 
  pinMode(motorPin, OUTPUT);
  inputString.reserve(200); // Protection mémoire
}
int setData()
{
  dataToSend = analogRead(A0);
}

void loop() {
  // On traite la commande dès qu'un '\n' est reçu
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
