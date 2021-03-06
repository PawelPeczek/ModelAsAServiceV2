import json

import numpy as np
import cv2 as cv
import requests

from .config import INPUT_IMAGE_FETCHING_URI, RESULT_POSTING_URI

LOGIN_FIELD = "login"
RESOURCE_IDENTIFIER_FIELD = "resource_identifier"
FACE_DETECTION_RESULTS_FIELD = "face_detection_results"


def fetch_processing_input(
    requester_login: str,
    request_identifier: str
) -> np.ndarray:
    payload = {
        LOGIN_FIELD: requester_login,
        RESOURCE_IDENTIFIER_FIELD: request_identifier
    }
    response = requests.get(INPUT_IMAGE_FETCHING_URI, data=payload)
    if response.status_code != 200:
        raise RuntimeError("Could not process request")
    data = np.fromstring(response.content, dtype=np.uint8)
    return cv.imdecode(data, cv.IMREAD_COLOR)


def register_results(
    requester_login: str,
    request_identifier: str,
    results: dict
) -> None:
    payload = {
        LOGIN_FIELD: requester_login,
        RESOURCE_IDENTIFIER_FIELD: request_identifier,
        FACE_DETECTION_RESULTS_FIELD: json.dumps(results)
    }
    response = requests.post(RESULT_POSTING_URI, data=payload)
    if response.status_code != 200:
        raise RuntimeError("Could not send back results.")
