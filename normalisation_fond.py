import numpy as np
# import os
import pandas as pd
#
# import OPEN_DEINTERLEAVE as OD


def calculate_local_average(film : np.ndarray) -> np.ndarray:
    '''Args:
        film (np.ndarray): the fluorescent microscopy film with only one color'''
    film_shape = np.shape(film)
    new_film = np.empty((film_shape[1], film_shape[2]))
    for x in range(film_shape[1]):
        for y in range (film_shape[2]):
            if x < 3 or x >= film_shape[1]-3 or y < 3 or y >= film_shape[2]-3 :
                new_film[x,y] = film [0,x,y]
            elif 3 <= x < film_shape[1]-3 and 2 <= y < film_shape[2]-3:
                avg_list = []
                for k in range(x-3, x+4):
                    for l in range(y-3, y+4):
                        avg_list.append(film[0,k,l])
                average_value = np.mean([avg_list])
                new_film[x,y] = average_value
    return new_film
