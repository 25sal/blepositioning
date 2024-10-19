import paho.mqtt.client as mqttClient
import json
import pandas as pd
import paho
import time


if __name__ == "__main__":

    df =pd.read_csv('data/trace.csv')
    print(df.head())
    

    if paho.mqtt.__version__[0] > '1':
        client = mqttClient.Client(mqttClient.CallbackAPIVersion.VERSION1)
    else:

        client = mqttClient.Client()

    client.username_pw_set("iotrobotic", "iotrobotic")
    #client.tls_set('root.ca', certfile='c1.crt', keyfile='c1.key')
    client.connect("127.0.0.1", 1883, 60)
    
    timestamp = 0
    for index, row in df.iterrows():
        for i in range(3,len(df.columns)):
            payload = {
                "mac": df.columns[i],
                "RSSI": row[i],
                "timestamp": timestamp
            }
            client.publish("rssi/1", json.dumps(payload))
            print(f"Published {json.dumps(payload)}")
            timestamp += 1
            time.sleep(1)
   
    
    