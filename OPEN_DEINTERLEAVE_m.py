"""
Title: OPEN_&_DEINTERLEAVE FUNCTIONS
Date: Sept 20 2022
Authors: Lucas Jacquier & Karen Perronet
"""

### Moduls to import
import imageio as io
import cv2
import numpy as np
import matplotlib.pyplot as plt
import time as time

### Functions

def load_tif_image(file_name: [str, 'you need to specify the work directory first']) -> np.ndarray:
    """this fonction take the name of a tiff image and return the image as an array. The file needs to be in tiff format: file_name = 'name.tif' """
    # open video as array
    video = io.volread(file_name)
    return video.astype(float)

#I wish to import and open the tiff image in python but I did not achieved
#I tried with this :
# > from PIL import Image
# > im = Image.open('EMCV1_0524_1RRL.tif')
# > im.show()
# But I obtained a black image
#Do you know an other method ?


def image_separation(image : [np.ndarray, 'this is an array of stacked images']) -> [np.ndarray, 'two different arrays with stacked images']:
    '''it takes a film as parameter and split it in two different films from even-numbered images and from odd-numbered images'''
    Nbframes = image.shape[0]
    Nbrows = image.shape[1]
    Nbcolumns = image.shape[2]
    Nbf = int(Nbframes / 2)
    red_image = np.zeros([Nbf, Nbrows, Nbcolumns])
    green_image = np.zeros([Nbf, Nbrows, Nbcolumns])
    for k in range(Nbf):
        red_image[k, :, :] = image[2 * k, :, :]
        green_image[k, :, :] = image[2 * k + 1, :, :]
    return red_image, green_image

# Maybe we can modify this fonction giving him the code (here RG) to generalize. For example, if we have a RRG film

# I think it is what this function does
#STOP READING HERE
def real_stack_separation(stack, temporal_sequence: str) -> np.ndarray:
    nb_frames = stack.shape[0]
    nb_rows = stack.shape[1]
    nb_columns = stack.shape[2]

    if len(temporal_sequence)==2:
        nb_f = int(nb_frames / 2)
        print('2 color stack')
        red_stack = np.zeros([nb_f, nb_rows, nb_columns])
        green_stack = np.zeros([nb_f, nb_rows, nb_columns])
        if temporal_sequence=='RG':
            for k in range(nb_f):
                red_stack[k, :, :] = stack[2 * k, :, :]
                green_stack[k, :, :] = stack[2 * k + 1, :, :]
        if temporal_sequence=='GR':
             for k in range(nb_f):
                red_stack[k, :, :] = stack[2 * k + 1, :, :]
                green_stack[k, :, :] = stack[2 * k, :, :]

    if (len(temporal_sequence) > 2):
        print('stack with ' + str(len(temporal_sequence)) + ' images par cycle')
        nb_images_per_cycle = len(temporal_sequence)
        nb_cycles = int(nb_frames / nb_images_per_cycle)
        nb_red_images_per_cycle = 0
        nb_green_images_per_cycle = 0
        for i in range(nb_images_per_cycle):
            if temporal_sequence[i]=='R':
                nb_red_images_per_cycle = nb_red_images_per_cycle + 1
            else:
                nb_green_images_per_cycle = nb_green_images_per_cycle + 1
        nb_f_R = int(nb_frames / nb_images_per_cycle * nb_red_images_per_cycle)
        nb_f_G = int(nb_frames / nb_images_per_cycle * nb_green_images_per_cycle)
        red_stack = np.zeros([nb_f_R, nb_rows, nb_columns])
        green_stack = np.zeros([nb_f_G, nb_rows, nb_columns])
        k=0
        for k in range (nb_cycles):
            i=0
            i_R=0
            i_G=0
            for i in range (nb_images_per_cycle):
                if temporal_sequence[i]=='R':
                    red_stack[k * nb_red_images_per_cycle + i_R, :, :] = \
                        stack[k * nb_images_per_cycle + i, :, :]
                    i_R = i_R + 1
                else:
                    green_stack[k * nb_green_images_per_cycle + i_G, :, :] = \
                        stack[k * nb_green_images_per_cycle + i, :, :]
                    i_G = i_G + 1

    return red_stack, green_stack


