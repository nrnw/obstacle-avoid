#include "ESP_MICRO.h"

const int LED = 2;
const int pD5 = 14;
const int pD6 = 12;
const int pD7 = 13;
const int pD8 = 15;

void setup(){
  Serial.begin(9600);
  pinMode(LED,OUTPUT);
 
 
start("SSID","PWD"); // Wifi details
 


  pinMode(pD5,OUTPUT);
  pinMode(pD6,OUTPUT);
  pinMode(pD7,OUTPUT);
  pinMode(pD8,OUTPUT);

  digitalWrite(pD5,LOW);
  digitalWrite(pD6,LOW);
  digitalWrite(pD7,LOW);
  digitalWrite(pD8,LOW);
}

void loop(){
  waitUntilNewReq();  //Waits until a new request from python come

  if (getPath()=="/OPEN_LED"){
    digitalWrite(LED,HIGH);
    returnThisInt(1); //Returns the data to python
  }
  if (getPath()=="/CLOSE_LED"){
    digitalWrite(LED,LOW);
    returnThisInt(1); //Returns the data to python
  }

  
  if (getPath()=="/FWD"){
    digitalWrite(pD5,HIGH);
    digitalWrite(pD6,LOW);
    digitalWrite(pD7,LOW);
    digitalWrite(pD8,HIGH);
    returnThisInt(1); //Returns the data to python
  }
  if (getPath()=="/BKW"){
    digitalWrite(pD5,LOW);
    digitalWrite(pD6,HIGH);
    digitalWrite(pD7,HIGH);
    digitalWrite(pD8,LOW);
    returnThisInt(1); //Returns the data to python
  }
  if (getPath()=="/LEFT"){
    digitalWrite(pD5,LOW);
    digitalWrite(pD6,HIGH);
    digitalWrite(pD7,LOW);
    digitalWrite(pD8,HIGH);
    returnThisInt(1); //Returns the data to python
  }
  if (getPath()=="/RIGHT"){
    digitalWrite(pD5,HIGH);
    digitalWrite(pD6,LOW);
    digitalWrite(pD7,HIGH);
    digitalWrite(pD8,LOW);
    returnThisInt(1); //Returns the data to python
  }

if (getPath()=="/STOP"){
    digitalWrite(pD5,LOW);
    digitalWrite(pD6,LOW);
    digitalWrite(pD7,LOW);
    digitalWrite(pD8,LOW);
    returnThisInt(1); //Returns the data to python
  }




  
}
