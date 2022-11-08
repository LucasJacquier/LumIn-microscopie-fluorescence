#%%
import numpy as np
import os
import pandas as pd

import OPEN_DEINTERLEAVE as OD


def calculate_background_and_noise_around_the_particle(followed_part, BTWT_stack):
    #for each followed particle, return the local background and noise calculated 
    # in a 50x50 pixels around the particle (except on the edges of the image)
    followed_part_noise = pd.DataFrame()
    followed_part_noise = followed_part
    followed_part_noise['noise'] = 0
    followed_part_noise['background'] = 0
    nb_of_images = BTWT_stack.shape[0]
    image_width = BTWT_stack.shape[1]
    image_height = BTWT_stack.shape[2]

    nb_followed_particles = max(followed_part.particle)
    for i in range(nb_followed_particles):
        t = followed_part[followed_part.particle == i]
        u = t.index.values.astype(int)[0]
        jmin = max(0, (int(followed_part.loc[u, 'x']) - 24))
        kmin = max(0, (int(followed_part.loc[u, 'y']) - 24))
        jmax = min(image_width, (int(followed_part.loc[u, 'x']) + 24))
        kmax = min(image_height, (int(followed_part.loc[u, 'y']) + 24))
        #print(jmin, jmax, kmin, kmax)
        #print(int(followed_part.loc[u, 'x']), int(followed_part.loc[u, 'y']))
        substack = BTWT_stack[0 : nb_of_images, jmin : jmax, kmin : kmax]
        followed_part_noise.loc[u, 'background'] = np.mean(substack)
        followed_part_noise.loc[u, 'noise'] = np.std(substack)
        #print(followed_part_noise)
        
        #seuil = np.mean(stack) + 0.5 * np.std(stack)
        #for j in range(jmin, jmax, 1):
    return followed_part_noise

#%%
cell = 'EMCV1_0524_6RRLh'
path = '/Users/karen/Desktop/20220524/'

filename = path + cell + '.tif'
results_folder = path + 'results/' + cell
save_path = results_folder + '/'

followed_part = pd.read_csv(save_path + 'red_followed_part.csv')
R_BTWT_stack = OD.load_tif_image(save_path + 'R_BTWT_' + cell + '.tif')
#%%
followed_part_noise = pd.DataFrame()
followed_part_noise = followed_part
followed_part_noise['noise'] = 0
followed_part_noise['background'] = 0
nb_of_images = R_BTWT_stack.shape[0]
print(nb_of_images)
image_width = R_BTWT_stack.shape[1]
print(image_width)
image_height = R_BTWT_stack.shape[2]
print(image_height)
#%%
nb_followed_particles = max(followed_part.particle) + 1
print(nb_followed_particles)
followed_part.tail(10)
#%%
for i in range(nb_followed_particles):
        t = followed_part[followed_part.particle == i]
        u = t.index.values.astype(int)[0]
        print(t.loc[u])
        jmin = max(0, (int(followed_part.loc[u, 'x']) - 24))
        kmin = max(0, (int(followed_part.loc[u, 'y']) - 24))
        jmax = min(image_width, (int(followed_part.loc[u, 'x']) + 24))
        kmax = min(image_height, (int(followed_part.loc[u, 'y']) + 24))
        print(jmin, jmax, kmin, kmax)
        #print(int(followed_part.loc[u, 'x']), int(followed_part.loc[u, 'y']))
        substack = R_BTWT_stack[0 : nb_of_images, jmin : jmax, kmin : kmax]
        followed_part_noise.loc[u, 'background'] = np.mean(substack)
        print(np.mean(substack))
        followed_part_noise.loc[u, 'noise'] = np.std(substack)
        print(followed_part_noise.loc[u])
#%%
print(followed_part)
# #%%
# followed_part_noise = calculate_background_and_noise_around_the_particle(followed_part, R_BTWT_stack)