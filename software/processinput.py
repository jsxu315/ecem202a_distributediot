# Runs continuously on the raspberry pi 

import json
import redis
import time 
from datetime import datetime

should_run = True
client = None
while should_run:
    # Dummy -- add a delay 
    time.sleep(10) # 10 second delay 
    current_datetime = datetime.now().isoformat()
    
    # Sample mic data 
        # TODO 

    # Process mic data and produce a label (ML)
        # Yaqi's code to produce a label from the mic data 

    # Dummy data 
    new_mic_event = True
    mic_label = 'person_talking'
    mic_vector = [0.1, 0.2, 0.3]

    # For now, make a dummy JSON 
    if new_mic_event: 
        mic_entry_dict = {}
        mic_entry_dict['event'] = mic_label
        mic_entry_dict['timestamp'] = current_datetime
        mic_entry_dict['vector'] = mic_vector
        mic_json = json.dumps(mic_entry_dict)


    # Sample camera data 
        # TODO 
    # Process camera data and produce a label (ML)
        # Yaqi's code to produce a label from the camera data 

    # Dummy data    
    new_camera_event = True
    camera_label = 'tall_person_seen'
    camera_vector = [0.4, 0.5, 0.6]

    # For now, make a dummy JSON 
    if new_camera_event:
        camera_entry_dict = {}
        camera_entry_dict['event'] = camera_label
        camera_entry_dict['timestamp'] = current_datetime
        camera_entry_dict['vector'] = camera_vector
        camera_json = json.dumps(camera_entry_dict)


    # Write camera and/or mic data into local database, if any classifications were produced 
    # For now, just write both dummies 
    if client is None: # Connect to the database if we haven't already 
        # NOTE: check the port 
        client = redis.Redis(host="localhost", port=6379, decode_responses=True)

    pipeline = client.pipeline() 
    # Redis is a key-value store 
    # Here, the key is the timestamp, and the value is the JSON. 
    

    # TODO: should probably keep camera and mic data in separate databases 
    if new_mic_event:
        redis_mic_key = "mic_" + current_datetime
        pipeline.json().set(redis_mic_key, "$", mic_json)

    if new_camera_event:
        redis_camera_key = "camera_" + current_datetime
        pipeline.json().set(redis_camera_key, "$", camera_json)

    res = pipeline.execute()

    should_run = False # Just run the loop once to test it 
    # Maybe in a separate script/process: 
    # Grab other databases' updates (does Redis handle?)


    # Handle queries to the database? (does Redis handle?) 
