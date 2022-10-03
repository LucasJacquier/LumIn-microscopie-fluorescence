#fonction qui prend une image et ressort les points

##Fonction percentile
import numpy as np


def remove_outliers (film):
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

def normalize (film):
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










