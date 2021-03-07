# Model as a Service - face detection service

## Service build
To build face detection service simply run:
```bash
repo_root/face_detection_service$ docker build -t maas/v2/face_detection_service .
```

## Service run
To run the service one should simply
```bash
repo_root/face_detection_service$ docker run --network host -v $PWD:/project maas/v2/face_detection_service:latest
```

## Communication schema
```
RabbitMQ message:
    Queue name: face_detection_channel
    Messages format: serialized json
    {
        "login": "user_login",
        "resource_identifier": "uuid"
    }
```
Data provided in message can be used to fetch image from resource manager service.
Desired outcome:
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
which describe face detection results. The json file should be posted to 
resource manager service.
