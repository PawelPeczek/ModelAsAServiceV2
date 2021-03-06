from flask import Response

from ..config import OBJECT_DETECTION_URL
from .proxy import Proxy


class ObjectDetection(Proxy):

    def post(self) -> Response:
        return self._forward_message(target_url=OBJECT_DETECTION_URL)
