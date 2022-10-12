#%%
#import numpy as np
#import pandas as pd
import trackpy as tp
#import skimage
#import os
#from scipy.signal import find_peaks
import sys
import warnings

#from tifffile import imsave

#import OPEN_DEINTERLEAVE as OD

#from link_particules import link_particles
#from tracking import optical_flow_intensity

##I don t know what this function does
if not sys.warnoptions: #Create an empty list
    warnings.simplefilter("ignore") # which warnings ?
    #Insert a simple entry into the list of warnings filters (at the front)
'Je pense que cela veut dire que s il y a une erreur le sytème doit l ignorer, mais je comprends pas trop ni comment ni ou cela agit'
##

def link_particles(
    stack: np.ndarray,
    particle_diameter: int = 5,
    min_mass = 0.1,
    pixel_range = 3,
    n_memory_frames = 10)-> (pd.DataFrame, pd.DataFrame):
    """Link particules.

    Args:
        video ([type]): the preprocessed video with the different filters BTWT       
        particle_diameter (int, odd): maximum diameter of spot to be located, in pixels. Odd value just above the diffraction limit. Need to see how to optimise this value.
        min_mass (float, optional): minimum mass (average intensity) of spot. Default value = 0.1. Need to see how to optimise this value.
        pixel_range (int, optional): search range (maximum displacement of the spot between 2 frames) in pixels. Need optimize.
        n_memory_frames (int, optional): maximum number of frames during which the particle can disappear, reappear and be considered as the same particle. Need optimize.
    """
    
    
    # particle detection using trackpy. 
    """the tp.batch function of trackpy detects the particles of a given particle_diameter and which mass is above the min_mass in all frames of the video"""
    located_particles = tp.batch(
        stack, diameter = particle_diameter, minmass = min_mass, percentile=60, engine='numba'
    ) #We can also try to optimize the percentile. The features must have a peak brighter than pixels in this percentile.
    
    # particle linking using trackpy
    """The tp.link function of trackpy takes in input the dataframe located_particles given by tp.batch and associates the particles 
    located in one frame to the one located in the other frames by using the criteria of the 
    pixel_range and the n_memory_frames. At this point, each particle, followed along the movie will have its own label.
    """
    linked_particles = tp.link_df(
        located_particles, pixel_range, memory = n_memory_frames
    )

    return linked_particles
    
def link_particles_on_2_first_frames(
    stack: np.ndarray,
    particle_diameter: int = 5,
    min_mass = 0.1,
    pixel_range = 3,
    n_memory_frames = 0)-> (pd.DataFrame, pd.DataFrame):
    """Link particules.

    Args:
        video ([type]): the preprocessed video with the different filters BTWT       
        particle_diameter (int, odd): maximum diameter of spot to be located, in pixels. Odd value just above the diffraction limit. 
        min_mass (float, optional): minimum mass (average intensity) of spot. Default value = 0.1.      
        pixel_range (int, optional): search range (maximum displacement of the spot between 2 frames) in pixels.        
        n_memory_frames (int, optional): maximum number of frames during which the particle can disappear, reappear and be considered
        as the same particle.
    """
    
    
    # particle detection using trackpy. 
    """the tp.batch function of trackpy detects the particles of a given particle_diameter and which mass is above the min_mass in all 
    frames of the video"""
    located_particles = tp.batch(
        stack, diameter = particle_diameter, minmass = min_mass, percentile=60, engine='numba'
    )
    
    # particle linking using trackpy
    """The tp.link function of trackpy takes in input the dataframe located_particles given by tp.batch and associates the particles 
    located in one frame to the one located in the other frames by using the criteria of the 
    pixel_range and the n_memory_frames. At this point, each particle, followed along the movie will have its own label.
    """
    linked_particles_0 = tp.link_df(located_particles, pixel_range, memory = n_memory_frames)

    linked_particles = linked_particles_0[linked_particles_0.frame == 0]
    n_detected_particles = max(linked_particles.particle) + 1
    linked_particles = pd.DataFrame()
    for i in range(n_detected_particles):
        t = linked_particles_0[linked_particles_0.particle == i]
        if (len(t)==2):
            df = t[t.frame == 0]
            linked_particles = pd.concat([linked_particles, df], ignore_index = True)

    return linked_particles
    
# def tracking_particles(filename_red, filename_green,t_init_RRL):

      
#     video_preprocessed_red =OD.load_tif_image('video_preprocessed_'+filename_red +'.tif')
#     video_preprocessed_green =OD.load_tif_image('video_preprocessed_'+filename_green +'.tif')
    

#     particle_diameter= 5
#     min_mass=0.15
#     pixel_range=3
#     n_memory_frames=0
    
#     linked_particles_red = link_particles(video_preprocessed_red[t_init_RRL[0]:t_init_RRL[0]+1], particle_diameter, min_mass, pixel_range, n_memory_frames)
        
#     linked_particles_green = link_particles(video_preprocessed_green[t_init_RRL[1]:t_init_RRL[1]+1], particle_diameter, min_mass, pixel_range, n_memory_frames)
    


#     '''we are only tracking particles present at the frame 0 in the full movie'''
    
#     particle_radius=3
    
#     followed_particles_red = optical_flow_intensity(
#          linked_particles_red, video_preprocessed_red, particle_radius, t_init_RRL[0]
#      )
    
#     followed_particles_green = optical_flow_intensity(
#          linked_particles_green, video_preprocessed_green, particle_radius,t_init_RRL[1]
#      )


#     ima=followed_particles_red[followed_particles_red.frame==0]
#     imb=followed_particles_green[followed_particles_green.frame==0]

#     print('red_particles:', len(ima))
#     print('green_particles:', len(imb))
    
