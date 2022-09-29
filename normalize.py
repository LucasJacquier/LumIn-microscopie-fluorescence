#fonction qui prend une image et ressort les points

##Fonction percentile
import numpy as np


def remove_outliers (film):
    new_max = np.percentile(film, 0.99)
    dimension = np.shape(film)
    for k in range(dimension[0]):
        for l in range(dimension[1]):
            for m in range(dimension[2]):
                if film[k,l,m] > new_max:
                    film[k,l,m] = new_max
    return np.amax(film)






