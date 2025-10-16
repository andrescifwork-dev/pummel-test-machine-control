#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

//Creamos el objeto lcd con la dirección 0x3F, 16 columnas y 2 filas
LiquidCrystal_I2C lcd(0x27,16,2);  

//NEMA
const byte DIR = 2;
const byte PUL = 3;

const int velocidad = 300;
const int PPR = 200; //pulsos por revolucion

void girar_derecha();
void girar_izquierda();
//NEMA

int Bot1 = 8;
int Bot2 = 9;
int Bot3 = 10;
int boton1 = 0;
int boton2 = 0;
int boton3 = 0;

int Cal = 0;
int Frz = 0;

int iBot1 = 0;
int iBot2 = 0;
int iBot3 = 0;

int ValCal = 0;
int ValFrz = 0;


void setup() {
Serial.begin(9600);
pinMode(DIR, OUTPUT);
pinMode(PUL, OUTPUT); 
    
pinMode(Bot1, INPUT);
pinMode(Bot2, INPUT);
pinMode(Bot3, INPUT);

Wire.begin();
lcd.begin(16,2);
lcd.setCursor(0, 0); // top left
lcd.backlight();

lcd.print("MAQUINA PUMMEL");
delay(800);
lcd.clear();
}


void loop() {
boton1 = digitalRead (Bot1);
boton2 = digitalRead (Bot2);
boton3 = digitalRead (Bot3);

if(boton1 == 1 && iBot3 == 0){
iBot1 += 1;
}
else if(boton1 == 1 && iBot3 == 1){
iBot1 += 50;
}
else if(boton2 == 1 && iBot3 == 0){
iBot1 -= 1;
}
else if(boton2 == 1 && iBot3 == 1){
iBot1 -= 50;
}

if(boton3 == 1){
delay(400);
iBot3 += 1;
iBot1 = 0;
lcd.clear();
}

//*****************MENU PRINCIPAL CONFIGURABLE*************************
if(iBot3 == 0){
conf1();
}
if(iBot3 == 1){
conf2();
}
if(iBot3 == 2){
conf3();
 }
if(iBot3 == 3){
secuenciaConf();
 } 
}

void conf1(){
lcd.setCursor(0,0);
lcd.print(" CONFIGURACION");

//(16,2)
lcd.setCursor(0,1);
lcd.print("CAL PROB(mm):");
lcd.setCursor(13,1);
lcd.print(iBot1);
ValCal = iBot1;
delay(90);  
}

void conf2(){
lcd.setCursor(0,0);
lcd.print(" CONFIGURACION");

//(16,2)
lcd.setCursor(0,1);
lcd.print("FUERZA(N):");
lcd.setCursor(11,1);
lcd.print(iBot1);
ValFrz = iBot1;
delay(90);
}

void conf3(){
if(ValFrz >= 100 && ValCal >= 20){
lcd.setCursor(1,0);
lcd.print("OPRIMA BOTON");
lcd.setCursor(6,1);
lcd.print("INICIAR");
//VALORES OBTENIDOS
Serial.print("CALIBRE:");
Serial.println(ValCal);
Serial.print("FUERZA:");
Serial.println(ValFrz);
}
else{
lcd.setCursor(0,0);
lcd.print("VALORES");
lcd.setCursor(0,1);
lcd.print("INVALIDOS RST");
 }
delay(90);
}

void secuenciaConf(){
for(int i=0;i<=100;i++){
lcd.setCursor(0,0);
lcd.print("PORCENTAJE: ");
lcd.setCursor(13,0);
lcd.print(i);
lcd.setCursor(0,1);
lcd.print("SECUENCIA STNDR.");

//NEMA23
girar_derecha(); 
delay(1000);
girar_izquierda();
delay(1000);
//NEMA23
 } 
}

//FUNCION NEMA
void girar_derecha(){
    digitalWrite(DIR, LOW);
    for (int i = 0; i < PPR; i++){
        digitalWrite(PUL, HIGH);
        delayMicroseconds(velocidad);
        digitalWrite(PUL, LOW);
        delayMicroseconds(velocidad);
    }
}
void girar_izquierda(){
    digitalWrite(DIR, HIGH);
    for (int i = 0; i < PPR; i++){
        digitalWrite(PUL, HIGH);
        delayMicroseconds(velocidad);
        digitalWrite(PUL, LOW);
        delayMicroseconds(velocidad);
   }
}
