import csv
import json
import requests
from datetime import datetime
from datetime import timedelta
import numpy as np
import time
import RPi.GPIO as GPIO

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

import Adafruit_DHT
sen = Adafruit_DHT.DHT22

#Sensor Functions            
def pH():
    phPin = 2
    voltage_step = .1
    #calibrationslope
    pHcal = 8.098
    pHstep =.002346
    pHin = float(mcp.read_adc(pin))
    print(pHin)
    pH = float((pHin*-pHstep*pHcal)+15.67)
    return pH

def EC():
    #MCP3008 pins 0-7
    vinPin = 5
    voutPin = 7
    K= float(.74)
    rKnown = 965
    ECCalibration = float(.172)
    #Turning on the sensor
    GPIO.output(ECpin, 0)
    
    #collect raw data from the ADC
    vin = float(mcp.read_adc(vinPin))
    vout = float(mcp.read_adc(voutPin))
    #Turning off the sensor
    GPIO.output(ECpin, 1)
    #Open Circuit
    if (vin==vout):
        return 0
    #Calculate the EC
    else:
        #Equation to find out the unknown resistance
        rUnknown = float(rKnown/((vin/vout)-1))
        #Finding the unkown conductance
        cUnknown = float((1/rUnknown)*1000)
        #Finding the conductance per cm
        return float(cUnknown*K)
    
def UV():
    pin = 0
    voltage_step = .1
    #Reading the analog input on the pin
    self = float(mcp.read_adc(pin))
    UvI = (self * voltageStep)*10 # Returns current UV index
    return UvI
    
def VisIrChange(select):
    bus.write_byte(i2c_address,select1)
    if __name__ == '__main__':

        tsl = tsl2591()  # initialize
        tsl.gain = 1
        lux = tsl.get_current()
        return lux['lux']
    
def lux():
    i2c_ch = 1
    i2c_address = 0x70
    bus = smbus.SMBus(i2c_ch)
    
    select = 0b00000001
    lux1 = VisIrChange(select)
    time.sleep(0.5)
    
    select = 0b00000010
    lux2 = VisIrChange(select)
    time.sleep(0.5)
    
    select = 0b0000100
    lux3 = VisIrChange(select)
    time.sleep(0.5)
    
    return lux1,lux2,lux3

#Gets Data from both Humidity/Temperature Sensors
def tempAndHum():
    #pins on the pi for the DHT sensors
    inside = 21
    outside = 20
    [TempIn,HumIn] = Adafruit_DHT.read_retry(sen, inside)
    [TempOut,HumOut] = Adafruit_DHT.read_retry(sen, outside)
    return TempIn,HumIn,TempOut,HumOut

#Sends sensor data to be displayed
def send(data,stp,firebase_url):
    size = len(data)
    for j in range(0, size):
        result = requests.put(firebase_url + '/users/3xL6MRsUvrN7I2H134ejPGglGgr2/sensors/' + stp[j] + '/' + '.json', data=json.dumps(data[j]))
        print('Record inserted. Result Code = ' + str(result.status_code) + ',' + result.text)

#Saves sensor data to .txt f
def save(data,now,stp):
    size = len(data)
    for j in range(0,size):
        with open('/home/pi/Sensor Data/'+stp[j]+'_'+now.strftime('%m-%d-%y_%H')+'.txt', mode = 'a') as data_file:
            f = csv.writer(data_file, delimiter = ',')
            f.writerow([data[j],now.strftime('%H_%M_%S')])
    with open('/home/pi/Sensor Data/Inst/ECInst.txt', mode ='w') as data_file:
        f= csv.writer(data_file)
        f.writerow([data[1],0])
# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

#Constants       
delay = 10 #seconds
firebase_url = 'https://seniordesign-e59ca.firebaseio.com/'
stp = ['pH','EC','TempIn','HumIn','TempOut','HumOut','UV','Lux1', 'Lux2','Lux3']

#Set GPIO pins (BCM)
ECpin=6

#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(ECpin,GPIO.OUT)
GPIO.setup(vinPin,GPIO.OUT)
GPIO.setup(voutPin,GPIO.OUT)

#Initialize
last = datetime.now()-timedelta(seconds = delay)
try:
    while(1):
        now = datetime.now()
        data = np.zeros(len(stp))
        if (now > (last + timedelta(seconds = delay))):
            #Enter Sensor Data into a Buffer
            #pH Sensor
            data[0] = pH()
            #EC Sensor
            data[1] = EC()
            #Temp/Humidity Sensors
            [data[2],data[3],data[4],data[5]] = tempAndHum()
            #UV Sensor
            data[6] = UV()
            #Visible/IR Sensors
            [data[7],data[8],data[9],data[10]] = lux()
            
            #Saves data                 
            save(data,now,stp)
            #Sends values to be displayed on app
            send(data,stp,firebase_url)
            
            #Sets last time for cycle
            last = now
            #Sleeps until next sensing
            time.sleep(delay)
            
except KeyboardInterrupt:
    GPIO.cleanup()
    print('Sensors Shutdown Sucessful')