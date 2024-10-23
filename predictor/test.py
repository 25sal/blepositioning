import pandas as pd
from datetime import datetime
from aipredictor import RSSIPredictor
from matplotlib import pyplot as plt

file_path = 'data/test/'

filenames = ['1_dx_2volte.csv','2_sx_2volte.csv','3_centro_2volte.csv','4_Circonferenza.csv']
for filename in filenames:
    df =pd.read_csv(file_path + filename)
    timestamp = 0
            
    aimodel = 'rf'
    pred = RSSIPredictor(aimodel)      
    pred.rssiwindow = 1
            
    x_values = []
    y_values = [] 
            
    for index, row in df.iterrows():
        epoch = datetime.strptime(row[0],"%Y-%m-%dT%H:%M:%S.%f").strftime("%s.%f")
        payload = {
            "mac": row[1],
            "RSSI": row[2],
            "timestamp": timestamp
            }
        timestamp += 1
        positions = pred.addrssi(payload, payload['mac'],update=False)
        if positions is not None:
            x_values.append(positions[0])
            y_values.append(positions[1])
    plt.figure()
    plt.title(filename)
    plt.scatter(x_values, y_values)
    plt.savefig('data/test/'+filename+'.png')

