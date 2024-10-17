import paho.mqtt
import paho.mqtt.client as mqttClient
import json
import argparse
import logging
import time
import sys

from pathlib import Path

logging.basicConfig(level=logging.DEBUG)
logger =  logging.getLogger()

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

class RSSIPredictor:
    ready = False
   
     

        
        
    def on_message(self, mosq, obj, msg):
       # collect rssi data from mesg and when ready computes the position
       
       if self.ready:
           #send the position to the api-service by an http post request
           url = "http://localhost:5000/api-service/update"
           headers = {'Content-Type': 'application/json'}
           data = {'id': self.id, 'x': 0, 'y': 0, 'z': 0}
           response = requests.post(url, headers=headers, data=json.dumps(data))
           
                
              

if __name__ == "__main__":
  
    if paho.mqtt.__version__[0] > '1':
        client = mqttClient.Client(mqttClient.CallbackAPIVersion.VERSION1)
    else:
        client = mqttClient.Client()

    client.on_message = w.on_message
    
    client.username_pw_set("iotrobotic", "iotrobotic")
    #client.tls_set('root.ca', certfile='c1.crt', keyfile='c1.key')
    client.connect("127.0.0.1", 1883, 60)

    client.subscribe(f"rssi/{w.id}", 0)
    
    client.loop_forever() 