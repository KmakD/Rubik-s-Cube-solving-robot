//zdefiniowanie wyjść sterujących
const int dirPin_R = 2;
const int stepPin_R = 3;

const int dirPin_L = 4;
const int stepPin_L = 5;

const int dirPin_U = 6;
const int stepPin_U = 7;

const int dirPin_D = 8;
const int stepPin_D = 9;

const int dirPin_F = 10;
const int stepPin_F = 11;

const int dirPin_B = 12;
const int stepPin_B = 13;

const int STEPS_PER_REV = 200;

int dirPin;
int stepPin;
int turn;
int tim;
String msg;

void setup() {

  //zainicjowanie komunikacji przez port USB
  Serial.begin(9600);
  //ustawienie rodzaju wyjść sterownika
  pinMode(stepPin_R, OUTPUT);
  pinMode(dirPin_R, OUTPUT);
  pinMode(stepPin_L, OUTPUT);
  pinMode(dirPin_L, OUTPUT);
  pinMode(stepPin_U, OUTPUT);
  pinMode(dirPin_U, OUTPUT);
  pinMode(stepPin_D, OUTPUT);
  pinMode(dirPin_D, OUTPUT);
  pinMode(stepPin_F, OUTPUT);
  pinMode(dirPin_F, OUTPUT);
  pinMode(stepPin_B, OUTPUT);
  pinMode(dirPin_B, OUTPUT);
}

void loop() {

  if(Serial.available() > 0){             
    msg = Serial.readStringUntil('\n'); //zapisanie przesłanego algorytmu

    for(int i=0; i<msg.length(); i++){

    //wyznaczenie silnika którym należy poruszyć na podstawie algorytmu
    if(msg[i] == 'R'){
      stepPin = stepPin_R;
      dirPin = dirPin_R;
      tim = 500;
    }else if(msg[i] == 'L'){
      stepPin = stepPin_L;
      dirPin = dirPin_L;
      tim = 500;
    }else if(msg[i] == 'U'){
      stepPin = stepPin_U;
      dirPin = dirPin_U;
      tim = 700;
    }else if(msg[i] == 'D'){
      stepPin = stepPin_D;
      dirPin = dirPin_D;
      tim = 500;
    }else if(msg[i] == 'F'){
      stepPin = stepPin_F;
      dirPin = dirPin_F;
      tim = 500;
    }else if(msg[i] == 'B'){
      stepPin = stepPin_B;
      dirPin = dirPin_B;
      tim = 500;
    }

    //ustalenie kierunku oraz zakresu ruchu silnika
    if(msg[i+1] == '\''){
      digitalWrite(dirPin, LOW);
      turn = STEPS_PER_REV/4;
    }else if(msg[i+1] == '2'){
      digitalWrite(dirPin, HIGH);
      turn = STEPS_PER_REV/2;
    }else{
      digitalWrite(dirPin, HIGH);
      turn = STEPS_PER_REV/4;
    }

    
    if(msg[i] == 'R' || msg[i] == 'L' || msg[i] == 'U'
    || msg[i] == 'D' || msg[i] == 'F' || msg[i] == 'B'){      

      //ruch silnika
      for(int i = 0; i< turn; i++){
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(tim);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(tim);
      }
    }
  }
  Serial.write("stop");
  }
}
