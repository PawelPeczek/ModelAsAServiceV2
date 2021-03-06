import json
import os
from typing import Optional

from flask_restful import reqparse

from .config import LOGIN_FIELD_NAME, RESOURCE_IDENTIFIER_FIELD_NAME
from ..config import PERSISTENCE_DIR


def persist_json_result(target_path: str, content: dict) -> None:
    with open(target_path, "w") as f:
        json.dump(content, f)


def safe_load_json(path: str) -> Optional[dict]:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return None


def initialize_request_parser(
    include_resource_identifier: bool = True
) -> reqparse.RequestParser:
    parser = reqparse.RequestParser()
    parser.add_argument(
        LOGIN_FIELD_NAME,
        help='Field "login" must be specified in this request.',
        required=True
    )
    if include_resource_identifier:
        parser.add_argument(
            RESOURCE_IDENTIFIER_FIELD_NAME,
            help='Field "resource_identifier" must '
                 'be specified in this request.',
            required=True
        )
    return parser


def build_base_resource_path(
    requester_login: str,
    resource_identifier: str
) -> str:
    return os.path.join(
        PERSISTENCE_DIR, requester_login, resource_identifier
    )
