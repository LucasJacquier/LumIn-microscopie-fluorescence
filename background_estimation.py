import numpy as np
import pandas as pd

##Background estimation

def calculate_local_average(film : np.ndarray, nbr_frame : int) -> np.ndarray:
    '''

    Args :
        film (np.ndarray): the fluorescent microscopy film with only one color.
        nbr_frame (int): the index of the frame to average. Must be inferior at the number of frame from the film.

        Returns :
        new_film (np.ndarray) : the film with the square average normalization.
    '''
    film_shape = np.shape(film)
    new_film = np.empty((film_shape[1], film_shape[2]))
    for x in range(film_shape[1]):
        for y in range (film_shape[2]):
            if x < 3 or x >= film_shape[1]-3 or y < 3 or y >= film_shape[2]-3 :
                new_film[x,y] = film [nbr_frame,x,y]
            elif 3 <= x < film_shape[1]-3 and 2 <= y < film_shape[2]-3:
                avg_list = []
                for k in range(x-3, x+4):
                    for l in range(y-3, y+4):
                        avg_list.append(film[nbr_frame,k,l])
                average_value = np.mean([avg_list])
                new_film[x,y] = average_value
    return new_film
