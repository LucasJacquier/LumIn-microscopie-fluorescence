##Test tp.batch
import numpy as np
import pandas as pd
import trackpy as tp
import matplotlib.pyplot as plt

#path = 'write the path of the film'
#path = 'C:/Users/lucas/Documents/sciences/Mes Recherches/2022_09 ARIA 1er Stage/Films/EMCV1_0524_1RRL.tif'
path = 'C:/Users/lucas/Documents/Science_ENS/matériel stage ARIA/A6_0831_8RRL.tif'
color_sequence = 'RG'

film_rouge = load_data (path, color_sequence) ['R'] #chargement du film
film_vert = load_data (path, color_sequence) ['G']

array_spot_R = tp.batch(film_rouge, diameter = 3, minmass = 0.1, percentile = 60) #extraction des points lumineux
array_spot_G = tp.batch(film_vert, diameter = 3, minmass = 0.1, percentile = 60)

##Realisation du graphe

list_number_spot_R = [len(array_spot_R[array_spot_R['frame'] == i])for i in range(100)] #nombre de spots en fonction de l'index de l'image
list_number_spot_G = [len(array_spot_G[array_spot_G['frame'] == i])for i in range(100)]

plt.plot(list_number_spot_G)
plt.show()

## Exemple de detection de pics sans debruitage
from PIL import Image

ordinate_image1_spot_R = array_spot_R[array_spot_R['frame'] == 1]['y']
abscissa_image1_spot_R = array_spot_R[array_spot_R['frame'] == 1]['x']

coordinate = [(ordinate_image1_spot_R[i], abscissa_image1_spot_R[i]) for i in range(6196,12346)]

modified_image = Image.new('RGB',(512,512))
origin_image = Image.new('RGB',(512,512))
int_coordinate = [(int(coordinate[i][0]), int(coordinate[i][1])) for i in range(6150)]
for x in range(512):
    for y in range(512):
            if (x,y) in int_coordinate:
                int_coordinate.remove((x,y))
                modified_image.putpixel((x,y), (255, 0, 0))
            else:
                color = int(film_rouge[1,x,y])
                modified_image.putpixel((x,y), (color, color, color))
            color = int(film_rouge[1,x,y])
            origin_image.putpixel((x,y), (color, color, color))
modified_image.show()
origin_image.show()



