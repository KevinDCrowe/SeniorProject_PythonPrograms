import csv
import json
from datetime import timedelta
from datetime import datetime
import time

#Important Stuff
firebase_url = 'https://seniordesign-e59ca.firebaseio.com/'
stp = ['pH','EC','TempIn','HumIn','TempOut','HumOut','UV','Lux1', 'Lux2','Lux3','Lux4']

#Main
sizetp = len(stp)
last_send = datetime.now()
try:
    while(1):
        now = datetime.now()
        if (last_send.strftime('%m_%d_%y_%H') != now.strftime('%m_%d_%y_%H')):
            
            for j in range (0,sizetp-1):#Cycles through the sensors
                try:
                    data={'value':[],'timestamp':[] #Creates an empty buffer for the data   
                    }
                    last = now - timedelta(hours = 1)
                    
                    with open('/home/pi/Sensor Data/'+last_send.strftime('%m_%d_%y_%H')+'/'+stp[j]+'.txt', mode='r') as data_file:
                        
                        csv_reader=csv.reader(data_file, delimiter=',')#reads csv file
                        
                        line_count=0   #Reads CSV file and converts it to the JSON format
                        for row in csv_reader:
                            data['value'].append(row[0])
                            data['timestamp'].append(row[1])
                            line_count += 1
                    last_send = now

                except IOError:
                    print('Failed to send. Retrying...')
        time.sleep(600)        
except KeyboardInterrupt:
    print('Sending Data Shutdown Success')