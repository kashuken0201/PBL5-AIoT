#include <SoftwareSerial.h>

#include "Arduino.h"  
#include "DFRobotDFPlayerMini.h"

#define SOUND_PIN 8

SoftwareSerial mySoftwareSerial(10, 11);
DFRobotDFPlayerMini myDFPlayer;

bool isPaused = false;

void setup()
{
    pinMode(SOUND_PIN, INPUT);

    mySoftwareSerial.begin(9600);
    Serial.begin(115200);
    Serial.println();
    Serial.println(F("DFRobot DFPlayer Mini Demo"));
    Serial.println(F("Initializing DFPlayer ... (May take 3~5 seconds)"));
    
    //Use softwareSerial to communicate with mp3
    while (!myDFPlayer.begin(mySoftwareSerial)) {  
      Serial.println(F("Unable to begin:"));
      Serial.println(F("1.Please recheck the connection!"));
      Serial.println(F("2.Please insert the SD card!"));
      delay(1000);
    }
    Serial.println(F("DFPlayer Mini online."));
    
    myDFPlayer.volume(15);        // Set volume value. From 0 to 30
    myDFPlayer.enableLoopAll();   // Enable Loop all songs mode
}

void loop()
{
    if (digitalRead(SOUND_PIN) == LOW)
    {
        if(!isPaused){
            myDFPlayer.stop();
            isPaused = true;
        }
    }
    else
    {
        if(isPaused){
            myDFPlayer.play(1);
            isPaused = false;
        }
    }
}