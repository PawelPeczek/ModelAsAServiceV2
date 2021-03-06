import json

from flask import Response, make_response
from pika.channel import Channel

from ..config import INPUT_IMAGE_INGEST_URL, FACE_DETECTION_CHANNEL, \
    FETCH_RESULTS_URL
from .proxy import Proxy


class FaceDetection(Proxy):

    def __init__(self, rabbit_channel: Channel):
        super().__init__()
        self.__rabbit_channel = rabbit_channel

    def post(self) -> Response:
        registration_response = self._forward_message(target_url=INPUT_IMAGE_INGEST_URL)
        if registration_response.status_code != 200:
            return registration_response
        try:
            self.__rabbit_channel.basic_publish(
                exchange="",
                routing_key=FACE_DETECTION_CHANNEL,
                body=json.dumps(registration_response.json)
            )
        except Exception as e:
            return make_response({"msg": f"Internal error, {e}"}, 500)
        return registration_response

    def get(self) -> Response:
        return self._forward_message(target_url=FETCH_RESULTS_URL)

