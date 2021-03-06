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
        resource_identifier = f'{uuid4()}'
        target_path = os.path.join(
            build_base_resource_path(
                requester_login=requester_login,
                resource_identifier=resource_identifier
            ),
            INPUT_IMAGE_NAME
        )
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        request.files['image'].save(target_path)
        return make_response(
            {
                LOGIN_FIELD_NAME: requester_login,
                RESOURCE_IDENTIFIER_FIELD_NAME: resource_identifier
            },
            200
        )

    def get(self) -> Response:
        data = self.__get_request_parser.parse_args()
        requester_login = data[LOGIN_FIELD_NAME]
        resource_identifier = data[RESOURCE_IDENTIFIER_FIELD_NAME]
        resources_dir = build_base_resource_path(
            requester_login=requester_login,
            resource_identifier=resource_identifier
        )
        if not os.path.isdir(resources_dir):
            return make_response(
                {'msg': 'Incorrect resource identifiers.'}, 500
            )
        try:
            return send_from_directory(
                directory=resources_dir,
                filename=INPUT_IMAGE_NAME,
                as_attachment=True
            )
        except FileNotFoundError:
            return make_response(
                {'msg': 'There is no input file detected.'}, 500
            )
