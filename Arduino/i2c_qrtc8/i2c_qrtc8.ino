/*
  06/06/2018 - IFSP EBOT Piracicaba

  Arduino em modo slave i2c - responsavel pela leitura dos sensores
  de infravermelho e envio para o bloco mestre (lego ev3) via i2c

  Mestre -> bloco ev3 com linux ev3dev (software de controle em python)
  Escravo -> Arduino executando este código
*/  


#include <Wire.h>
#include <QTRSensors.h>     // biblioteca para o sensor de linha pololu

#define SLAVE_ADDRESS 0x04  // endereço escolhido 0x04 - pode ser alterado (no ev3 tambem)
//  I2C Pinouts - Arduino Uno
//  SDA -> A4 - Fio Amarelo do Cabo LEGO
//  SCL -> A5 - Fio Azul do cabo LEGO

String data_send = "00000000";      // Var global que será enviada com os dados para o mestre
boolean leitura = false;

#define NUM_SENSORES   8      // numero de sensores usados
#define TIMEOUT        2500   // 2500 microseconds para saida ir para LOW
#define IF_EMISSOR     2      // Pino para controlar o emissor

QTRSensorsRC qtrrc((unsigned char[]) {5, 6, 7, 8, 9, 10, 11, 12},
                    NUM_SENSORES, TIMEOUT, IF_EMISSOR); 

unsigned int valorSensores[NUM_SENSORES];  // Vetor para guardar o resultado das leituras

void setup()
{
  Serial.begin(9600);  
  Wire.begin(SLAVE_ADDRESS);        // Endereço i2c
  Wire.onReceive(receiveData);      // Funcao executada quando chega dado do mestre
  Wire.onRequest(sendData);         // Funcao executada para responder ao mestre
  Serial.println("");
  pinMode(13, OUTPUT);              // Pino 13 (LED) para testes
  calibrar();
}

void calibrar()
{
  boolean estado = false;
  int contador = 0;
  Serial.println("Calibrando");
  for (int i = 0; i < 400; i++)  // make the calibration take about 10 seconds
  {
    qtrrc.calibrate();            // reads all sensors 10 times at 2500 us per read (i.e. ~25 ms per call)
    if (contador % 10 == 0 ) 
    {
      estado = !estado;
      digitalWrite(13, estado);
      Serial.println(estado);
    }
    contador++;
  }
  Serial.println("Calibrado");
}

void loop()
{
  qtrrc.readLine(valorSensores);
  delay(10);
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
    else if ( leitura == 4 )
    {
      calibrar();
    }
    else
    {
      digitalWrite(13, LOW);
    }  
  }
}

void sendData() 
{
  for (int i=0; i<NUM_SENSORES; i++)
  {
    Wire.write(valorSensores[i]);
  }
}

