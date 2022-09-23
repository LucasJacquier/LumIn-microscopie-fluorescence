# LumIn-microscopie-fluorescence 

## Installation

The packages to install can be found in `requirements.txt`.

## Load data

```python
from load_data import load_data

filepath = ...  # path to the .tiff or .tif file

# red_film and green_film are of shape (n_frames, n_rows, n_columns).
red_film, green_film = load_data(filepath)
```

## Detect particles
