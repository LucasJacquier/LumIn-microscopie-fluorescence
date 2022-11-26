import cv2 as cv
import numpy.typing as npt
from typing import Optional


def remove_background(
    image: npt.NDArray,
    kernel_size: Optional[int] = 101,
    sigma: Optional[float] = None
) -> npt.NDArray:
    if sigma is None:
        sigma = 0.3*((kernel_size-1)*0.5 - 1) + 0.8
    background = cv.GaussianBlur(
        src=image, ksize=(kernel_size, kernel_size), sigmaX=sigma
    )
    out = image - background
    return out