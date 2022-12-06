##Creation du dataframe

film = load_data(
    "C:/Users/lucas/Documents/Science_ENS/matériel stage ARIA/A6_0831_8RRL.tif", "[RG]"
)
red_movie = film["R"]
peak_position = detect_peaks(red_movie, 5, 0.1, 60)

##Manipulation du dataframe

peak_position["x"]
peak_position[peak_position["frame"] == 0]
peak_position[peak_position["frame"] == 0].iloc[0]

pp_sorted_0 = peak_position[peak_position["frame"] == 0].sort_values(
    by="x", ascending=False
)
pp_sorted_1 = peak_position[peak_position["frame"] == 1].sort_values(
    by="x", ascending=False
)

frame_number = np.shape(red_movie)[0]
img_width = np.shape(red_movie)[1]
img_height = np.shape(red_movie)[2]

point_A = peak_position[peak_position["frame"] == 0].iloc[0]
x_A = peak_position[peak_position["frame"] == 0].iloc[0]["x"]
y_A = peak_position[peak_position["frame"] == 0].iloc[0]["y"]
int_x_number = (
    np.shape(peak_position[peak_position["frame"] == 0])[0] / 100
)  # Proposition de garder 1% des points les plus proches, ici ca nous en fait 25
int_x_value = 5  # Il doit y avoir un moyen d'avoir un codage un peu plus fin de ce paramètre. Demander à Karen de combien elle estime le mouvement des particules. En sélectionnant la frame suivante, on obtient 10 points.
int_y_value = 5

# selected_x = peak_position[peak_position["x"] > (x_A-int_x_value) & peak_position["x"] < (x_A+int_x_value)]
# Ne marche pas, j'ai obtenu cette erreur :
# TypeError: Cannot perform 'rand_' with a dtyped [float64] array and scalar of type [bool]
peak_position_1 = peak_position[peak_position["frame"] == 1]
selected_x = peak_position_1[peak_position_1["x"] > x_A - int_x_value]
selected_x = selected_x[selected_x["x"] < (x_A + int_x_value)]

selected_y = peak_position_1[peak_position_1["y"] > y_A - int_y_value]
selected_y = selected_y[selected_y["y"] < (y_A + int_y_value)]


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
