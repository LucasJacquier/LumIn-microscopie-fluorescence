##import
import numpy as np
import pandas as pd
import trackpy as tp
import matplotlib.pyplot as plt
import time
import re
from PIL import Image
from load_data import load_data

##Fonction simplifié


def image_peak_save_show (path, color_sequence, batch_parameters):
    '''batch_parameters = [diameter, minmass, percentile]'''
    film_rouge = load_data(path, color_sequence) ['R'] #chargement du film

    array_spot_R = tp.batch(film_rouge, diameter = batch_parameters[0], minmass = batch_parameters[1], percentile = batch_parameters[2]) #extraction des points lumineux

    ordinate_image0_spot, abscissa_image0_spot = (
    array_spot_R[array_spot_R['frame'] == 0]['y'],
    array_spot_R[array_spot_R['frame'] == 0]['x'])

    length = len(ordinate_image0_spot)

    coordinate = [(ordinate_image0_spot[i], abscissa_image0_spot[i]) for i in range(0,length)]

    modified_image = Image.new('RGB',(film_shape[1],film_shape[2]))
    int_coordinate = [(int(coordinate[i][0]), int(coordinate[i][1])) for i in range(length)]
    for x in range(film_shape[1]):
        for y in range(film_shape[2]):
            color = int(film_rouge[0,x,y])
            if (x,y) in int_coordinate:
                int_coordinate.remove((x,y))
                modified_image.putpixel((x,y), (255, 0, 0))
            else:
                modified_image.putpixel((x,y), (color, color, color))
            origin_image.putpixel((x,y), (color, color, color))


    name_modif = str(path[re.search('Films/', path).span()[1] : -4] + '_' + str(batch_parameters) + '_R0_detectedpeaks')

    modified_image.save(r'C:\Users\lucas\Documents\sciences\Mes Recherches\2022_09 ARIA 1er Stage\Images\img_auto(2022_10_21)\ ' + name_modif + '.png')



##Fonction complète

def image_peak_save_show_complete (path, color_sequence, batch_parameters):
    '''batch_parameters = [diameter, minmass, percentile]'''
    film_rouge, film_vert = (
        load_data(path, color_sequence) ['R'],
        load_data(path, color_sequence) ['G'])
    #chargement du film

    array_spot_R, array_spot_G = (
        tp.batch(film_rouge, diameter = batch_parameters[0], minmass = batch_parameters[1], percentile = batch_parameters[2]),
        tp.batch(film_vert, diameter = batch_parameters[0], minmass = batch_parameters[1], percentile = batch_parameters[2]))
    #extraction des points lumineux

    # film_shape = np.shape(film_rouge)
    # graph_choice = input('Voulez-vous voir les graphes de l evolution du nombre de spots (y pour oui et n pour non)?')
    # if graph_choice == 'y':
    #     list_number_spot_R, list_number_spot_G = (
    #         [len(array_spot_R[array_spot_R['frame'] == i])for i in range(film_shape[0])],
    #         [len(array_spot_G[array_spot_G['frame'] == i])for i in range(film_shape[0])])
    #
    #     plt.plot(list_number_spot_R, 'r')
    # green_choice = input ('Voulez-vous voir le graphe vert (y pour oui et n pour non)?')
    # if green_choice == 'y':
    #     plt.plot(list_number_spot_G, 'g')
    #     plt.title('Evolution du nombre de spot dans les deux films')
    #     plt.show()
    # else:
    #     plt.title('Evolution du nombre de spot dans le film rouge')
    #     plt.show()

    ordinate_image0_spot, abscissa_image0_spot = (
    array_spot_R[array_spot_R['frame'] == 0]['y'],
    array_spot_R[array_spot_R['frame'] == 0]['x'])

    length = len(ordinate_image0_spot)

    coordinate = [(ordinate_image0_spot[i], abscissa_image0_spot[i]) for i in range(0,length)]

    modified_image = Image.new('RGB',(film_shape[1],film_shape[2]))
    #origin_image = Image.new('RGB',(film_shape[1],film_shape[2]))
    int_coordinate = [(int(coordinate[i][0]), int(coordinate[i][1])) for i in range(length)]
    for x in range(film_shape[1]):
        for y in range(film_shape[2]):
            color = int(film_rouge[0,x,y])
            if (x,y) in int_coordinate:
                int_coordinate.remove((x,y))
                modified_image.putpixel((x,y), (255, 0, 0))
            else:
                modified_image.putpixel((x,y), (color, color, color))
            origin_image.putpixel((x,y), (color, color, color))

    # modified_image.show()
    # origin_image.show()
    name_modif = str(path[re.search('Films/', path).span()[1] : -4] + '_' + str(batch_parameters) + '_R0_detectedpeaks')
    #name_origin = str(path[re.search('Films/', path).span()[1] : -4] + '_' + str(batch_parameters) + '_R0_initialimage')
    modified_image.save(r'C:\Users\lucas\Documents\sciences\Mes Recherches\2022_09 ARIA 1er Stage\Images\img_auto\ ' + name_modif + '.png')
    #origin_image.save(r'C:\Users\lucas\Documents\sciences\Mes Recherches\2022_09 ARIA 1er Stage\Images\img_auto\ ' + name_origin + '.png')

##Test tp.batch


#path = 'write the path of the film'
#path = 'C:/Users/lucas/Documents/sciences/Mes Recherches/2022_09 ARIA 1er Stage/Films/EMCV1_0524_1RRL.tif'
#path = 'C:/Users/lucas/Documents/Science_ENS/matériel stage ARIA/A6_0831_8RRL.tif'


## Exemple de detection de pics sans debruitage
from PIL import Image

ordinate_image0_spot, abscissa_image0_spot = (
array_spot_R[array_spot_R['frame'] == 0]['y'],
array_spot_R[array_spot_R['frame'] == 0]['x'])

length = len(ordinate_image0_spot)

coordinate = [(ordinate_image0_spot[i], abscissa_image0_spot[i]) for i in range(0,length)]

modified_image = Image.new('RGB',(film_shape[1],film_shape[2]))
origin_image = Image.new('RGB',(film_shape[1],film_shape[2]))
int_coordinate = [(int(coordinate[i][0]), int(coordinate[i][1])) for i in range(length)]
for x in range(film_shape[1]):
    for y in range(film_shape[2]):
        color = int(film_rouge[0,x,y])
        if (x,y) in int_coordinate:
            int_coordinate.remove((x,y))
            modified_image.putpixel((x,y), (255, 0, 0))
        else:
            modified_image.putpixel((x,y), (color, color, color))
        origin_image.putpixel((x,y), (color, color, color))
# modified_image.show()
# origin_image.show()




