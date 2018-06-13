/*
  06/06/2018 - IFSP EBOT Piracicaba

  Arduino em modo slave i2c - responsavel pela leitura dos sensores
  de infravermelho e envio para o bloco mestre (lego ev3) via i2c

  Mestre -> bloco ev3 com linux ev3dev (software de controle em python)
  Escravo -> Arduino executando este código

  I2C Pinouts - Arduino Uno
  SDA -> A4 - Fio Amarelo do Cabo LEGO
  SCL -> A5 - Fio Azul do cabo LEGO
*/


#include <Wire.h>
#include <QTRSensors.h>     // biblioteca para o sensor de linha pololu

#define SLAVE_ADDRESS 0x04  // endereço escolhido 0x04 - pode ser alterado (no ev3 tambem)

#define NUM_SENSORES   8      // numero de sensores usados
#define TIMEOUT        2500   // 2500 microseconds para saida ir para LOW
#define IF_EMISSOR     2      // Pino para controlar o emissor
#define led            4      // Pino do led na placa arduino para debug

QTRSensorsRC qtrrc((unsigned char[]) {
  6, 7, 8, 9, 10, 11, 12, 13
}, NUM_SENSORES, TIMEOUT, IF_EMISSOR);

unsigned int valorSensores[NUM_SENSORES];     // Vetor para guardar o resultado das leituras
unsigned int valorRawSensores[NUM_SENSORES];  // Vetor para guardar o resultado das leituras

#define DEBUG true
int debug_print = 0; 
                         

void setup()
{
  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);        // Endereço i2c
  Wire.onReceive(receiveData);      // Funcao executada quando chega dado do mestre
  Wire.onRequest(sendData);         // Funcao executada para responder ao mestre
  Serial.println("");
  pinMode(led, OUTPUT);              // Pino 13 (LED) para testes
  calibrar();
}

void loop()
{
  delay(10);
  qtrrc.readLine(valorSensores);

  if (DEBUG)
  {
    //qtrrc.read(valorRawSensores);
    if ( debug_print % 100 == 0 )
    {
      Serial.print(" 8bit: " );
      for (int i = 0; i < NUM_SENSORES; i++)
      {
        unsigned char retorno = (unsigned char) (valorSensores[i] / 4);
        Serial.print(retorno);
        Serial.print("\t" );
      }
      Serial.println();
      Serial.print(" full: " );
      for (int i = 0; i < NUM_SENSORES; i++)
      {
        Serial.print(valorSensores[i]);
        Serial.print("\t" );
      }
      Serial.println();
      Serial.println();
      //    Serial.print(" RAW: " );
      //    for (int i = 0; i < NUM_SENSORES; i++)
      //    {
      //      unsigned char retorno = (unsigned char) (valorRawSensores[i] / 4);
      //      Serial.print(retorno);
      //      Serial.print(" - " );
      //    }
      //    Serial.println();
      //    Serial.println();
    }
    debug_print++;
  }
}

void calibrar()
{
  boolean estado = false;
  int contador = 0;
  Serial.println("Calibrando");
  for (int i = 0; i < 100; i++)  // make the calibration take about 10 seconds
  {
    qtrrc.calibrate();            // reads all sensors 10 times at 2500 us per read (i.e. ~25 ms per call)
    if (contador % 10 == 0 )
    {
      estado = !estado;
      digitalWrite(led, estado);
      Serial.println(estado);
    }
    contador++;
  }
  Serial.println("Calibrado");
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
      digitalWrite(led, HIGH);
    }
    else if (leitura == 3 )
    {
      digitalWrite(led, LOW);
    }
    else if ( leitura == 4 )
    {
      calibrar();
    }
    else
    {
      digitalWrite(led, LOW);
    }
  }
}

void sendData()
{
  for (int i = 0; i < NUM_SENSORES; i++)
  {
    unsigned char retorno = (unsigned char) (valorSensores[i] / 4);
    Wire.write(retorno);
  }
}

