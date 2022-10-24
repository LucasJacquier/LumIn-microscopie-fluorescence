list_diameter = [5,7,9]
list_minmass = [0.01*i for i in range(11,17)]
list_percentile = [75+1*i for i in range(0,15)]
path = 'C:/Users/lucas/Documents/sciences/Mes Recherches/2022_09 ARIA 1er Stage/Films/EMCV1_0524_1RRL.tif'

for diam in range(len(list_diameter)):
    for mm in range(len(list_minmass)):
        for pe in range(len(list_percentile)):
            bp = [list_diameter[diam], list_minmass[mm], list_percentile[pe]]
            image_peak_save_show (path, 'RG', bp)

#[3,0.1,60]