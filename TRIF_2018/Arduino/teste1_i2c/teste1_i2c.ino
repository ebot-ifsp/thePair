/*
  06/06/2018 - IFSP EBOT Piracicaba

  Arduino em modo slave i2c - responsavel pela leitura dos sensores
  de infravermelho e envio para o bloco mestre (lego ev3) via i2c

  Mestre -> bloco ev3 com linux ev3dev (software de controle em python)
  Escravo -> Arduino executando este código
*/  


#include <Wire.h>

#define SLAVE_ADDRESS 0x04  // endereço escolhido 0x04 - pode ser alterado (no ev3 tambem)
//  I2C Pinouts - Arduino Uno
//  SDA -> A4 - Fio Amarelo do Cabo LEGO
//  SCL -> A5 - Fio Azul do cabo LEGO

#define DEBUG true

String data_send = "00000000";      // Var global que será enviada com os dados para o mestre
boolean leitura = false;

void setup()
{
  //if (DEBUG) Serial.begin(9600);  // Envio pela serial para debug no desenvolvimento  
  Serial.begin(9600);  
  Wire.begin(SLAVE_ADDRESS);        // Endereço i2c
  Wire.onReceive(receiveData);      // Funcao executada quando chega dado do mestre
  Wire.onRequest(sendData);         // Funcao executada para responder ao mestre
  for (int i = 2; i < 10; i++)
  {
    pinMode(i, INPUT);              // Declarando os pinos (2 a 10) como entrada- sensor IF
  }
  pinMode(13, OUTPUT);              // Pino 13 (LED) para testes
}

void loop()
{
  //delay(100);                       // TODO - Tirar ou reduzir o delay
  le_sensores();
  delay(10);
}

void le_sensores()
{
    for (int i=2; i<10; i++)        // Lê todos os sensores
    {
      int b = digitalRead(i);
      data_send[i-2] = b;
    }
    //Serial.println(data_send);
}

void receiveData(int byteCount)
{
  int i = 0;
  while (Wire.available()) 
  {
    char leitura = Wire.read();
    if ( leitura == '1' )
    {
      Serial.println("antes do le_sensores");
      
    }
    else if ( leitura == 2 )
    {
      digitalWrite(13, HIGH);
    }
    else if (leitura == 3 )
    {
      digitalWrite(13, LOW);
    }
    else
    {
      digitalWrite(13, LOW);
    }
  }
}

void sendData() 
{
  for (int i=0; i<8; i++)
  {
    Wire.write(data_send[i]);
  }
}

