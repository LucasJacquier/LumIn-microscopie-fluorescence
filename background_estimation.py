import numpy as np
import pandas as pd

##Background estimation

def calculate_local_average(film : np.ndarray, nbr_frame : int) -> np.ndarray:
    '''Create a new image where each pixel from the frame is reimplaced by the average value of a 7x7 square centered on this pixel. Allow the background elimination at a next step.

    Args :
        film (np.ndarray): the fluorescent microscopy film with only one color.
        nbr_frame (int): the index of the frame to average. Must be inferior at the number of frame from the film.

        Returns :
        new_film (np.ndarray) : the film with the square average normalization.
    '''
    film_shape = np.shape(film)
    new_film = np.empty((film_shape[1], film_shape[2]))
    for x in range(film_shape[1]):
        for y in range (film_shape[2]):
            if x < 3 or x >= film_shape[1]-3 or y < 3 or y >= film_shape[2]-3 :
                new_film[x,y] = film [nbr_frame,x,y]
            elif 3 <= x < film_shape[1]-3 and 2 <= y < film_shape[2]-3:
                avg_list = []
                for k in range(x-3, x+4):
                    for l in range(y-3, y+4):
                        avg_list.append(film[nbr_frame,k,l])
                average_value = np.mean([avg_list])
                new_film[x,y] = average_value
    return new_film


## Different techniques of background estimation
import cv2 as cv
from skimage import restoration


img_init = load_data('C:/Users/lucas/Documents/sciences/Mes Recherches/2022_09 ARIA 1er Stage/Films/A6_0831_8RRL.tif', '[R,D]')['R'][10]
filter_size = int(input('Choose the size of the kernel filter size'))
kernel = np.ones((filter_size,filter_size),np.float32)/(filter_size**2)

#Cette fonction est efficace mais je sais pas trop les calculs qu'elle fait
dst = cv.filter2D(img_init, -1,kernel)
plt.imshow(dst, cmap= 'gray')
plt.show()

#Averaging convolution
blur = cv.blur(img_init,(filter_size, filter_size))
plt.imshow(blur, cmap = 'gray')
plt.show()

#Gaussian blurring with a type given kernel
blur = cv.GaussianBlur(img_init,(filter_size, filter_size),0)
plt.imshow(blur, cmap = 'gray')
plt.show()

#Gaussian blurring on the whole image
x_size_img = np.shape(img_init)[0]
if x_size_img % 2 == 0:
    x_size_img -= 1
blur = cv.GaussianBlur(img_init,(x_size_img,x_size_img),0)
plt.imshow(blur, cmap = 'gray')
plt.show()

#Median blurring
#Je comprends pas pourquoi cette fonction ne marche pas
img_int_init = np.ones((512,512), np.int32)
for i in range (np.shape(img_init)[0]):
    for k in range(np.shape(img_init)[1]):
        img_int_init[i,k] = int(img_init[i,k])

median = cv.medianBlur(img_int_init, np.ones((512,512), np.int32), 5)

#Rollingball
#Donne des résultats étranges mais forme de jolies images
background = restoration.rolling_ball(img_init, radius=filter_size)
plt.imshow(background, cmap = 'gray')
plt.show()

##Background substraction

def background_elimination_substract (initial_frame : np.ndarray, averaged_frame : np.ndarray) -> np.ndarray:
    '''Elimination backgroun function for one frame, with the background estimation from the calculate_local_average function.

    Args :
        initial_frame (np.ndarray) :  One frame from the fluorescent microscopy film with only one color.
        averaged_frame (np.ndarray) : The initial_frame averaged by square with the calculate_local_average function.

    Returns :
        np.ndarray : the initial frame corrected with a background elimination
    '''
    frame_shape = np.shape (initial_frame)
    for x in range(frame_shape[0]):
        for y in range(frame_shape[1]):
            initial_frame[x,y]-= averaged_frame[x,y]
        return initial_frame