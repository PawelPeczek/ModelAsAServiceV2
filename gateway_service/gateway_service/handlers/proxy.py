import requests
from flask import request, Response, make_response
from flask_restful import Resource


class Proxy(Resource):

    def __init__(self):
        super().__init__()
        self.__excluded_headers = [
            'content-encoding', 'content-length',
            'transfer-encoding', 'connection'
        ]

    def _forward_message(self, target_url: str) -> Response:
        headers = {
            key: value for (key, value) in request.headers if key != 'Host'
        }
        try:
            resp = requests.request(
                method=request.method,
                url=target_url,
                headers=headers,
                data=request.get_data(),
                allow_redirects=False,
                verify=False
            )
        except Exception:
            return make_response({'msg': 'Internal error'}, 500)
        headers = [
            (name, value) for (name, value) in resp.raw.headers.items()
            if name.lower() not in self.__excluded_headers
        ]
        response = Response(resp.content, resp.status_code, headers)
        return response
