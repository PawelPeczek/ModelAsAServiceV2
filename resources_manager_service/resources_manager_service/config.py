import os

BASE_RESOURCE_PATH = '/maas_workshop/v2/resources_manager'
PORT = 50002
PERSISTENCE_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "storage"
))
INPUT_IMAGE_NAME = "input_image.jpeg"
