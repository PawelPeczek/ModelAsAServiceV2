import logging
from typing import Tuple

import torch
from flask import Response, request, make_response
from flask_restful import Resource
import numpy as np
import cv2 as cv
from torchvision.models.detection.retinanet import RetinaNet

from ..config import \
    CLASS_MAPPING
from ..entities import \
    DetectedObjects, BoundingBox, DetectedObject
from ..utils import \
    image_from_str, to_chw_tensor

STANDARDIZATION_CONST = 255.0

RawPrediction = dict


logging.getLogger().setLevel(logging.INFO)


class ObjectDetection(Resource):

    def __init__(
        self,
        model: RetinaNet,
        confidence_threshold: float,
        max_image_dim: int
    ):
        self.__model = model
        self.__confidence_threshold = confidence_threshold
        self.__max_image_dim = max_image_dim

    def post(self) -> Response:
        if 'image' not in request.files:
            return make_response({'msg': 'Field named "image" required.'}, 500)
        image = image_from_str(raw_image=request.files['image'].read())
        results = self.__infer_from_image(image=image)
        return make_response(results.to_dict(), 200)

    def __infer_from_image(
        self,
        image: np.ndarray
    ) -> DetectedObjects:
        image, scale = self.__standardize_image(image=image)
        logging.info(f"Standardized image shape: {image.shape}. scale: {scale}")
        prediction = self.__model(image)[0]
        return self.__post_process_inference(prediction=prediction, scale=scale)

    def __standardize_image(
        self,
        image: np.ndarray
    ) -> Tuple[torch.Tensor, float]:
        max_shape = max(image.shape[:2])
        if max_shape <= self.__max_image_dim:
            return to_chw_tensor(image / STANDARDIZATION_CONST), 1.0
        scale = self.__max_image_dim / max_shape
        resized_image = cv.resize(image, dsize=None, fx=scale, fy=scale)
        return to_chw_tensor(resized_image / STANDARDIZATION_CONST), scale

    def __post_process_inference(
        self,
        prediction: RawPrediction,
        scale: float
    ) -> DetectedObjects:
        boxes, scores, labels = \
            prediction["boxes"].detach().numpy() / scale, \
            prediction["scores"].detach().numpy(), \
            prediction["labels"].detach().numpy()
        detected_objects = []
        for bbox, score, label in zip(boxes, scores, labels):
            if score < self.__confidence_threshold:
                continue
            bbox = BoundingBox(
                left_top=(int(round(bbox[0])), int(round(bbox[1]))),
                right_bottom=(int(round(bbox[2])), int(round(bbox[3])))
            )
            detected_object = DetectedObject(
                bbox=bbox,
                confidence=score.astype(float).item(),
                label=label.item(),
                class_name=CLASS_MAPPING.get(label, "N/A")
            )
            detected_objects.append(detected_object)
        return DetectedObjects(detected_objects=detected_objects)

