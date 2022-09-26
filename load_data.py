from pathlib import Path
from typing import Dict, List, Union

import imageio.v3 as iio


def load_data(filepath: Union[Path, str], color_sequence: List[str]) -> Dict:
    """Return the deinterlaced films contained in the file.

    The original file is a .tiff or .tif film where frames are interlaced, e.g.
    `[red_frame, green_frame, red_frame, green_frame,...]`.
    The order of the colors is given in `color_sequence`. For instance, if
    `color_sequence=["red", "green"]` then the ouput is a dictionary:
    `{"red": red_frames_array, "green": green_frames_array}`.

    Args:
        filepath (Union[Path, str]): path to the film (e.g.
            "c:\\users\\john\\documents\\project\\film.tif")
        color_sequence (List[str]): initials of the laser's colors

    Returns:
        Dict: dictionary {"color": numpy array}
    """
    video = iio.imread(filepath).astype(float)
    n_colors = len(color_sequence)
    res_dict = {
        color: video[k_color::n_colors]
        for (k_color, color) in enumerate(color_sequence)
    }
    return res_dict
