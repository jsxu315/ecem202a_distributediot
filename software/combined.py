import os
import json
import time
from datetime import datetime
from collections import Counter
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
from mediapipe.tasks import python
from mediapipe.tasks.python.audio.core import audio_record
from mediapipe.tasks.python.components import containers
from mediapipe.tasks.python import audio
import sys

# Add Hailo library path
sys.path.append("/home/pi4/my_project_env/project1/hailo-rpi5-examples/basic_pipelines")

# Import hailo and Hailo-specific utilities
import hailo
from hailo_rpi_common import app_callback_class, get_caps_from_pad, get_numpy_from_buffer
from detection_pipeline import GStreamerDetectionApp


# imports from other file
import redis
from rediscluster import RedisCluster



# Base directories for outputs
BASE_DIR = os.path.expanduser("~/Desktop/test")
JSON_SAVE_DIR = os.path.join(BASE_DIR, "json")
os.makedirs(JSON_SAVE_DIR, exist_ok=True)

# Initialize GStreamer
Gst.init(None)

# Audio classification parameters
MODEL_PATH = "/home/pi4/my_project_env/project1/mediapipe-samples/examples/audio_classifier/raspberry_pi/yamnet.tflite"
MAX_RESULTS = 5
OVERLAPPING_FACTOR = 0.5
SAMPLE_RATE = 16000
NUM_CHANNELS = 1
AUDIO_DURATION = 5  # Duration for audio recording

# Initialize classification results
classification_results = []


# Redis client
client = None 

class UserAppCallback(app_callback_class):
    """Custom callback class for Hailo detections."""
    def __init__(self):
        super().__init__()
        self.last_event_time = time.time()  # Time of last event


def record_audio():
    """Classify audio using Mediapipe without saving sound files."""
    global classification_results

    # Initialize the audio classifier
    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = audio.AudioClassifierOptions(
        base_options=base_options,
        running_mode=audio.RunningMode.AUDIO_STREAM,
        max_results=MAX_RESULTS,
        result_callback=save_audio_result
    )
    classifier = audio.AudioClassifier.create_from_options(options)

    # Initialize audio recorder
    buffer_size = 15600
    audio_format = containers.AudioDataFormat(NUM_CHANNELS, SAMPLE_RATE)
    recorder = audio_record.AudioRecord(NUM_CHANNELS, SAMPLE_RATE, buffer_size)
    audio_data = containers.AudioData(buffer_size, audio_format)

    recorder.start_recording()
    start_time = time.time()
    print("Recording audio...")

    while time.time() - start_time < AUDIO_DURATION:
        # Read audio data and classify
        data = recorder.read(buffer_size)
        audio_data.load_from_array(data)
        classifier.classify_async(audio_data, int((time.time() - start_time) * 1000))
        time.sleep(OVERLAPPING_FACTOR)  # Ensure overlapping

    print("Audio recording completed.")
    return aggregate_audio_predictions()


def save_audio_result(result: audio.AudioClassifierResult, timestamp_ms: int):
    """Save Mediapipe audio classification results."""
    classification_results.append((timestamp_ms, result))


def aggregate_audio_predictions():
    """Aggregate predictions over the recording duration."""
    global classification_results

    # Count category occurrences
    category_counter = Counter()
    for _, result in classification_results:
        for classification in result.classifications:
            for category in classification.categories:
                category_counter[category.category_name] += category.score

    # Get the most frequent category
    most_common = category_counter.most_common(MAX_RESULTS)
    mic_label = most_common[0][0] if most_common else "unknown"
    mic_vector = [score for _, score in most_common]
    classification_results.clear()  # Reset for next recording
    return mic_label, mic_vector


def app_callback(pad, info, user_data):
    global client
    
    """Hailo detection pipeline callback."""
    buffer = info.get_buffer()
    if buffer is None:
        return Gst.PadProbeReturn.OK

    current_time = time.time()
    if current_time - user_data.last_event_time >= 10:  # Trigger every 30 seconds
        user_data.last_event_time = current_time
        print("Processing Hailo detection and recording audio...")

        # Hailo detection processing
        roi = hailo.get_roi_from_buffer(buffer)
        detections = roi.get_objects_typed(hailo.HAILO_DETECTION)
        detected_objects = {}
        for detection in detections:
            label = detection.get_label()
            confidence = detection.get_confidence()
            if confidence > 0.3:
                detected_objects[label] = detected_objects.get(label, 0) + 1

        # Generate Hailo JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_data = {
            "new_camera_event": True,
            "camera_label": ", ".join(detected_objects.keys()),
            "object_counts": detected_objects,
            "timestamp": timestamp,
        }
        json_filename = os.path.join(JSON_SAVE_DIR, f"camera_event_{timestamp}.json")
        with open(json_filename, "w") as json_file:
            json.dump(json_data, json_file, indent=4)
        print(f"Camera JSON saved: {json_filename}")
        
        # Create camera json object for database 
        camera_json = json.dumps(json_data)
        print(f"Camera JSON string: {camera_json}")

        # Record and classify audio
        mic_label, mic_vector = record_audio()

        # Generate audio JSON
        audio_json_data = {
            "new_mic_event": True,
            "mic_label": mic_label,
            "mic_vector": mic_vector,
            "timestamp": timestamp,
        }
        audio_json_filename = os.path.join(JSON_SAVE_DIR, f"mic_event_{timestamp}.json")
        with open(audio_json_filename, "w") as json_file:
            json.dump(audio_json_data, json_file, indent=4)
        print(f"Audio JSON saved: {audio_json_filename}")
        
        # Create mic json object for database
        mic_json = json.dumps(audio_json_data)
        print(f"Mic JSON string: {mic_json}")
        
        
        if client is None: # Connect to the database if we haven't already 
            # NOTE: check the port and host
            print("!!!!!!!!!!!!!! client is None")
            #client = redis.Redis(host="localhost", port=6379, decode_responses=True)
            startup_nodes = [{"host": "localhost", "port": "6379"}]
            client = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

        else:
            print("Have client")
            
        pipeline = client.pipeline()
        redis_mic_key = "mic_" + timestamp # Note: the timestamps will be slightly off from when the audio/video was actually recorded becuase of when the variable is declared
        redis_camera_key = "camera_" + timestamp
        pipeline.json().set(redis_mic_key, "$", mic_json)
        pipeline.json().set(redis_camera_key, "$", camera_json)
        res = pipeline.execute()
        

    return Gst.PadProbeReturn.OK


if __name__ == "__main__":
    print("Starting the combined Hailo and Mediapipe pipeline...")
    user_data = UserAppCallback()
    app = GStreamerDetectionApp(app_callback, user_data)
    app.run()
