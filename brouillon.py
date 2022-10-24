##Comparaison des coordonées des points sur les premières images

liste_positions_0 = array_spot_R[array_spot_R['frame'] == 0]
liste_positions_1 = array_spot_R[array_spot_R['frame'] == 1]
coordonees0 = [(liste_positions_0['x'][i], liste_positions_0['y'][i]) for i in range(0,len(liste_positions_0))]
