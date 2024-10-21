import paho.mqtt
import paho.mqtt.client as mqttClient
import json
import argparse
import logging
import time
import sys
from pathlib import Path
from positioning import Positioning 
import joblib
import requests

logging.basicConfig(level=logging.DEBUG)
logger =  logging.getLogger()

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))



class RSSIPredictor:
    ready = False
    rssi = {}
    rssiwindow = 4
    positioning = None
   
    def __init__(self, aimodel):
        self.ready = True
        self.scaler = joblib.load('predictor/aimodels/scaler.pkl')
        self.positioning = Positioning(model_type=aimodel, optimize=False)
        model = joblib.load('predictor/aimodels/'+aimodel+'_model.pkl')
        self.positioning.model_x = model['model_x']
        self.positioning.model_y = model['model_y']
    
    def addrssi(self, rssi, mac):
        # add rssi to the model
        if mac not in self.rssi:
            self.rssi[mac] = []
        self.rssi[mac].append(rssi)

        next_positions = self.predict()
    
        if next_positions is not None:
            data = {'id': 1, 'x': next_positions[0], 'y': next_positions[1], 'z': 0}
            #send the position to the api-service by an http post request
            url = "http://localhost:5000/api-service/update"
            headers = {'Content-Type': 'application/json'}
            # print(data)
            response = requests.post(url, headers=headers, data=json.dumps(data))

    def predict(self):
        if len(self.rssi.keys())>=3 :
            avg_values = []
            for mac in self.rssi.keys():
              rssi = self.rssi[mac]
              if len(rssi) >= self.rssiwindow:
                avg = 0
                for item in rssi:
                    avg += item['RSSI']
                avg_values.append(avg/len(rssi))
                
            if len(avg_values) >= 3:
                scaled_values = self.scaler.transform([list(avg_values)])
                position = self.positioning.predict(scaled_values)[0]
                for mac in self.rssi.keys():
                    del self.rssi[mac][0]    
                print(position)
                return position
        return None
            
        
    def getlastrssi(self, mac):
        if mac in self.rssi:
            return self.rssi[mac][-1]['timestamp']
        else:
            return None        
        
    
     
class MqttClient:
    
    predictor = None
    
    def __init__(self, predictor):
        self.predictor = predictor
    
    # Funzione per processare il payload JSON
    def process_payload(self, id, payload_json):
        try:
            mac_address = payload_json.get("mac")
            rssi = payload_json.get("RSSI")
            timestamp = payload_json.get("timestamp")

            if mac_address and rssi is not None:
                # logging.info(f"Ricevuto {json.dumps(payload_json)} al tempo '{timestamp}'")
                # Controlla se il timestamp è più recente rispetto all'ultimo salvato
                last_timestamp = self.predictor.getlastrssi(mac_address)
                if  last_timestamp is None or  last_timestamp < timestamp:
                    self.predictor.addrssi(
                        {
                            "mac": mac_address,
                            "RSSI": rssi,
                            "timestamp": timestamp
                            },
                        mac_address)
                else:
                    logging.info(f"Scartato payload obsoleto per {mac_address}")
        except Exception as e:
            logging.error(f"Errore nel processare il payload: {e}")

                
           
        
    def on_message(self, mosq, obj, msg):
        # logger.info(f"Ricevuto messaggio: {msg.topic} {str(msg.payload)}")
        # collect rssi data from mesg and when ready computes the position
        try:
            # id should be taked by last part of topic
            id = msg.topic.split("/")[-1]
            
            msg = msg.payload.decode()
            payload_json = json.loads(msg)
            
            # Se il payload è una lista, iterare attraverso di essa
            if isinstance(payload_json, list):
                for item in payload_json:
                    self.process_payload(id, item)
            else:
                self.process_payload(id, payload_json)

        except Exception as e:
            logging.error(f"Errore nel processare il messaggio: {e}")
            logging.error(f"Payload: {msg}")
            pass        

if __name__ == "__main__": 
    aimodel = 'rf'
    pred = RSSIPredictor(aimodel)

  
    if paho.mqtt.__version__[0] > '1':
        client = mqttClient.Client(mqttClient.CallbackAPIVersion.VERSION1)
    else:
        client = mqttClient.Client()

    mqttClient = MqttClient(pred)
    client.on_message = mqttClient.on_message
    
    client.username_pw_set("iotrobotic", "iotrobotic")
    #client.tls_set('root.ca', certfile='c1.crt', keyfile='c1.key')
    client.connect("127.0.0.1", 1883, 60)
    client.subscribe(f"rssi/1", 0)
    
    client.loop_forever() 