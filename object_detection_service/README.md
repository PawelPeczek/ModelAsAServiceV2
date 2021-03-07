# Model as a Service - object detection service

## Environment build
To build object detection service simply run:
```bash
repo_root/object_detection_service$ docker build -t maas/v2/object_detection_service . 
```

## Service run
To run the service one should simply
```bash
repo_root/object_detection_service$ docker run --network host -v $PWD:/project maas/v2/object_detection_service:latest
```

## Communication schema
Communication should be implemented via REST.

Request:
```
Method: POST
Port: 50001
Path: /maas_workshop/v2/object_detection/detect
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
