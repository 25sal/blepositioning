
# Installation
## Server side
- Install python3 requirements
- Create the mqtt container
```bash
   cd mqtt5
   docker compose up
```  
- Run the flask application
```python
   cd api-service
   python3 app.py
```
- run the predictor (which receive the rssi data, computes the user position and use the api-service to update it)
  
## Client side
- Install the app and configure user id, and mqtt address
- Open the browser
  


# Future works 
## for multi users and multi-spaces
- ask for the user id
- define a room
- relate the objects to a room
- relate the ble id to the room
  
