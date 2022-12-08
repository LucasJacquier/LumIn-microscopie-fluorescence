import numpy.typing as npt
import pandas as pd
import trackpy as tp


def detect_peaks(
    frames: npt.NDArray, diameter: int, minmass: float, percentile: float
) -> pd.DataFrame:
    """Detect the peaks.

    Args:
        frames (npt.NDArray): shape (n_frames, height, width)
        diameter (int): This may be a single number or a tuple giving the
            feature's extent in each dimension, useful when the dimensions do
            not have equal resolution (e.g. confocal microscopy). The tuple
            order is the same as the image shape, conventionally (z, y, x) or
            (y, x). The number(s) must be odd integers. When in doubt, round up.
        minmass (float): The minimum integrated brightness. This is a crucial
            parameter for eliminating spurious features. Recommended minimum
            values are 100 for integer images and 1 for float images.
        percentile (float): Features must have a peak brighter than pixels in
            this percentile. This helps eliminate spurious peaks.


    Returns:
        npt.NDArray: Dataframe with columns [x, y, mass, size, ecc, signal]
            where mass means total integrated brightness of the blob, size means
            the radius of gyration of its Gaussian-like profile, and ecc is its
            eccentricity (0 is circular).
    """
    out = tp.batch(
        frames=frames,
        diameter=diameter,
        minmass=minmass,
        percentile=percentile,
        preprocess=False,
    )
    return out
