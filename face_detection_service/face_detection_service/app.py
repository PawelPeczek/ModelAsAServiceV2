import json
import logging
from functools import partial
from typing import List

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
        channel.basic_ack(delivery_tag=method.delivery_tag)
        logging.info(f"Results registered: {message_content}")
    except Exception as e:
        logging.error(f"Could not process image: {e}")


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
