from typing import Optional

import numexpr as ne
import numpy as np
import numpy.typing as npt


def normalize(frame: npt.NDArray, keep_percentile: Optional[float]=99)->npt.NDArray:
    """Remove outliers and normalize to [0,1]"""
    high = np.percentile(a=frame, q=keep_percentile)
    low = frame.min()
    out = ne.evaluate("where(frame<high, (frame - low) / (high - low), 1)")
    return out