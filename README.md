# LumIn-microscopie-fluorescence 

## Installation

The packages to install can be found in `requirements.txt`.

## Load data

```python
from pathlib import Path
from load_data import load_data

filepath = Path(...)  # path to the .tiff or .tif file
color_sequence = ["red", "green"]  # [red frame, green frame, red frame,...]

# red_film and green_film are of shape (n_frames, n_rows, n_columns).
movie_dict = load_data(filepath)

movie_dict["red"]  # array of shape (n_red_frames, n_rows, n_cols)
movie_dict["green"]  # array of shape (n_green_frames, n_rows, n_cols)

# display a frame
frame = movie_dict["red"][10]
plt.imshow(frame, cmap="gray")
plt.show()
```
TODO: Add image of a frame or two.

## Detect particles
