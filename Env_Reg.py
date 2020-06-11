import csv
import time
from datetime import datetime
from datetime import timedelta
import RPi.GPIO as GPIO

#Time duration
delay = 30 #seconds (Must be larger than the sum of all others)
duration = 1 # second


#Set thresholds
EC_thresh = .1

#Set GPIO numbers (BCM)
EC_GPIO = 17

#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(EC_GPIO, GPIO.OUT)

#Initialize time
last = datetime.now() 
try:
    while(1):
        #Get current time
        now = datetime.now()
        
        #Check if enough time has passed
        if (now > last + timedelta(seconds = delay)): 
            
            #Get most current EC reading
            with open('/home/pi/Sensor Data/Inst/ECInst.txt', mode ='r') as f:
                data = csv.reader(f)
                for row in data:
                    EC = row[0]    
            
            #Check if the EC is too low
            if (float(EC) < EC_thresh):
                #EC pump on
                GPIO.output(EC_GPIO, GPIO.HIGH) #Chemical Pump On
                #sleep for duration
                time.sleep(duration)
                #EC pump off
                GPIO.output(EC_GPIO, GPIO.LOW) #Chemical Pump Off
                
            #Set time of last check
            last = now
            
            #Sleep to conserve CPU
            time.sleep(delay - duration)
except KeyboardInterrupt:
    GPIO.cleanup()
    print('Enviormental Regulation Shutdown Successful')