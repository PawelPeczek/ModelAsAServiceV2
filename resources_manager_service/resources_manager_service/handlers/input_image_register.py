import os
from uuid import uuid4

from flask import request, Response, make_response, send_from_directory
from flask_restful import Resource

from .utils import initialize_request_parser, build_base_resource_path
from .config import RESOURCE_IDENTIFIER_FIELD_NAME, LOGIN_FIELD_NAME
from ..config import INPUT_IMAGE_NAME


class InputImageRegister(Resource):

    def __init__(self):
        self.__get_request_parser = initialize_request_parser()
        self.__post_request_parser = initialize_request_parser(
            include_resource_identifier=False
        )

    def post(self) -> Response:
        if 'image' not in request.files:
            return make_response(
                {'msg': 'Field called "image" must be specified'}, 400
            )
        data = self.__post_request_parser.parse_args()
        requester_login = data[LOGIN_FIELD_NAME]
        raise NotImplementedError()

    def get(self) -> Response:
        data = self.__get_request_parser.parse_args()
        requester_login = data[LOGIN_FIELD_NAME]
        resource_identifier = data[RESOURCE_IDENTIFIER_FIELD_NAME]
        raise NotImplementedError()