def RRL_arrival(file_name: str, temporal_sequence: str):
    stack_tot = load_tif_image(file_name)
    red_stack, green_stack = real_stack_separation(stack_tot, temporal_sequence)
    BkgR = np.zeros(shape = (red_stack.shape[0]))
    BkgG = np.zeros(shape = (green_stack.shape[0]))
    i = 0
    for i in range (red_stack.shape[0]):
        BkgR[i] = (red_stack[i, :, :]).mean()
    i = 0
    for i in range (green_stack.shape[0]):
        BkgG[i] = (green_stack[i, :, :]).mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(BkgR, 'r')
    ax.set_xlim(0, 15)
    plt.show()
        #plt.ylim((0, 0.4))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(BkgG, "*-", alpha=0.5)
    ax.set_xlim(0, 20)
    plt.show()

    print("Determination of the RRL arrival time")
    #R_RRL_arrival_image = int(input("Enter the red image number at which RRL has arrived : "))
    #G_RRL_arrival_image = int(input("Enter the green image number at which RRL has arrived : "))
    #last_red_image_before_RRL = BkgR.index(min(BkgR))
    #last_green_image_before_RRL = BkgG.index(min(BkgG))
    return stack_tot #, last_red_image_before_RRL, last_green_image_before_RRL


def MakeSubstack(stack, first_image, last_image):
#warning: first stack image is 0. Thus, last stack image is stack.shape[0]-1.
    substack = stack
    if(last_image < stack.shape[0] - 1):
        i = 0
        for i in range (stack.shape[0] - 1 - last_image):
            substack = np.delete(substack, stack.shape[0] - 1 - i, axis = 0)

    if(first_image > 0):
        i = 0
        for i in range (first_image):
            substack = np.delete(substack, 0, axis = 0)

    return substack

def Make_Cheat_Stack(stack, t_RRL, nb_added_first_image):
    '''from the initial stack: remove images before the last image with no RRL
    and add 3 times the first image so that ruptures can find particles that disappear after less than 3 images.'''
    last_image_nb = stack.shape[0]-1
    image_width = stack.shape[1]
    image_height = stack.shape[2]
    cheat_stack = MakeSubstack(stack,t_RRL,last_image_nb)
    first_image = stack[t_RRL]
    add_images = np.zeros((nb_added_first_image, image_width, image_height))
    for i in range(nb_added_first_image):
       add_images[i, :, :] = first_image
    cheat_stack = np.concatenate((add_images, cheat_stack), axis = 0)
    return cheat_stack

###Deleted parts
##First bloc

#matplotlib.rcParams['text.usetex'] = True

#colors = {'PINK': '#590b3d', 'BLUE': '#2a1e60', 'pink': '#b9529f', 'lblue': '#78e1f9', 'green': '#6abd45',
#          'lgreen': '#a9d8b4', 'gray': '#bfbfbf'}


#class HiddenPrints:
#    # hides print statements temporarily
#    def __enter__(self):
#        self._original_stdout = sys.stdout
#        sys.stdout = open(os.devnull, 'w')
#
#    def __exit__(self, exc_type, exc_val, exc_tb):
#        sys.stdout.close()
#        sys.stdout = self._original_stdout

##Second bloc

# def open_npy_image(file_name):
#    # concatenate image name
#    file_name = file_name + '.npy'
#
#    # open image as numpy array
#    image = np.load(file_name)
#
#    # change array type to float64
#    image = np.float64(image)
#    return image


#def open_csv_image(file_name):
#    # concatenate image name
#    file_name = file_name + '.csv'
#
#    # open image as pandas dataframe
#    image = pd.read_csv(file_name, sep='\t')
#    return image
