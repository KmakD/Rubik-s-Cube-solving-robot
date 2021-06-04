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
int dirPin2;
int stepPin2;
int turn;
int turn2;
int tim;
int i;
String msg;
char par;
boolean para;

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

    for(i=0; i<msg.length(); i++){

    //wyznaczenie silnika którym należy poruszyć na podstawie algorytmu
    if(msg[i] == 'R'){
      stepPin = stepPin_R;
      dirPin = dirPin_R;
      tim = 500;
      par = 'L';
    }else if(msg[i] == 'L'){
      stepPin = stepPin_L;
      dirPin = dirPin_L;
      tim = 500;
      par = 'R';
    }else if(msg[i] == 'U'){
      stepPin = stepPin_U;
      dirPin = dirPin_U;
      tim = 700;
      par = 'D';
    }else if(msg[i] == 'D'){
      stepPin = stepPin_D;
      dirPin = dirPin_D;
      tim = 500;
      par = 'U';
    }else if(msg[i] == 'F'){
      stepPin = stepPin_F;
      dirPin = dirPin_F;
      tim = 500;
      par = 'B';
    }else if(msg[i] == 'B'){
      stepPin = stepPin_B;
      dirPin = dirPin_B;
      tim = 500;
      par = 'F';
    }else{
      par = 'X';
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

  for(int j=1; j<4; j++){
    if(msg[i+j] == par){
      para = true;
      //printf(par);
        
    if(msg[i+j] == 'R'){
      stepPin2 = stepPin_R;
      dirPin2 = dirPin_R;
      tim = 500;
    }else if(msg[i+j] == 'L'){
      stepPin2 = stepPin_L;
      dirPin2 = dirPin_L;
      tim = 500;
    }else if(msg[i+j] == 'U'){
      stepPin2 = stepPin_U;
      dirPin2 = dirPin_U;
      tim = 700;
    }else if(msg[i+j] == 'D'){
      stepPin2 = stepPin_D;
      dirPin2 = dirPin_D;
      tim = 700;
    }else if(msg[i+j] == 'F'){
      stepPin2 = stepPin_F;
      dirPin2 = dirPin_F;
      tim = 500;
    }else if(msg[i+j] == 'B'){
      stepPin2 = stepPin_B;
      dirPin2 = dirPin_B;
      tim = 500;
    }
    if(msg[i+j+1] == '\''){
      digitalWrite(dirPin2, LOW);
      turn2 = STEPS_PER_REV/4;
    }else if(msg[i+j+1] == '2'){
      digitalWrite(dirPin2, HIGH);
      turn2 = STEPS_PER_REV/2;
    }else{
      digitalWrite(dirPin2, HIGH);
      turn2 = STEPS_PER_REV/4;
    }
    i = i+j;
    break;
    }    
  }
    
    if(msg[i] == 'R' || msg[i] == 'L' || msg[i] == 'U'
    || msg[i] == 'D' || msg[i] == 'F' || msg[i] == 'B'){      
      
      //ruch silnika
      if(para == true && turn == turn2){
        for(int j = 0; j< turn; j++){
          digitalWrite(stepPin, HIGH);
          digitalWrite(stepPin2, HIGH);
          delayMicroseconds(tim+1000);
          digitalWrite(stepPin, LOW);
          digitalWrite(stepPin2, LOW);
          delayMicroseconds(tim+1000);
        } 
      }
      else if(para == true && turn > turn2){
        for(int j = 0; j< turn2; j++){
          digitalWrite(stepPin, HIGH);
          digitalWrite(stepPin2, HIGH);
          delayMicroseconds(tim+1000);
          digitalWrite(stepPin, LOW);
          digitalWrite(stepPin2, LOW);
          delayMicroseconds(tim+1000);
        } 
        for(int j = 0; j< turn2; j++){
          digitalWrite(stepPin, HIGH);
          delayMicroseconds(tim+1000);
          digitalWrite(stepPin, LOW);
          delayMicroseconds(tim+1000);
        }         
      }
      else if(para == true && turn < turn2){
        for(int j = 0; j< turn; j++){
          digitalWrite(stepPin, HIGH);
          digitalWrite(stepPin2, HIGH);
          delayMicroseconds(tim+1000);
          digitalWrite(stepPin, LOW);
          digitalWrite(stepPin2, LOW);
          delayMicroseconds(tim+1000);
        } 
        for(int j = 0; j< turn; j++){
          digitalWrite(stepPin, HIGH);
          delayMicroseconds(tim+1000);
          digitalWrite(stepPin, LOW);
          delayMicroseconds(tim+1000);
        }         
      }       
      else{
        for(int j = 0; j< turn; j++){
          digitalWrite(stepPin, HIGH);
          delayMicroseconds(tim+1000);
          digitalWrite(stepPin, LOW);
          delayMicroseconds(tim+1000);
        }
      }

    }
  }
  Serial.write("stop");
  }
}
