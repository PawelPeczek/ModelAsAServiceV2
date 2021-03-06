from flask import Flask
from flask_restful import Api

from .handlers.input_image_register import InputImageRegister
from .handlers.face_detection_register import FaceDetectionRegister
from .config import BASE_RESOURCE_PATH, PORT

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True


def create_api() -> Api:
    api = Api(app)
    api.add_resource(
        InputImageRegister,
        construct_api_url('input_image_register')
    )
    api.add_resource(
        FaceDetectionRegister,
        construct_api_url('face_detection_register')
    )
    return api


def construct_api_url(resource_postfix: str) -> str:
    return f'{BASE_RESOURCE_PATH}/{resource_postfix}'


if __name__ == '__main__':
    api = create_api()
    app.run(host='0.0.0.0', port=PORT)
