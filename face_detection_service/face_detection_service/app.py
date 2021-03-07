import json
import logging
from functools import partial
from threading import Thread
from typing import List, Any

import pika
from pika import spec
from pika.channel import Channel
from retina_face_net import RetinaFaceNet, RetinaFaceNetPrediction

from .communication import fetch_processing_input, register_results, \
    LOGIN_FIELD, RESOURCE_IDENTIFIER_FIELD
from .config import RABBIT_HOST, RABBIT_PORT, RABBIT_USER, RABBIT_PASSWORD, \
    FACE_DETECTION_CHANNEL, WEIGHTS_PATH, TOP_K, CONFIDENCE_THRESHOLD

logging.getLogger().setLevel(logging.INFO)


def start_app() -> None:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBIT_HOST,
            port=RABBIT_PORT,
            credentials=pika.PlainCredentials(
                username=RABBIT_USER,
                password=RABBIT_PASSWORD
            )
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue=FACE_DETECTION_CHANNEL)
    channel.basic_qos(prefetch_count=1)
    model = RetinaFaceNet.initialize(
        weights_path=WEIGHTS_PATH,
        top_k=TOP_K,
        confidence_threshold=CONFIDENCE_THRESHOLD
    )
    channel.basic_consume(
        queue=FACE_DETECTION_CHANNEL,
        on_message_callback=partial(on_face_detection, model=model)
    )
    channel.start_consuming()


def on_face_detection(
    channel: Channel,
    method: spec.Basic.Deliver,
    properties: spec.BasicProperties,
    body: str,
    model: RetinaFaceNet
) -> None:
    logging.info("Starting worker thread.")
    worker_thread = Thread(
        target=start_face_detection,
        args=(channel, method, properties, body, model,)
    )
    worker_thread.daemon = True
    worker_thread.start()
    logging.info("Working thread started.")


def start_face_detection(
    channel: Channel,
    method: spec.Basic.Deliver,
    properties: spec.BasicProperties,
    body: str,
    model: RetinaFaceNet
) -> None:
    # https://stackoverflow.com/questions/51752890/how-to-disable-heartbeats-with-pika-and-rabbitmq
    raise NotImplementedError()


def ack_message(channel: Channel, delivery_tag: Any):
    raise NotImplementedError()


def _inference_results_to_dict(
    inference_results:  List[RetinaFaceNetPrediction]
) -> dict:
    raise NotImplementedError()


if __name__ == '__main__':
    start_app()
