#include <Arduino.h>
#include <QTRSensors.h>
#include <ESP32Servo.h>
//#include <sensorlinha.h>

#define NUM_SENSORES   8      // numero de sensores usados
#define TIMEOUT        2500   // 2500 microseconds para saida ir para LOW
#define IF_EMISSOR     15      // Pino para controlar o emissor

#define PIN_SERVO_1    18
#define PIN_SERVO_2    19

QTRSensorsRC qtrrc((unsigned char[]) {
                    12, 13, 14, 25, 26, 27, 16, 17}, 
                    NUM_SENSORES, TIMEOUT, IF_EMISSOR);

unsigned int valorSensores[NUM_SENSORES];     // Vetor para guardar o resultado das leituras
unsigned int valorRawSensores[NUM_SENSORES];  // Vetor para guardar o resultado das leituras
int posicao = 0;
bool envio_automatico = false;
String buff = "";

String QTR = "00110000-3.1345";
String cor1 = "2,255,120"; 
String cor2 = "255,255,0"; 

Servo servo1;
Servo servo2;

void calibrar()
{
  bool estado = false;
  int contador = 0;
  Serial.println("Calibrando");
  for (int i = 0; i < 400; i++)  // make the calibration take about 10 seconds
  {
    qtrrc.calibrate();            // reads all sensors 10 times at 2500 us per read (i.e. ~25 ms per call)
    if (contador % 10 == 0 )
    {
      estado = !estado;
      digitalWrite(LED_BUILTIN, estado);
    }
    contador++;
  }
  Serial.println("Calibrado");
}

void leitura_qtr(bool raw = false)
{
  if ( !raw )
  {
    posicao = qtrrc.readLine(valorSensores);
  }
  else
  {
    qtrrc.read(valorSensores);
  } 
}

void qtr_to_String(bool raw = false)
{
  QTR = "";
  if ( raw )
  {
    for (int i=0; i<NUM_SENSORES; i++)
    {
      QTR += String(valorRawSensores[i]);
    }
  }
  else
  {
    for (int i=0; i<NUM_SENSORES; i++)
    {
      QTR += String(valorSensores[i]);
    }
    QTR += "-";
    QTR += String(posicao);
  }
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
  servo1.setPeriodHertz(50);    // TODO - verificar frequencia do servo SG90
  servo2.setPeriodHertz(50);
  servo1.attach(PIN_SERVO_1, 500, 2400);
  servo2.attach(PIN_SERVO_2, 500, 2400);
  calibrar();
}

void loop() 
{
  if ( envio_automatico )
  {
    leitura_qtr(true);
    qtr_to_String(true);
    // ler cor1
    // ler cor2
    // converter ambas para string
    Serial.println(QTR + "," + cor1 + "," + cor2);
    delay(50);
  }
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
            envio_automatico = false;
            break;
          case 1:
            envio_automatico = true;
            break;
          case 2: // 2 - Qrcode-raw
            leitura_qtr(true);
            qtr_to_String(true);
            Serial.println(QTR);
            break;
          case 3: // 3 - Qrcode-calibrado
            leitura_qtr();
            qtr_to_String();
            Serial.println(QTR);
            break;
          case 4: // 4 - Calibrar
            calibrar();
            break;
          case 5: // 5 - leitura cor1
            cor1 = "2,255,120";
            Serial.println(cor1);
            break;
          case 6: // 6 - leitura cor1
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
        servo1.write(posicao_servo);
      }
      else if ( buff.startsWith("S2") >= 0 )
      {
        int posicao_servo = buff.toInt();
        Serial.print("movendo servo 2 para: ");
        Serial.println(posicao_servo);
        servo2.write(posicao_servo);
      }
      buff = "";
    }
  }
}

