from typing import Union, List

import numpy as np
import cv2 as cv
import torch


def image_from_str(raw_image: str) -> np.ndarray:
    data = np.fromstring(raw_image, dtype=np.uint8)
    return cv.imdecode(data, cv.IMREAD_COLOR)


def to_chw_tensor(x: Union[np.ndarray, List[np.ndarray]]) -> torch.Tensor:
    if type(x) is not list:
        x = [x]
    return torch.Tensor([e.transpose(2, 0, 1).copy() for e in x])
