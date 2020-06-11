import os
import subprocess
import time
from datetime import datetime
from datetime import timedelta
import requests

#Runs Programs in "pi" folder
def runprog(file):
    p = subprocess.Popen('python '+ file ,shell=True)
    return p


def receiveL():
    Times = []
    buf=''
    counter = 0
    
    firebase_url = 'https://seniordesign-e59ca.firebaseio.com/'
    user = '3xL6MRsUvrN7I2H134ejPGglGgr2'
    
    req = requests.get(firebase_url + '/users/'+ user +'/sensors/LightTimes.json')
    data = req.json()
    n= len(data)
     
    for i in range(0,n):
        if data[i]=='"'and counter == 0:
            counter=counter+1
            continue
        if data[i] == ':':
            buf=buf+'_'
            continue
        if data[i] == '"' and counter == 1:
            Times.append(buf)
            buf=''
            counter = 0
            continue
        buf=buf+data[i]
    return Times



#Tuneables
Receive_Delay = 10 #seconds
Send_Delay = 10 #minutes
Water_Duration = 10 #seconds
Light_Duration = 18 # hours

#Buffers
Water_Times = []
Light_Times = []


#Initialization
init = datetime.now()
Last_Receive=init
Last_Water=init
Last_Light=init


er = runprog('Env_Reg.py') #  Controls chemical pump(s)
sd = runprog('Send_Data.py') # Sends packets of sensor data on an interval for records
s = runprog('Sensors.py') #   Runs sensors on an interval, saves, and sends for display
w = runprog('Water_Pump.py')# Runs water pump on an interval
try:
    while 1:
        
        #Automation

        now = datetime.now() #gets "current" time
        now_hhmm = now.strftime('%H_%M')#Current 'Hour_Minute'
        
        
        #Lights
        num_L = len(Light_Times)
        for j in range (0,num_L):
            if (Light_Times[j] == now_hhmm) and (Last_Light.strftime('%H_%M') != now.strftime('%H_%M')):
                l = runprog('Lights.py')
                Last_Light = now

        #Recieve Data
        receive_delta = timedelta(seconds = Receive_Delay)
        if (now > (Last_Receive + receive_delta)):
            Light_Times = receiveL()
            Last_Receive = now
        
        
        #Programs working?
        if (er.poll() != None):
            print('Regulation error')
        if (sd.poll() != None):
            print('Sending data packet error')
        if (s.poll() != None):
            print('Sensors error')
        if (w.poll() != None):
            print('Water Pump error')
except KeyboardInterrupt:
    time.sleep(1)
    while 1:
        if (er.poll() != None) and (sd.poll() != None) and (s.poll() != None):
            break
        print('Device Shutting Down')    
        time.sleep(2)
    print('Device Succesfully Shutdown')   