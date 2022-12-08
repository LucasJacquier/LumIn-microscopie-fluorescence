#path = 'C:/Users/lucas/Documents/sciences/Mes Recherches/2022_09 ARIA 1er Stage/Films/A6_0831_8RRL.tif'
#path = 'C:/Users/lucas/Documents/Science_ENS/matériel stage ARIA/A6_0831_8RRL.tif'

import numpy as np
import pandas as pd
import random as rd

##Creation du dataframe

film = load_data('C:/Users/lucas/Documents/sciences/Mes Recherches/2022_09 ARIA 1er Stage/Films/A6_0831_8RRL.tif', '[RG]')
red_movie = film['R']
peak_position = detect_peaks(red_movie, 5, 0.1, 60)

##Liste de points candidats à la frame 1

candidate_list = pd.DataFrame(columns=['y', 'x', 'mass', 'size', 'ecc', 'signal', 'raw_mass', 'ep', 'frame', 'peak_index'], index=range(0)) #Creation du dataframe vide qui acceuillera les points candidats des frames suivantes
for position in range(np.shape(peak_position[ peak_position["frame"] == 0 ])[0]):
#position = rd.randint (0, 2551) # Ok pour 0, 1159. 2 candidats pour 2243, 167

    point_A = peak_position[ peak_position["frame"] == 0 ].iloc[position]
    x_A = peak_position[ peak_position["frame"] == 0 ].iloc[position]['x']
    y_A = peak_position[ peak_position["frame"] == 0 ].iloc[position]['y']

    peak_position_1 = peak_position[ peak_position["frame"] == 1 ]
    selected_x = peak_position_1[peak_position_1['x'] > x_A - int_x_value]
    selected_x = selected_x[selected_x ['x'] < (x_A+int_x_value)]

    selected_y = peak_position_1[peak_position_1['y'] > y_A - int_y_value]
    selected_y = selected_y[selected_y ['y'] < (y_A+int_y_value)]
    intersect = pd.merge (selected_y, selected_x) #Liste de tous les points candidats
    if np.shape(intersect)[0] == 0:
        data = {'y': ['NaN'],
            'x': ['NaN'],
            'mass': ['NaN'],
            'size': ['NaN'],
            'ecc': ['NaN'],
            'signal': ['NaN'],
            'raw_mass': ['NaN'],
            'ep': ['NaN'],
            'frame': ['NaN'],
            'peak_index' : [position]}
        candidate = pd.DataFrame(data)

    if np.shape(intersect)[0] == 1:
        candidate = intersect
        candidate['peak_index'] = [position]

    if np.shape(intersect)[0] >= 2:
        distance_list = []
        for i in range(np.shape(intersect)[0]):
            x_candidate = intersect.iloc[i]['x']
            y_candidate = intersect.iloc[i]['x']
            distance_list.append((x_candidate - x_A)**2 + (y_candidate - y_A)**2)
        candidate_index = distance_list.index(min(distance_list)) #Distance comparison between the peak and the candidates
        candidate = intersect.iloc[candidate_index].to_frame().transpose()
        candidate['peak_index'] = [position]

    candidate_list = pd.concat ([candidate_list, candidate])
print (candidate_list)
#On obtient un data frame qui contient toutes les infos des points candidats de la frame 1 correspondant aux points de la frame 0. Il y a de plus une colonne correspondant au numéro du peak de la frame 1. Mtn on peut étirer ça sur toutes les frames suivantes.


##Plan de l'algorithme à réaliser
# Sélection d'un point A de la frame n
# Enregistrement de ses paramètres, notamment x_A et y_A
# Sélection des points dans l'intervalle : [ x_A - int_x ; x_A + int_x] appartenant aux frames : n< frame < n+m
# WARNING : est ce que int_x représente un intervalle de valeurs ou le nombre de points. A voir.
# (m à définir : soit de manière itérative, soit dans toutes les frames)
# Parmi l'intervalle précédent, sélection du point au y le plus proche : obtention du point candidat B
# Test du point candidat B (je sais pas encore comment faire ça)
# Validation du point B
# Suppression de la ligne du point B dans le dataframe
# Selection du point suivant de la frame n
# etc.

##Manipulation du dataframe

peak_position['x']
peak_position[ peak_position["frame"] == 0 ]
peak_position[ peak_position["frame"] == 0 ].iloc[0]

pp_sorted_0 = peak_position[peak_position["frame"] == 0].sort_values(by="x", ascending=False)
pp_sorted_1 = peak_position[peak_position["frame"] == 1].sort_values(by="x", ascending=False)

frame_number = np.shape(red_movie)[0]
img_width = np.shape(red_movie)[1]
img_height = np.shape(red_movie)[2]

int_x_number = np.shape(peak_position[peak_position["frame"] == 0])[0] / 100 #Proposition de garder 1% des points les plus proches, ici ca nous en fait 25
int_x_value = 5 #Il doit y avoir un moyen d'avoir un codage un peu plus fin de ce paramètre. Demander à Karen de combien elle estime le mouvement des particules. Avec un intervalle sur x, j'obtiens dans cet exemple 55 candidats.
int_y_value = 5


