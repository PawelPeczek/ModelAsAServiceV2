# Resource manager service

## Service build
To build face detection service simply run:
```bash
repo_root/gateway_service$ docker build -t maas/v2/gateway_service .
```

## Service run
To run the service one should simply
```bash
repo_root/gateway_service$ docker run --network host -v $PWD:/project maas/v2/gateway_service:latest
```

## Communication schema
Communication should be implemented via REST.

### Object detection
Request:
```
Method: POST
Port: 50000
Path: /maas_workshop/v2/gateway/detect_objects
Body: (form-data)
    "image": bytes of jpeg image
```

Response:
```json
{
  "detected_objects": [
    {
      "bbox": {
        "left_top": [0, 0],
        "right_bottom": [100, 100]
      },
      "confidence": 0.87,
      "label": 1,
      "class_name": "person"
    }
  ]
}
```

### Face detection - initialize job
Request:
```
Method: POST
Port: 50000
Path: /maas_workshop/v2/gateway/detect_faces
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


### Face detection - fetch results
Request:
```
Method: GET
Path: /maas_workshop/v2/gateway/detect_faces
Body: (form-data)
    "login" user login (str)
    "resource_identifier" uuid (str)
```
Response:
```json
{
    "inference_results": [{
      "bounding_box": {
        "left_top": [0, 0],
        "right_bottom": [100, 100]
      },
      "confidence": 0.78,
      "landmarks": [[0, 0], [100, 100]]
    }]
}
```