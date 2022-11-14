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

![initial_image_print_with_plt](https://user-images.githubusercontent.com/113975558/201638553-98618c64-fb45-496e-ac58-5ae9aa413e7e.png)


## Detect particles

## Detection and elimination of the background

First, it is needed to calculate the background
```python
from background_estimation import all
#Je sais pas si je dois mettre l'import de numpy et pandas aussi

averaged_movie_img = calculate_local_average(movie_dict["R"], 10)

averaged_movie_img #One specific frame of movie_dict['color'], with averaged pixel value (here it is the frame 10 from the red movie)
```
Example on an averaged image
![calculate_local_average_Print_with_plt](https://user-images.githubusercontent.com/113975558/201638778-6a66a395-6484-4a4a-a1d6-a8d8faed9c18.png)

Then, it is possible to eliminate the background
The first method is a substraction
```python
background_substracted_img = background_elimination_substract(movie_dict["R"][10], averaged_movie_img)
background_substracted_img # Specific frame with the background elimination method applied to it(here : frame 10, red movie)
```
Example of an background eliminated image
![background_elimination_substract_print_with_plt](https://user-images.githubusercontent.com/113975558/201640395-a759ec38-6f9f-4eef-acff-f3c5cf299eed.png)
