from rotary import Rotary
import time
from machine import Pin
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd


#PIN SALIDA CONTROL
MotControlPin = Pin(28, Pin.OUT)
MotControlPin.value(0)

#FIN CARRERA
#AMARILLO: DERECHA
#NEGRO: IZQUIERDA
ELizqDer = Pin(16, Pin.IN, Pin.PULL_UP) #IZQ
ELizqDer2 = Pin(17, Pin.IN, Pin.PULL_UP)  #DER
DirID = 'I'
#END LINE UP-DOWN D-19//UP-20
ELUDpwn = Pin(18, Pin.IN, Pin.PULL_UP)
ELUDpwn2 = Pin(19, Pin.IN, Pin.PULL_UP)
DirUDwn = 'U'
AutoHome = 'F'

#I2C SCREEN
I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

#VARIABLES
iMode = 0
ValCal = 0
ValFrz = 0
StrBtn = 'a'

#ENCODER 14,13,15
rotary = Rotary(3,4,2)
val = 0

#STEP MOT 1
pinEnabled = Pin(8, Pin.OUT,value=0)
pinStep = Pin(7, Pin.OUT)
pinDirection = Pin(6, Pin.OUT)
Vel = 950
#TEST MOT2
pinEnabled2 = Pin(12, Pin.OUT,value=0)
pinStep2 = Pin(11, Pin.OUT)
pinDirection2 = Pin(10, Pin.OUT)
Vel2 = 1100

stepsPerRevolution = 1000
#STEP MOT

#FIN CARRERA
NegOutIDer = Pin(26, Pin.OUT)
NegOutUD = Pin(27, Pin.OUT)
#boton = Pin(16, Pin.IN, Pin.PULL_UP)
#ArduMotor = Pin(28, Pin.OUT)



def Stop():
    global pinDirection
    global Vel
    global stepsPerRevolution
    global pinStep
    
    pinStep.off()
    time.sleep_us(Vel)
    pinStep.off()
    time.sleep_us(Vel)
    
def StopUD():
    global pinDirection2
    global Vel2
    global stepsPerRevolution
    global pinStep2
    
    pinStep2.off()
    time.sleep_us(Vel2)
    pinStep2.off()
    time.sleep_us(Vel2)    

def MovDer():
    global pinDirection
    global Vel
    global stepsPerRevolution
    global pinStep
    
    pinDirection.on()
    for i in range(0,stepsPerRevolution):
        pinStep.on()
        time.sleep_us(Vel)
        pinStep.off()
        time.sleep_us(Vel)
    
def MovIzq():
    global pinDirection
    global Vel
    global stepsPerRevolution
    global pinStep
    
    pinDirection.off()
    for i in range(0,stepsPerRevolution):
        pinStep.on()
        time.sleep_us(Vel)
        pinStep.off()
        time.sleep_us(Vel)
         
         
def MovUp():
    global pinDirection2
    global Vel2
    global stepsPerRevolution
    global pinStep2
    
    pinDirection2.off()
    for i in range(0,stepsPerRevolution):
        pinStep2.on()
        time.sleep_us(Vel2)
        pinStep2.off()
        time.sleep_us(Vel2)
        
        
def MovDown():
    global pinDirection2
    global Vel2
    global stepsPerRevolution
    global pinStep2
    
    pinDirection2.on()
    for i in range(0,stepsPerRevolution):
        pinStep2.on()
        time.sleep_us(Vel2)
        pinStep2.off()
        time.sleep_us(Vel2)           


def Modo0():
    global ValCal 
    global val
    
    lcd.move_to(0,0)
    lcd.putstr("CONFIGURACION")
    lcd.move_to(0,1)
    lcd.putstr("CAL PROB(mm):" + str(ValCal))
    ValCal = ValCal + val

def Modo1():
    global ValFrz 
    global val
    
    lcd.move_to(0,0)
    lcd.putstr("CONFIGURACION")
    lcd.move_to(0,1)
    lcd.putstr("FUERZA:" + str(ValFrz) +"  ")
    ValFrz = ValFrz + val * 50
    
def Modo2():
    global StrBtn
    
    if(ValFrz >= 0 and ValCal >= 0): #100/20 ValFrz >= 50 and ValCal >= 10
        StrBtn = 'b'
        print("FUERZA: ",ValFrz)
        print("CALIBRE: ", ValCal)
        lcd.move_to(0,0)
        lcd.putstr("OPRIME BOTON")
        lcd.move_to(0,1)
        lcd.putstr("INICIAR      ")
        print(StrBtn)
    else:
        lcd.move_to(0,0)
        lcd.putstr("VALOR INVALIDO")
        lcd.move_to(3,1)
        lcd.putstr("RESETEAR     ")

#LEER ENCODER
def rotary_changed(change):
    global iMode
    global val
    global StrBtn
    
    if change == Rotary.ROT_CW:
        val = val + 1
        #print(val)
    elif change == Rotary.ROT_CCW:
        val = val - 1
        #print(val)
    elif change == Rotary.SW_PRESS:
        lcd.clear()
        time.sleep(0.8)
        iMode = iMode + 1
        val = 0
        if(iMode == 3 and StrBtn == 'a'):
            iMode = 0
            
        elif(iMode == 3 and StrBtn == 'b'):
            StrBtn = 'c'
            #iMode = 3
                    
rotary.add_handler(rotary_changed)



while True:
    if(iMode == 0):
        Modo0()
        
    if(iMode == 1):
        Modo1()
        
    elif(iMode == 2):
        Modo2()

            
#FUNCION SECUENCIA MOTORES    
    if(StrBtn == 'c'):
        if(ELizqDer.value() == 1 and DirID == 'D'):
            MotControlPin.value(1)
            NegOutIDer.value(1)
            MovDer()
            print("M DER")
            
        if(ELizqDer2.value() == 1 and DirID == 'I'):
            MotControlPin.value(1)
            NegOutIDer.value(1)
            MovIzq()
            print("M IZQ")    
           
        #ALTO Y REDIRECCION DERECHA
        elif(ELizqDer.value() == 0 and DirID == 'D'):
            MotControlPin.value(0)
            time.sleep(0.1)
            
            print("stop DER")
            Stop()
            time.sleep(1)
            
            NegOutUD.value(1)
            MovUp()
            time.sleep(2)
            NegOutUD.value(0)
            StopUD()
            
            DirID = 'I'
            print(DirID)
            
            print("SALIENDO DER")
            
            
        #ALTO Y REDIRECCION IZQUIERDA
        elif(ELizqDer2.value() == 0 and DirID == 'I'):
            MotControlPin.value(0)
            time.sleep(0.1)
            
            print("stop IZQ")
            Stop()
            time.sleep(1)
            
            NegOutUD.value(1)
            MovUp()
            time.sleep(2)
            NegOutUD.value(0)
            StopUD()
            
            DirID = 'D'
            print(DirID)
            
            print("SALIENDO IZQ")
            
            
        #TEST
        if(ELUDpwn2.value() == 0):
            NegOutUD.value(0)
            Stop()
            StopUD()
            
            time.sleep(1)
            NegOutUD.value(1)
            MovDown()
            #AutoHome = 'G'
            
            
        """if(AutoHome == 'G'):
            Stop()
            StopUD()
            MovDown()"""
            
        if(ELUDpwn.value() == 0):
            NegOutUD.value(0)
            Stop()
            StopUD()
            #AutoHome = 'F'