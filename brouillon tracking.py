##

import pandas as pd
import trackpy as tp
import numpy.typing as npt
import matplotlib.pyplot as plt
##


film = load_data('C:/Users/lucas/Documents/sciences/Mes Recherches/2022_09 ARIA 1er Stage/Films/EMCV1_0524_1RRL.tif', 'RG')
red_movie = film['R']
tp.quiet()
peak_position = detect_peaks(red_movie, 5, 0.1, 60)


tp.quiet()
t = tp.link(peak_position, 5, memory=5)
print(t)
print(t['particle'].max())

t_1 = tp.filter_stubs(t, 10)
print(t_1)
print(t_1['particle'].max())

print(len(t_1)/len(t))

plt.figure()
tp.mass_size(t.groupby('particle').mean())

plt.figure()
tp.mass_size(t_1.groupby('particle').mean())

plt.figure()
tp.mass_ecc(t.groupby('particle').mean())

plt.figure()
tp.mass_ecc(t_1.groupby('particle').mean())

plt.figure()
tp.plot_traj(t_1)

t_1_reduced_3 = t_1[t_1['particle']%3 == 0]
plt.figure()
tp.plot_traj(t_1_reduced_3)

t_1_reduced_5 = t_1[t_1['particle']%5 == 0]
plt.figure()
tp.plot_traj(t_1_reduced_5)