import torchvision
from flask import Flask
from flask_restful import Api

from .config import \
    OBJECT_DETECTION_PATH, CONFIDENCE_THRESHOLD, MAX_IMAGE_DIM, PORT
from .handlers.object_detection import \
    ObjectDetection

app = Flask(__name__)


def create_api() -> Api:
    api = Api(app)
    model = torchvision.models.detection.retinanet_resnet50_fpn(pretrained=True)
    model.eval()
    api.add_resource(
        ObjectDetection,
        OBJECT_DETECTION_PATH,
        resource_class_kwargs={
            'model': model,
            'confidence_threshold': CONFIDENCE_THRESHOLD,
            'max_image_dim': MAX_IMAGE_DIM
        }
    )
    return api


api = create_api()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
