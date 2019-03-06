#include <Arduino.h>
#include <QTRSensors.h>

#define NUM_SENSORES   8      // numero de sensores usados
#define TIMEOUT        2500   // 2500 microseconds para saida ir para LOW
#define IF_EMISSOR     2      // Pino para controlar o emissor
#define led            4      // Pino do led na placa arduino para debug

QTRSensorsRC qtrrc((unsigned char[]) {
                    6, 7, 8, 9, 10, 11, 12, 13}, 
                    NUM_SENSORES, TIMEOUT, IF_EMISSOR);

unsigned int valorSensores[NUM_SENSORES];     // Vetor para guardar o resultado das leituras
unsigned int valorRawSensores[NUM_SENSORES];  // Vetor para guardar o resultado das leituras
int posicao = 0;
bool automatico = false;
String buff = "";

String QTR = "00110000-3.1345";
String cor1 = "2,255,120"; 
String cor2 = "255,255,0"; 

void calibrar()
{
  // calibrar sensores

}

void envia_todos()
{

}

/*
modos:
  0 - Aguardar
  1 - Envio automatico
  2 - Qrcode-raw
  3 - Qrcode-calibrado
  4 - calibar
  5 - leitura senror cor1
  6 - leitura sensor cor2
  s1-xyz - move posicao do servo1 para inteiro xyz
  s2-xyz - move posicao do servo2 para inteiro xyz
*/

void setup() 
{
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  
  // pisca o led para indicar que o setup acabou
  for (int i=0; i<6; i++)
  {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(200);
    digitalWrite(LED_BUILTIN, LOW);
    delay(200);
  }
}

void loop() 
{
  if ( Serial.available() > 0)
  {
    char c = Serial.read();
    if ( c != '\n' )
    {
      buff += c;
    }
    else
    {
      if ( buff.length() == 1)
      {
        int valor = buff.toInt();
        switch (valor)
        {
          case 0:
            automatico = false;
            break;
          case 1:
            automatico = true;
            // ler QTR
            QTR = "00110000-3.1345"; // fake
            // ler cor1
            cor1 = "2,255,120"; // fake
            // ler cor2
            cor2 = "255,255,0"; // fake
            Serial.println(QTR + cor1 + cor2);
            break;
          case 2:
            QTR = "00010000-4.1345";
            Serial.println(QTR);
            break;
          case 3:
            QTR = "00000100-5.1345";
            Serial.println(QTR);
            break;
          case 4:
            calibrar();
            break;
          case 5:
            cor1 = "2,255,120";
            Serial.println(cor1);
            break;
          case 6:
            cor2 = "255,255,0";
            Serial.println(cor2);
            break;
          default:
            break;
        }
      }
      else if ( buff.startsWith("S1") >= 0 )
      { 
        buff.remove(0, 2);
        int posicao_servo = buff.toInt();
        Serial.print("movendo servo 1 para: ");
        Serial.println(posicao_servo);
      }
      else if ( buff.startsWith("S2") >= 0 )
      {
        int posicao_servo = buff.toInt();
        Serial.print("movendo servo 2 para: ");
        Serial.println(posicao_servo);
      }
      buff = "";
    }
  }
}

