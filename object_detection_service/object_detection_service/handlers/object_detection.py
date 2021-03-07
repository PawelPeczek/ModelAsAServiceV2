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
            return make_response({'msg': 'Field named "image" required.'}, 400)
        image = image_from_str(raw_image=request.files['image'].read())
        raise NotImplementedError()

    def __infer_from_image(
        self,
        image: np.ndarray
    ) -> DetectedObjects:
        raise NotImplementedError()

    def __standardize_image(
        self,
        image: np.ndarray
    ) -> Tuple[torch.Tensor, float]:
        raise NotImplementedError()

    def __post_process_inference(
        self,
        prediction: RawPrediction,
        scale: float
    ) -> DetectedObjects:
        raise NotImplementedError()

