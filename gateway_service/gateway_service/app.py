import logging
import time
from threading import Thread
from typing import Tuple

import pika
from flask import Flask
from flask_restful import Api

from .handlers.face_detection import FaceDetection
from .handlers.object_detection import ObjectDetection
from .config import RABBIT_PASSWORD, RABBIT_USER, RABBIT_PORT, RABBIT_HOST, \
    PORT, FACE_DETECTION_CHANNEL, GATEWAY_API_BASE_PATH

logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
STOP_HEARTBEAT = False


def keep_rabbit_connection_online(connection: pika.BlockingConnection) -> None:
    while not STOP_HEARTBEAT:
        logging.info("RabbitMQ heartbeat.")
        connection.process_data_events()
        time.sleep(30)


def create_api() -> Tuple[Api, Thread]:
    api = Api(app)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBIT_HOST,
            port=RABBIT_PORT,
            credentials=pika.PlainCredentials(
                username=RABBIT_USER,
                password=RABBIT_PASSWORD
            ),
            heartbeat=60
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue=FACE_DETECTION_CHANNEL)
    api.add_resource(
        FaceDetection,
        construct_api_url('detect_faces'),
        resource_class_kwargs={
            'rabbit_channel': channel
        }
    )
    api.add_resource(
        ObjectDetection,
        construct_api_url('detect_objects')
    )
    heartbeat = Thread(target=keep_rabbit_connection_online, args=(connection, ))
    heartbeat.start()
    return api, heartbeat


def construct_api_url(url_postfix: str) -> str:
    return f"{GATEWAY_API_BASE_PATH}/{url_postfix}"


if __name__ == '__main__':
    api, heartbeat = create_api()
    try:
        app.run(host='0.0.0.0', port=PORT)
    except KeyboardInterrupt:
        STOP_HEARTBEAT = True
        heartbeat.join()
