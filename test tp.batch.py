##Test tp.batch
import numpy as np
import pandas as pd
import trackpy as tp
import matplotlib.pyplot as plt

#path = 'write the path of the film'
path = 'C:/Users/lucas/Documents/sciences/Mes Recherches/2022_09 ARIA 1er Stage/Films/EMCV1_0524_1RRL.tif'
color_sequence = 'RG'

film_rouge = load_data (path, color_sequence) ['R'] #chargement du film
film_vert = load_data (path, color_sequence) ['G']

array_spot_R = tp.batch(film_rouge, diameter = 3, minmass = 0.1, percentile = 60) #extraction des points lumineux
array_spot_G = tp.batch(film_vert, diameter = 3, minmass = 0.1, percentile = 60)

list_number_spot_R = [len(array_spot_R[array_spot_R['frame'] == i])for i in range(100)] #nombre de spots en fonction de l'index de l'image
list_number_spot_G = [len(array_spot_G[array_spot_G['frame'] == i])for i in range(100)]

plt.plot(list_number_spot_G)
plt.show()

