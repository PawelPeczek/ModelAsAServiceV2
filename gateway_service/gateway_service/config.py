import os

PORT = 50000
FACE_DETECTION_CHANNEL = "face_detection_channel"
RABBIT_HOST = os.getenv("RABBIT_HOST", "127.0.0.1")
RABBIT_PORT = 5672
RABBIT_USER = os.getenv("RABBIT_USER", "guest")
RABBIT_PASSWORD = os.getenv("RABBIT_PASSWORD", "guest")
OBJECT_DETECTION_URL = "http://127.0.0.1:50001/maas_workshop/v2/object_detection/detect"
INPUT_IMAGE_INGEST_URL = "http://127.0.0.1:50002/maas_workshop/v2/resources_manager/input_image_register"
FETCH_RESULTS_URL = "http://127.0.0.1:50002/maas_workshop/v2/resources_manager/face_detection_register"
GATEWAY_API_BASE_PATH = "/maas_workshop/v2/gateway"
