#include <Arduino.h>
#include <Wifi.h>
#include <FirebaseESP32.h>
#include <string.h>
#include <HardwareSerial.h>

//Provide the token generation process info.
#include "addons/TokenHelper.h"
//Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

#define WIFI_SSID ""
#define WIFI_PASSWORD ""

#define FIREBASE_HOST ""
#define FIREBASE_AUTH ""

FirebaseData fbdo;
String path = "/arduino_command";
String pathID = "command";
int command;

const int MA1 = 12;
const int MA2 = 14;
const int MB1 = 26;
const int MB2 = 17;

void Wifi_Init() {
 WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
 Serial.print("Connecting to Wi-Fi");
 while (WiFi.status() != WL_CONNECTED)
 {
  Serial.print(".");
  delay(300);
  }
 Serial.println();
 Serial.print("Connected with IP: ");
 Serial.println(WiFi.localIP());
 Serial.println();
}

void setup() {
  pinMode(MA1,OUTPUT);
  pinMode(MA2,OUTPUT);
  pinMode(MB1,OUTPUT);
  pinMode(MB2,OUTPUT);

  Serial.begin(115200);
  Wifi_Init();
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
}

void loop() {
  if(Firebase.getInt(fbdo, path + "/" + pathID))
  {
   command =  fbdo.payload().toInt();
   delay(2000);

   if(command == 0)
  {
    Serial.println(command);
    digitalWrite(MA1, HIGH);
    digitalWrite(MA2, LOW);
    digitalWrite(MB1, HIGH);
    digitalWrite(MB2, LOW);
  }
  if(command == 1)
  {
    Serial.println(command);
    digitalWrite(MA1, LOW);
    digitalWrite(MA2, HIGH);
    digitalWrite(MB1, LOW);
    digitalWrite(MB2, HIGH);
  }
  if(command == 2)
  {
    Serial.println(command);
    digitalWrite(MA1, LOW);
    digitalWrite(MA2, HIGH);
    digitalWrite(MB1, HIGH);
    digitalWrite(MB2, LOW);
  }
  if(command == 3)
  {
    Serial.println(command);
    digitalWrite(MA1, HIGH);
    digitalWrite(MA2, LOW);
    digitalWrite(MB1, HIGH);
    digitalWrite(MB2, LOW);
  }
  if(command == 4)
  {
    Serial.println(command);
    digitalWrite(MA1, HIGH);
    digitalWrite(MA2, LOW);
    digitalWrite(MB1, HIGH);
    digitalWrite(MB2, LOW);
  }
  }
}
