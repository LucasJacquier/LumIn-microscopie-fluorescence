##Creation du dataframe

film = load_data('C:/Users/lucas/Documents/Science_ENS/matériel stage ARIA/A6_0831_8RRL.tif', '[RG]')
red_movie = film['R']
peak_position = detect_peaks(red_movie, 5, 0.1, 60)

##Manipulation du dataframe

peak_position['x']
peak_position[ peak_position["frame"] == 0 ]
peak_position[ peak_position["frame"] == 0 ].iloc[0]

pp_sorted_0 = peak_position[peak_position["frame"] == 0].sort_values(by="x", ascending=False)
pp_sorted_1 = peak_position[peak_position["frame"] == 1].sort_values(by="x", ascending=False)

#Fonctionnement : je prends un point A de la frame n
#je save ses parametres, notamment x et y
#je cherche pour un intervalle (int_x) tous les points autour, appartenant aux frames : n< frame < n+m
#(m a definir : 1 ou toutes les frames)
#Je recherche dans un intervalle (int_y) le y le plus proche
#J obtiens un point candidat B
#Trouver une maniere de tester si B est le bon point
#Je valide que B est le bon point
#Je retire le point B du data frame
#Je passe au point suivant C de la frame n
# etc.