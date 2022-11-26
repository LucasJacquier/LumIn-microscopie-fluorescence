import pandas as pd
import trackpy as tp
import numpy.typing as npt


def detect_peaks(
    frames: npt.NDArray, diameter: int, minmass: float, percentile: float
) -> pd.DataFrame:
    """Detect the peaks.

    Args:
        frames (npt.NDArray): shape (n_frames, height, width)
        diameter (int): This may be a single number or a tuple giving the
            feature's extent in each dimension, useful when the dimensions do
            not have equal resolution (e.g. confocal microscopy). The tuple
            order is the same as the image shape, conventionally (z, y, x) or
            (y, x). The number(s) must be odd integers. When in doubt, round up.
        minmass (float): The minimum integrated brightness. This is a crucial
            parameter for eliminating spurious features. Recommended minimum
            values are 100 for integer images and 1 for float images.
        percentile (float): Features must have a peak brighter than pixels in
            this percentile. This helps eliminate spurious peaks.


    Returns:
        npt.NDArray: Dataframe with columns [x, y, mass, size, ecc, signal]
            where mass means total integrated brightness of the blob, size means
            the radius of gyration of its Gaussian-like profile, and ecc is its
            eccentricity (0 is circular).
    """
    out = tp.batch(
        frames=frames,
        diameter=diameter,
        minmass=minmass,
        percentile=percentile,
        preprocess=False,
    )
    return out


# def image_peak_save_show (path : Union[Path, str], color_sequence : List[str], selection : Union[str, int], batch_parameters : list, saving_path : Union[Path, str]):
#     '''Create an image with the detected particles marked with a red dot and save it in a predefined folder. The detection parameters can be modified selecting the batch parameters.
#     Args :

#     path (Union[Path, str]): path to the film (e.g. "c:\\users\\john\\documents\\project\\film.tif")
#     color_sequence (List[str]): colors of the frames, in the correct order.
#     selection (List[str, int] = [selected_color, selected_frame]) : the color and the frame selected from the film
#     batch_parameters (List[str] = [diameter, minmass, percentile]): the parameters of the tracky.batch function to find the particles
#     saving_path : path to the file where to save the images

#     Returns :

#         None

#     '''
#     film_one_color = load_data(path, color_sequence) [selection[0]] #Film loading

#     array_spot_R = tp.batch(film_one_color, diameter = batch_parameters[0], minmass = batch_parameters[1], percentile = batch_parameters[2]) #Peak extraction

#     ordinate_image_spot, abscissa_image_spot = (
#     array_spot_R[array_spot_R['frame'] == selection[1]]['y'],
#     array_spot_R[array_spot_R['frame'] == selection[1]]['x'])
#     length = len(ordinate_image_spot)
#     int_coordinate = [(int(ordinate_image_spot[i]), int(abscissa_image_spot[i])) for i in range(length)] #Establishment of integers peak coordinates

#     modified_image = Image.new('RGB',(film_shape[1],film_shape[2])) #Creation of a new image

#     for x in range(film_shape[1]):
#         for y in range(film_shape[2]):
#             color = int(film_rouge[0,x,y])
#             if (x,y) in int_coordinate:
#                 int_coordinate.remove((x,y))
#                 modified_image.putpixel((x,y), (255, 0, 0))
#             else:
#                 modified_image.putpixel((x,y), (color, color, color))
#             origin_image.putpixel((x,y), (color, color, color)) #Painting of the image with the red dots


#     name_modif = str(path[re.search('Films/', path).span()[1] : -4] + '_' + str(batch_parameters) + '_R0_detectedpeaks') #Name of the new file

#     modified_image.save(r'C:\Users\lucas\Documents\sciences\Mes Recherches\2022_09 ARIA 1er Stage\Images\img_auto(2022_10_21)\ ' + name_modif + '.png') #Saving of the new image


# ##Complete function

# def image_peak_save_show_complete (path : Union[Path, str], color_sequence : List[str], frame_selection : int, batch_parameters : list, saving_path : Union[Path, str]):
#     '''Create an image with the detected particles marked with a red dot and save it in a predefined folder.  It also can show et save the graph of the number of detected peaks according to the frame. It is the complete version of the image_peak_save_show function. The detection parameters can be modified selecting the batch parameters.
#     Args :

