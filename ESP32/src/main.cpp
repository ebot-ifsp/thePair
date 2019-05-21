#include <Arduino.h>
#include <QTRSensors.h>
#include <ESP32Servo.h>

#define NUM_SENSORES   8        // numero de sensores usados
#define TIMEOUT        2500     // 2500 microseconds para saida ir para LOW
#define IF_EMISSOR     15       // Pino para controlar o emissor

#define PIN_SERVO_A    21       // Pino do servo A
#define PIN_SERVO_B    21       // Pino do servo B

// Definir os pinos do sonar (trigger e echo)

QTRSensorsRC qtrrc((unsigned char[]) {
                    13, 12, 14, 27, 26, 25, 33, 32}, 
                    NUM_SENSORES, TIMEOUT, IF_EMISSOR);

unsigned int valorSensores[NUM_SENSORES];     // Vetor para guardar o resultado das leituras
unsigned int valorRawSensores[NUM_SENSORES];  // Vetor para guardar o resultado das leituras
int posicao = 0;
bool envio_automatico = false;
String buff = "";

String QTR = "00110000-3.1345";

Servo servoA;
Servo servoB;

void calibrar()
{
  bool estado = false;
  int contador = 0;
  Serial.println("Calibrando");
  for (int i = 0; i < 40; i++)  // make the calibration take about 10 seconds
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
  5 - leitura sonar1
  6 - leitura sonar2
  s1-xyz - move posicao do servo1 para inteiro xyz
  s2-xyz - move posicao do servo2 para inteiro xyz
*/

void setup() 
{
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  servoA.setPeriodHertz(50);    // TODO - verificar frequencia do servo SG90
  servoB.setPeriodHertz(50);
  servoA.attach(PIN_SERVO_A, 500, 2400);
  servoB.attach(PIN_SERVO_B, 500, 2400);
  calibrar();
}

void loop() 
{
  if ( envio_automatico )
  {
    leitura_qtr(true);
    qtr_to_String(true);
    // ler os sonares
    // converter ambas para string
    Serial.println(QTR + "," + "Leirutra sonares");
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
      if (buff.charAt(buff.length()-1) == '\r')
      {
        Serial.println("aqui");
        buff.remove(buff.length()-1);
      }
      Serial.println("debug");
      Serial.println(buff);
      Serial.println(buff.length());
      Serial.println("fim debug");
      if ( buff.length() == 1)
      {
        int valor = buff.toInt();
        switch (valor)
        {
          case 0: // Desativa o envio automático
            envio_automatico = false;
            break;
          case 1: // Ativa o envio automático
            envio_automatico = true;
            break;
          case 2: // Pede leitura do Qrcode no modo raw
            leitura_qtr(true);
            qtr_to_String(true);
            Serial.println(QTR);
            break;
          case 3: // Pede leitura do Qrcode no modo calibrado
            leitura_qtr();
            qtr_to_String();
            Serial.println(QTR);
            break;
          case 4: // Realiza calibração do sensor de linha
            calibrar();
            break;
          case 5: // Leitura do sonar 1
            Serial.println("Sonar 1");
            break;
          case 6: // Leitura do sonar 2
            Serial.println("Sonar 1");
            break;
          default:
            break;
        }
      } else if ( buff.startsWith("SA") )
      { 
        buff.remove(0, 2);
        int posicao_servo = buff.toInt();
        Serial.print("movendo servo 1 para: ");
        Serial.println(posicao_servo);
        servoA.write(posicao_servo);
      } else if ( buff.startsWith("SB") >= 0 )
      {
        int posicao_servo = buff.toInt();
        Serial.print("movendo servo 2 para: ");
        Serial.println(posicao_servo);
        servoB.write(posicao_servo);
      }
      buff = "";
    }
  }
}

