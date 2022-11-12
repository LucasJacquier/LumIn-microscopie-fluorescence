# LumIn-microscopie-fluorescence 

## Installation

The packages to install can be found in `requirements.txt`.

## Load data

```python
from pathlib import Path
from load_data import load_data

filepath = Path(...)  # path to the .tiff or .tif file
color_sequence = ["R", "G"]  # [R frame, G frame, R frame,...] (with "R" for red and "G" for green)

# red_film and green_film are of shape (n_frames, n_rows, n_columns).
movie_dict = load_data(filepath)

movie_dict["R"]  # array of shape (n_red_frames, n_rows, n_cols)
movie_dict["G"]  # array of shape (n_green_frames, n_rows, n_cols)

# display a frame
frame = movie_dict["G"][10]
plt.imshow(frame, cmap="gray")
plt.show()
```
Example of a frame
(from our data : EMCV1_0524_1RRL, red, 10th frame)
# Changer l'image en dessous afin d'être homogène
![Figure_1](https://user-images.githubusercontent.com/113975558/192475178-1bc63813-b195-4fec-9e22-214abcd8baa6.png)


## Detect particles

## Detection and elimination of the background

'''python
from background_estimation import all
#Je sais pas si je dois mettre l'import de numpy et pandas aussi

averaged_movie_dict = calculate_local_average(movie_dict["G"], 10)

averaged_movie_dict # One specific frame (here, for the example it is the 10th) of movie_dict['color'] (here, for the example it is the green one), with averaged pixel value
'''
Produire l'img qui va là