#     followed_particles_green.to_csv('followed_particles_' + filename_green.split('.')[0] +'.csv')
#     followed_particles_red.to_csv('followed_particles_'+ filename_red.split('.')[0] +'.csv')


def compute_intensity(
    image, position_x: float, position_y: float, particule_diameter: int
) -> float:
    '''function which permits to clculate the intensity in a position( xp, yp)'''
    neighbourhood_size = (particule_diameter - 1) // 2
    position_x_int = int(position_x)
    position_y_int = int(position_y)
    nb_rows, nb_columns = image.shape
    if (
        position_y_int >= neighbourhood_size
        and position_y_int <= nb_rows - neighbourhood_size - 1
        and position_x_int >= neighbourhood_size
        and position_x_int <= nb_columns - neighbourhood_size - 1
    ):
        intensity_value = (
            sum(
                sum(
                    image[
                        position_y_int - neighbourhood_size : position_y_int + neighbourhood_size + 1,
                        position_x_int - neighbourhood_size : position_x_int + neighbourhood_size + 1,
                    ]
                )
            )
            / particule_diameter ** 2
        )
    else:
        intensity_value = 1.0
    return intensity_value




def optical_flow(linked_particles, n_frames) -> pd.DataFrame:
    '''For each particle found at the frame 0, we create a subdataframe containing
    the same columns as linked_particles with a n_frames number of rows .
     Then we concatene all the subdataframes in order to obtain a dataframe of size
     n_frames*nB of particles (frame0) rows . It a dataframe for initialization because we copy n_frames 
     times the subdataframe dor the nB particles'''
     
    particules_on_first_frame = linked_particles[linked_particles.frame == 0]
    

    for item, row in particules_on_first_frame.iterrows():
        a=item
        particules_on_first_frame.loc[item, "particle"] = a

    
    particules_on_first_frame.drop(
        ["mass", "size", "raw_mass", "ep", "ecc"], axis=1, inplace=True
    )
    fol_part1 = particules_on_first_frame.copy()
    fol_part2 = particules_on_first_frame.copy()

    for f in range(n_frames):
        if f > 0:
            fol_part2.frame = fol_part1.frame + f
            particules_on_first_frame = pd.concat(
                [particules_on_first_frame, fol_part2], ignore_index=True
            )
    return particules_on_first_frame


def optical_flow_intensity(linked_particles, video, particule_diameter) -> pd.DataFrame:
    ''' here we calculate the intensity value and put that on the column signal '''
    n_frames = video.shape[0]
    particules_on_first_frame = optical_flow(linked_particles, n_frames)

    for row in particules_on_first_frame.itertuples():

        intensity_value = compute_intensity(video[row.frame], row.x, row.y, particule_diameter)

        particules_on_first_frame.at[row.Index, "signal"] = intensity_value

    return particules_on_first_frame


def optical_flow_intensity_cheat(followed_part):
    '''add 3 times the intensity value on virtual -1, -2 and -3 frames 
    so that ruptures can detect particles lasting only 1 image'''

    t1 = followed_part[followed_part.frame == 0]
    i=0
    for i in range(len(t1['y'])):
        t1.loc[i, 'frame'] = -1
    t2 = followed_part[followed_part.frame == 0]
    i=0
    for i in range(len(t2['y'])):
      t2.loc[i, 'frame'] = -2
    t3 = followed_part[followed_part.frame == 0]
    i=0
    for i in range(len(t3['y'])):
        t3.loc[i, 'frame'] = -3
    df_ttot = pd.concat([t3, t2, t1], ignore_index = True)
    cheat_followed_part = pd.concat([df_ttot, followed_part], ignore_index = True)

    return cheat_followed_part

#%%
cell_name = 'EMCV2_0531_1TpR'
experiment_path = '/Users/karen/Desktop/20220531/'
filename = experiment_path + cell_name + '.tif'
experiment_results_folder = experiment_path + 'results'
results_folder = experiment_path + 'results/' + cell_name
save_path = results_folder + '/'

stack_tot = OD.load_tif_image(filename)
R_BTWT_stack = OD.load_tif_image(save_path + 'R_BTWT_' + cell_name + '.tif')
G_BTWT_stack = OD.load_tif_image(save_path + 'G_BTWT_' + cell_name + '.tif')

#%%
# stack =  R_BTWT_stack
# particle_diameter = 5
# min_mass = 0.1
# pixel_range = 3
# n_memory_frames = 0
# #%%
# located_particles = tp.batch(
#         stack[0:2], diameter = particle_diameter, minmass = min_mass, percentile=60, engine='numba'
#     )

# #linked_particles_0 = tp.link_df(located_particles, pixel_range, memory = n_memory_frames)
# #print(linked_particles_0)
# #linked_particles = linked_particles_0[linked_particles_0.frame == 0]
# #print(linked_particles)
# #%%
# n_detected_particles = max(linked_particles.particle) + 1
# #print(n_detected_particles)
# #%%
# linked_particles = pd.DataFrame()
# for i in range(n_detected_particles):
#     t = linked_particles_0[linked_particles_0.particle == i]
#     if (len(t)==2):
#         df = t[t.frame == 0]
#         linked_particles = pd.concat([linked_particles, df], ignore_index = True)

# #print(linked_particles)
# image = stack[0]

# x1 = linked_particles['x'].to_numpy()
# y1 = linked_particles['y'].to_numpy()
# print(len(x1))

# #plt.imshow(noisy_image)
# #plt.show()
# #%%
# plt.imshow(image)
# plt.ylim(350,250)
# plt.xlim(250,350)
# plt.scatter(x1, y1, s = 20, facecolors = 'none', edgecolors = 'r')
# plt.show()