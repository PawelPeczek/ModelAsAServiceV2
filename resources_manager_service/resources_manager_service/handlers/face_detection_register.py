import json
import os
from json.decoder import JSONDecodeError

from flask import Response, make_response
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from .utils import safe_load_json, initialize_request_parser, \
    build_base_resource_path, persist_json_result
from .config import LOGIN_FIELD_NAME, RESOURCE_IDENTIFIER_FIELD_NAME
from ..config import PERSISTENCE_DIR


FACE_DETECTION_FILE_NAME = "face_detection.json"
FACE_DETECTION_RESULTS_FIELD = "face_detection_results"


class FaceDetectionRegister(Resource):

    def __init__(self):
        self.__get_request_parser = initialize_request_parser()
        self.__post_request_parser = self.__initialize_post_request_parser()

    def get(self) -> Response:
        data = self.__get_request_parser.parse_args()
        requester_login = data[LOGIN_FIELD_NAME]
        resource_identifier = data[RESOURCE_IDENTIFIER_FIELD_NAME]
        raise NotImplementedError()

    def post(self) -> Response:
        data = self.__post_request_parser.parse_args()
        requester_login = data[LOGIN_FIELD_NAME]
        resource_identifier = data[RESOURCE_IDENTIFIER_FIELD_NAME]
        raise NotImplementedError()

    def __initialize_post_request_parser(self) -> RequestParser:
        parser = initialize_request_parser()
        parser.add_argument(
            FACE_DETECTION_RESULTS_FIELD,
            help=f'Field "{FACE_DETECTION_RESULTS_FIELD}" must '
                 'be specified in this request.',
            required=True
        )
        return parser
