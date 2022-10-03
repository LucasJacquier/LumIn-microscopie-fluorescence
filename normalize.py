

##Lissage des valeurs abberrantes et normalisation de 0 à 255
import numpy as np


def remove_outliers (film : numpy.ndarray) -> numpy.ndarray:
    """Return the film without its extremes values.

    Args:
        film (numpy.ndarray): the fluorescent microscopy film with only one color

    Returns:
        None : the film is modified by side effect
    """
    list_outliers = []
    for i in range(int(np.size(film)/(2*10**6))):
        new_max = np.amax(film)
        print(new_max)
        indice_new_max = np.where(film == new_max)
        film[indice_new_max] = 0
        list_outliers.append(indice_new_max)
    print(len(list_outliers))
    print(list_outliers)
    definitive_max = np.amax(film)
    for l in range(int(np.size(film)/(2*10**6))):
        film[list_outliers[l]] = definitive_max
    return None

def normalize (film : numpy.ndarray) -> numpy.ndarray:
    """Return the film with values in an interval of [0, 255]. It is recommended to use first the remove_outliers function.

    Args:
        film (numpy.ndarray): the fluorescent microscopy film with only one color

    Returns:
        None : the film is modified by side effect
    """
    old_extremes = [np.amin(film), np.amax(film)]
    new_extremes = [0,255]
    classe = (old_extremes[1] - old_extremes[0]) / 256
    dimension = np.shape(film)
    for k in range(dimension[0]):
        for l in range(dimension[1]):
            for m in range(dimension[2]):
                if (film[k,l,m]-old_extremes[0]) % classe == 0 :
                    film[k,l,m] = (film[k,l,m]-old_extremes[0])//classe - 1
                else :
                    film[k,l,m] = (film[k,l,m]-old_extremes[0])//classe
    return None










