# Resource manager service

## Service build
To build face detection service simply run:
```bash
repo_root/resources_manager_service$ docker build -t maas/v2/resource_manager_service .
```

## Service run
To run the service one should simply
```bash
repo_root/resources_manager_service$ docker run --network host -v $PWD:/project maas/v2/resource_manager_service:latest
```

## Communication schema
Communication should be implemented via REST.

### Input image registration
Request:
```
Method: POST
Port: 50002
Path: /maas_workshop/v2/resources_manager/input_image_register
Body: (form-data)
    "image": bytes of jpeg image
    "login" user login (str)
```
Response:
```json
{
    "login": "requester_login",
    "resource_identifier": "uuid"
}
```

### Input image fetching
Request:
```
Method: GET
Port: 50002
Path: /maas_workshop/v2/resources_manager/input_image_register
Body: (form-data)
    "resource_identifier": uuid (str)
    "login" user login (str)
```
Response:
```
Bytes - jpeg image
```

### Face detection result registration
Request:
```
Method: POST
Port: 50002
Path: /maas_workshop/v2/resources_manager/face_detection_register
Body: (form-data)
    "resource_identifier": uuid (str)
    "login" user login (str)
    "face_detection_results" json of format returned by face detection service as text
```
Response:
```json
{
  "msg": "OK"
}
```

### Face detection result fetching
Request:
```
Method: GET
Port: 50002
Path: /maas_workshop/v2/resources_manager/face_detection_register
Body: (form-data)
    "resource_identifier": uuid (str)
    "login" user login (str)
```
Response:
```json
{
    "inference_results": [
        {
            "bounding_box": {
                "left_top": [0, 0],
                "right_bottom": [100, 100]
            },
            "confidence": 0.78,
            "landmarks": [
                [0, 0], [10, 10]
            ]
        }
    ]
}
```