#     path (Union[Path, str]): path to the film (e.g. "c:\\users\\john\\documents\\project\\film.tif")
#     color_sequence (List[str]): colors of the frames, in the correct order.
#     frame_selection (int) : the frame selected from the film
#     batch_parameters (List[str]) = [diameter, minmass, percentile]): the parameters of the tracky.batch function to find the particles
#     saving_path : path to the file where to save the images

#     Returns :

#         None

#     '''

#     film_rouge, film_vert = (
#         load_data(path, color_sequence) [color_sequence[0]],
#         load_data(path, color_sequence) [color_sequence[1]]) #chargement du film

#     array_spot_R, array_spot_G = (
#         tp.batch(film_rouge, diameter = batch_parameters[0], minmass = batch_parameters[1], percentile = batch_parameters[2]),
#         tp.batch(film_vert, diameter = batch_parameters[0], minmass = batch_parameters[1], percentile = batch_parameters[2])) #extraction des points lumineux

#     # film_shape = np.shape(film_rouge)
#     # graph_choice = input('Voulez-vous voir les graphes de l evolution du nombre de spots (y pour oui et n pour non)?')
#     # if graph_choice == 'y':
#     #     list_number_spot_R, list_number_spot_G = (
#     #         [len(array_spot_R[array_spot_R['frame'] == i])for i in range(film_shape[0])],
#     #         [len(array_spot_G[array_spot_G['frame'] == i])for i in range(film_shape[0])])
#     #
#     #     plt.plot(list_number_spot_R, 'r')
#     # green_choice = input ('Voulez-vous voir le graphe vert (y pour oui et n pour non)?')
#     # if green_choice == 'y':
#     #     plt.plot(list_number_spot_G, 'g')
#     #     plt.title('Evolution du nombre de spot dans les deux films')
#     #     plt.show()
#     # else:
#     #     plt.title('Evolution du nombre de spot dans le film rouge')
#     #     plt.show()

#     ordinate_image_spot, abscissa_image_spot = (
#     array_spot_R[array_spot_R['frame'] == frame_selection]['y'],
#     array_spot_R[array_spot_R['frame'] == frame_selection]['x'])
#     length = len(ordinate_image_spot)
#     int_coordinate = [(int(ordinate_image_spot[i]), int(abscissa_image_spot[i])) for i in range(length)] #Establishment of integers peak coordinates

#     modified_image = Image.new('RGB',(film_shape[1],film_shape[2])) #Creation of the red dots image
#     origin_image = Image.new('RGB',(film_shape[1],film_shape[2])) #Creation of the original image
#     for x in range(film_shape[1]):
#         for y in range(film_shape[2]):
#             color = int(film_rouge[0,x,y])
#             if (x,y) in int_coordinate:
#                 int_coordinate.remove((x,y))
#                 modified_image.putpixel((x,y), (255, 0, 0))
#             else:
#                 modified_image.putpixel((x,y), (color, color, color))
#             origin_image.putpixel((x,y), (color, color, color)) #Painting of the two images

#     modified_image.show()
#     origin_image.show() #Showing the images
#     name_modif = str(path[re.search('Films/', path).span()[1] : -4] + '_' + str(batch_parameters) + '_R0_detectedpeaks')
#     name_origin = str(path[re.search('Films/', path).span()[1] : -4] + '_' + str(batch_parameters) + '_R0_initialimage')
#     modified_image.save(r'C:\Users\lucas\Documents\sciences\Mes Recherches\2022_09 ARIA 1er Stage\Images\img_auto\ ' + name_modif + '.png')
#     origin_image.save(r'C:\Users\lucas\Documents\sciences\Mes Recherches\2022_09 ARIA 1er Stage\Images\img_auto\ ' + name_origin + '.png') #Saving of the images with the specified path


# ##Automatic launch of the simplified function
# list_diameter = [5,7,9]
# list_minmass = [0.01*i for i in range(11,17)]
# list_percentile = [75+1*i for i in range(0,15)] #Range values realization

# # path = (e.g. "c:\\users\\john\\documents\\project\\film.tif") #Assign the path value

# for diam in range(len(list_diameter)):
#     for mm in range(len(list_minmass)):
#         for pe in range(len(list_percentile)):
#             bp = [list_diameter[diam], list_minmass[mm], list_percentile[pe]]
#             image_peak_save_show (path, 'RG', bp) # loops of calls
