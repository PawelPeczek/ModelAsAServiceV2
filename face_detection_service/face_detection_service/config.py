import os

FACE_DETECTION_CHANNEL = "face_detection_channel"
RABBIT_HOST = os.getenv("RABBIT_HOST", "127.0.0.1")
RABBIT_PORT = 5672
RABBIT_USER = os.getenv("RABBIT_USER", "guest")
RABBIT_PASSWORD = os.getenv("RABBIT_PASSWORD", "guest")
RESOURCE_MANAGER_BASE_URI = "http://127.0.0.1:50002/maas_workshop/v2/resources_manager/"
INPUT_IMAGE_FETCHING_URI = f"{RESOURCE_MANAGER_BASE_URI}input_image_register"
RESULT_POSTING_URI = f"{RESOURCE_MANAGER_BASE_URI}face_detection_register"
WEIGHTS_PATH = os.path.join("/weights", "weights.pth")
TOP_K = 50
CONFIDENCE_THRESHOLD = 0.2
