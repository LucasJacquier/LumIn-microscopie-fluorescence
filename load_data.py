"""
Title: OPEN_&_DEINTERLEAVE FUNCTIONS
Date: Sept 20 2022
Authors: Lucas Jacquier & Charles Truong & Karen Perronet
"""

### Moduls to import
import imageio as io
import numpy as np

from pathlib import Path
from typing import Tuple

###Principal function
def load_separate_data(filepath: Path, temporal_sequence: str)-> Tuple[np.ndarray, np.ndarray]:
    """Return the red and green films.add(). Print the number of images by cycle.

    Each film is a ndarray of shape (n_frames, n_rows, n_columns)

    Args:
        filepath (Path): path to the .tiff film (Example : 'c:\\users\\john\\documents\\project\\film.tif')
        temporal_sequence (str) : initials of the laser's colors

    Returns:
        tuple[numpy.ndarray, numpy.ndarray]: (red_film, green_film)
    """
    initial_image = load_tif_image(filepath)
    return real_stack_separation (initial_image, temporal_sequence)


###Preliminary Functions
def load_tif_image(file_name: str) -> np.ndarray:
    """Takes the name of an image and returns the image as an numpy.ndarray.

    Args:
        filepath (Path): path to the .tiff film (Example : 'c:\\users\\john\\documents\\project\\film.tif')

    Returns:
        numpy.ndarray : the loaded image
    """
    # open video as array
    video = io.volread(file_name)
    return video.astype(float)

#I wish to import and open the tiff image in python but I did not achieved
#I tried with this :
# > from PIL import Image
# > im = Image.open('EMCV1_0524_1RRL.tif')
# > im.show()
# But I obtained a black image
#Do you know an other method ?


def real_stack_separation(image : np.ndarray, temporal_sequence: str) -> tuple [np.ndarray, np.ndarray]:
    """Return the films separated by colors, red and green. Print the number of images by cycle.

    Each film is a ndarray of shape (n_frames, n_rows, n_columns)

    Args:
        image (numpy.ndarray) : loaded image
        temporal sequence (str) : initials of the laser's colors

    Returns:
        tuple [numpy.ndarray, numpy.ndarray]: (red_film, green_film)
    """
    #Collecting the size
    nb_frames = image.shape[0]
    nb_rows = image.shape[1]
    nb_columns = image.shape[2]
    nb_images_per_cycle = len(temporal_sequence)
    print ('stack with ' + str(nb_images_per_cycle) + ' images per cycle')
    #2 colors
    if nb_images_per_cycle == 2:
        nb_f = int(nb_frames / 2)
        red_stack = np.zeros([nb_f, nb_rows, nb_columns])
        green_stack = np.zeros([nb_f, nb_rows, nb_columns])
        if temporal_sequence == 'RG': #If it start with the R img
            for k in range(nb_f):
                red_stack[k, :, :] = image[2 * k, :, :]
                green_stack[k, :, :] = image[2 * k + 1, :, :]
        if temporal_sequence == 'GR':#If it start with the G img
             for k in range(nb_f):
                red_stack[k, :, :] = image[2 * k + 1, :, :]
                green_stack[k, :, :] = image[2 * k, :, :]
    #More than 2 colors
    if nb_images_per_cycle > 2:
        nb_cycles = int(nb_frames / nb_images_per_cycle)
        nb_red_images_per_cycle = 0
        nb_green_images_per_cycle = 0
        for i in range(nb_images_per_cycle): #Counts the colors
            if temporal_sequence[i] == 'R':
                nb_red_images_per_cycle += 1
            else:
                nb_green_images_per_cycle += 1
        #Count the frames by color
        nb_f_R = int(nb_frames / nb_images_per_cycle * nb_red_images_per_cycle)
        nb_f_G = int(nb_frames - nb_f_R)
        #Create the empty arrays
        red_stack = np.zeros([nb_f_R, nb_rows, nb_columns])
        green_stack = np.zeros([nb_f_G, nb_rows, nb_columns])
        # Writing in theses arrays
        # Each image of each cycle is loaded in color_stack
        # I THINK THIS PART CAN BE SIMPLIFIED
        for k in range (nb_cycles):
            i_R=0 # turns into zero at each time it restarts
            i_G=0
            for i in range (nb_images_per_cycle):
                if temporal_sequence[i] == 'R':
                    red_stack[k * nb_red_images_per_cycle + i_R, :, :] = image[k * nb_images_per_cycle + i, :, :]
                    i_R = i_R + 1 # To add the next image of this color
                else:
                    green_stack[k * nb_green_images_per_cycle + i_G, :, :] = image[k * nb_green_images_per_cycle + i, :, :]
                    i_G = i_G + 1

    return red_stack, green_stack
