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
    try:
        message_content = json.loads(body)
        logging.info(f"Processing request: {message_content}")
        image = fetch_processing_input(
            requester_login=message_content[LOGIN_FIELD],
            request_identifier=message_content[RESOURCE_IDENTIFIER_FIELD]
        )
        inference_results = model.infer(image=image)
        logging.info(f"Inference done: {message_content}")
        serialized_results = _inference_results_to_dict(
            inference_results=inference_results
        )
        register_results(
            requester_login=message_content[LOGIN_FIELD],
            request_identifier=message_content[RESOURCE_IDENTIFIER_FIELD],
            results=serialized_results
        )
        send_ack = partial(ack_message, channel=channel, delivery_tag=method.delivery_tag)
        channel.connection.add_callback_threadsafe(send_ack)
        logging.info(f"Results registered: {message_content}")
    except Exception as e:
        logging.error(f"Could not process image: {e}")


def ack_message(channel: Channel, delivery_tag: Any):
    """Note that `channel` must be the same pika channel instance via which
    the message being ACKed was retrieved (AMQP protocol constraint).
    """
    if channel.is_open:
        channel.basic_ack(delivery_tag)
    else:
        # Channel is already closed, so we can't ACK this message;
        # log and/or do something that makes sense for your app in this case.
        pass


def _inference_results_to_dict(
    inference_results:  List[RetinaFaceNetPrediction]
) -> dict:
    return {
        "inference_results": [
            {
                "bounding_box": {
                    "left_top": list(r.bbox.left_top.compact_form),
                    "right_bottom": list(r.bbox.right_bottom.compact_form)
                },
                "confidence": r.confidence.astype(float).item(),
                "landmarks": [
                    list(l.compact_form) for l in r.landmarks
                ]
            } for r in inference_results
        ]
    }


if __name__ == '__main__':
    start_app()
