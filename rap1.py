import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import funkcjetopt as ft
from pathlib import Path
from matplotlib.animation import FFMpegWriter, PillowWriter
import matplotlib.animation as animation
dane=ft.file_reading()  # This function reads the CSV files and prepares the data

#initializing sums of com_x and com_y for the whole dataset
com_x= {}
com_y = {}
time = {}  
T=[60,100,140]
Mfr=[0,305]
for t in T:
    for m in Mfr:
        # Exclude files with t=100 and mfr=0
        if not (t == 100 and m == 0):
            for i in range(4):
                com_x[f'{i+1}_4_sum_mfr_{m}_T{t}'] = 0
                com_y[f'{i+1}_4_sum_mfr_{m}_T{t}'] = 0

#print(com_x)
#print(com_y)

count=7 #how many files we have for each T and Mfr(is seven from the dataset)

for t in T:
    for m in Mfr:
        if not (t == 100 and m == 0):
            for i in range(4):
                dane[f'{i+1}_4_avg_mfr_{m}_T{t}'] = ft.analiza_csv(f'T{t}mfr{m}_0{i+1:01d}.csv')

for key in dane.keys(): #not really needed, but just to check if the keys are correct
    if 'mfr0' in key:
        for t in T:
            for m in Mfr:
                if f'mfr{m}_T{t}' in key:
                    for i in range(7):
                        time[f'{i+1}_4_avg_mfr_{m}_T{t}'] = dane[f'{i+1}_4_avg_mfr_{m}_T{t}'][key][5]
                        
                        com_x[f'{i+1}_4_avg_mfr_{m}_T{t}'] = dane[f'{i+1}_4_avg_mfr_{m}_T{t}'][key][3]
                        com_y[f'{i+1}_4_avg_mfr_{m}_T{t}'] = dane[f'{i+1}_4_avg_mfr_{m}_T{t}'][key][4]
                        max_time = np.max(time[f'{i+1}_4_avg_mfr_{m}_T{t}'])
                        min_time = np.min(time[f'{i+1}_4_avg_mfr_{m}_T{t}'])
                        time_1_4 = min_time + (max_time - min_time) / 4
                        time_2_4 = min_time + 2 * (max_time - min_time) / 4
                        time_3_4 = min_time + 3 * (max_time - min_time) / 4
                        time_4_4 = max_time  
                        # teraz szukam wartosci dla tych czasów
                        com_x_1_4 = com_x[np.abs(time - time_1_4).argmin()]
                        com_x_2_4 = com_x[np.abs(time - time_2_4).argmin()]
                        com_x_3_4 = com_x[np.abs(time - time_3_4).argmin()]
                        com_x_4_4 = com_x[np.abs(time - time_4_4).argmin()]
                        com_y_1_4 = com_y[np.abs(time - time_1_4).argmin()]
                        com_y_2_4 = com_y[np.abs(time - time_2_4).argmin()]
                        com_y_3_4 = com_y[np.abs(time - time_3_4).argmin()]
                        com_y_4_4 = com_y[np.abs(time - time_4_4).argmin()]
                        
                        # adding to the sums
                        com_x[f'1/4_sum_mfr_{m}_T{t}'] += com_x_1_4
                        com_x[f'2/4_sum_mfr_{m}_T{t}'] += com_x_2_4
                        com_x[f'3/4_sum_mfr_{m}_T{t}'] += com_x_3_4
                        com_x[f'4/4_sum_mfr_{m}_T{t}'] += com_x_4_4
                        
                        com_y[f'1/4_sum_mfr_{m}_T{t}'] += com_y_1_4
                        com_y[f'2/4_sum_mfr_{m}_T{t}'] += com_y_2_4
                        com_y[f'3/4_sum_mfr_{m}_T{t}'] += com_y_3_4
                        com_y[f'4/4_sum_mfr_{m}_T{t}'] += com_y_4_4

# Plot com_x and com_y vs time for each data set

all_times = []
all_com_x_mfr_0_T60 = []
all_com_y_mfr_0_T60 = []
all_com_x_mfr_305_T60 = []
all_com_y_mfr_305_T60 = []
all_com_x_mfr_305_T100 = []
all_com_y_mfr_305_T100 = []
all_com_x_mfr_0_T140 = []
all_com_y_mfr_0_T140 = []
all_com_x_mfr_305_T140 = []
all_com_y_mfr_305_T140 = []

# Add lists for area
all_area_mfr_0_T60 = []
all_area_mfr_305_T60 = []
all_area_mfr_305_T100 = []
all_area_mfr_0_T140 = []
all_area_mfr_305_T140 = []

for key in dane.keys():
    if 'mfr0' in key:
        if 'T60' in key:
            all_com_x_mfr_0_T60.append(dane[key][3])
            all_com_y_mfr_0_T60.append(dane[key][4])
            all_area_mfr_0_T60.append(dane[key][11])  # Changed area index to 11
        elif 'T100' in key: #there is no mfr0 for T100 but just in case
            all_com_x_mfr_0_T140.append(dane[key][3])
            all_com_y_mfr_0_T140.append(dane[key][4])
            all_area_mfr_0_T140.append(dane[key][11])  # Changed area index to 11
        if 'T140' in key:
            all_com_x_mfr_0_T140.append(dane[key][3])
            all_com_y_mfr_0_T140.append(dane[key][4])
            all_area_mfr_0_T140.append(dane[key][11])  # Changed area index to 11
        time_data = dane[key][5]
        com_x_data = dane[key][3]
        com_y_data = dane[key][4]
        all_times.append(time_data)
        all_com_x_mfr_305_T60.append(com_x_data)
        all_com_y_mfr_305_T60.append(com_y_data)
    if 'mfr305' in key:
        if 'T60' in key:
            all_com_x_mfr_305_T60.append(dane[key][3])
            all_com_y_mfr_305_T60.append(dane[key][4])
            all_area_mfr_305_T60.append(dane[key][11])  # Changed area index to 11
        elif 'T100' in key:
            all_com_x_mfr_305_T100.append(dane[key][3])
            all_com_y_mfr_305_T100.append(dane[key][4])
            all_area_mfr_305_T100.append(dane[key][11])  # Changed area index to 11
        elif 'T140' in key:
            all_com_x_mfr_305_T140.append(dane[key][3])
            all_com_y_mfr_305_T140.append(dane[key][4])
            all_area_mfr_305_T140.append(dane[key][11])  # Changed area index to 11
        time_data = dane[key][5]
        com_x_data = dane[key][3]
        com_y_data = dane[key][4]
        all_times.append(time_data)
        all_com_x_mfr_305_T60.append(com_x_data)
        all_com_y_mfr_305_T60.append(com_y_data)
min_length = min(len(t) for t in all_times)
common_time = all_times[0][:min_length] 

com_x_arrays_mfr_0_T60 = [arr[:min_length] for arr in all_com_x_mfr_0_T60]
com_y_arrays_mfr_0_T60 = [arr[:min_length] for arr in all_com_y_mfr_0_T60]
com_x_arrays_mfr_305_T60 = [arr[:min_length] for arr in all_com_x_mfr_305_T60]
com_y_arrays_mfr_305_T60 = [arr[:min_length] for arr in all_com_y_mfr_305_T60]
com_x_arrays_mfr_305_T100 = [arr[:min_length] for arr in all_com_x_mfr_305_T100]
com_y_arrays_mfr_305_T100 = [arr[:min_length] for arr in all_com_y_mfr_305_T100]
com_x_arrays_mfr_0_T140 = [arr[:min_length] for arr in all_com_x_mfr_0_T140]
com_y_arrays_mfr_0_T140 = [arr[:min_length] for arr in all_com_y_mfr_0_T140]
com_x_arrays_mfr_305_T140 = [arr[:min_length] for arr in all_com_x_mfr_305_T140]
com_y_arrays_mfr_305_T140 = [arr[:min_length] for arr in all_com_y_mfr_305_T140]

area_arrays_mfr_0_T60 = [arr[:min_length] for arr in all_area_mfr_0_T60]
area_arrays_mfr_305_T60 = [arr[:min_length] for arr in all_area_mfr_305_T60]
area_arrays_mfr_305_T100 = [arr[:min_length] for arr in all_area_mfr_305_T100]
area_arrays_mfr_0_T140 = [arr[:min_length] for arr in all_area_mfr_0_T140]
area_arrays_mfr_305_T140 = [arr[:min_length] for arr in all_area_mfr_305_T140]

# Define com_area_arrays_* variables for plotting function
com_area_arrays_mfr_0_T60 = area_arrays_mfr_0_T60
com_area_arrays_mfr_0_T140 = area_arrays_mfr_0_T140
com_area_arrays_mfr_305_T60 = area_arrays_mfr_305_T60
com_area_arrays_mfr_305_T100 = area_arrays_mfr_305_T100
com_area_arrays_mfr_305_T140 = area_arrays_mfr_305_T140

avg_com_x_arrays_mfr_0_T60= np.mean(com_x_arrays_mfr_0_T60, axis=0)
avg_com_y_arrays_mfr_0_T60 = np.mean(com_y_arrays_mfr_0_T60, axis=0)
avg_com_x_arrays_mfr_305_T60 = np.mean(com_x_arrays_mfr_305_T60, axis=0)
avg_com_y_arrays_mfr_305_T60 = np.mean(com_y_arrays_mfr_305_T60, axis=0)
avg_com_x_arrays_mfr_305_T100 = np.mean(com_x_arrays_mfr_305_T100, axis=0)
avg_com_y_arrays_mfr_305_T100 = np.mean(com_y_arrays_mfr_305_T100, axis=0)
avg_com_x_arrays_mfr_0_T140 = np.mean(com_x_arrays_mfr_0_T140, axis=0)
avg_com_y_arrays_mfr_0_T140 = np.mean(com_y_arrays_mfr_0_T140, axis=0)
avg_com_x_arrays_mfr_305_T140 = np.mean(com_x_arrays_mfr_305_T140, axis=0)
avg_com_y_arrays_mfr_305_T140 = np.mean(com_y_arrays_mfr_305_T140, axis=0)

avg_area_arrays_mfr_0_T60 = np.mean(area_arrays_mfr_0_T60, axis=0)
avg_area_arrays_mfr_305_T60 = np.mean(area_arrays_mfr_305_T60, axis=0)
avg_area_arrays_mfr_305_T100 = np.mean(area_arrays_mfr_305_T100, axis=0)
avg_area_arrays_mfr_0_T140 = np.mean(area_arrays_mfr_0_T140, axis=0)
avg_area_arrays_mfr_305_T140 = np.mean(area_arrays_mfr_305_T140, axis=0)    
# ... [previous code] ...

# Calculate min and max for each condition
min_com_x_mfr_0_T60 = np.min(com_x_arrays_mfr_0_T60, axis=0)
max_com_x_mfr_0_T60 = np.max(com_x_arrays_mfr_0_T60, axis=0)

min_com_x_mfr_0_T140 = np.min(com_x_arrays_mfr_0_T140, axis=0)
max_com_x_mfr_0_T140 = np.max(com_x_arrays_mfr_0_T140, axis=0)

min_com_x_mfr_305_T60 = np.min(com_x_arrays_mfr_305_T60, axis=0)
max_com_x_mfr_305_T60 = np.max(com_x_arrays_mfr_305_T60, axis=0)

min_com_x_mfr_305_T100 = np.min(com_x_arrays_mfr_305_T100, axis=0)
max_com_x_mfr_305_T100 = np.max(com_x_arrays_mfr_305_T100, axis=0)

min_com_x_mfr_305_T140 = np.min(com_x_arrays_mfr_305_T140, axis=0)
max_com_x_mfr_305_T140 = np.max(com_x_arrays_mfr_305_T140, axis=0)

min_area_mfr_0_T60 = np.min(area_arrays_mfr_0_T60, axis=0)
max_area_mfr_0_T60 = np.max(area_arrays_mfr_0_T60, axis=0)

min_area_mfr_305_T60 = np.min(area_arrays_mfr_305_T60, axis=0)
max_area_mfr_305_T60 = np.max(area_arrays_mfr_305_T60, axis=0)

min_area_mfr_305_T100 = np.min(area_arrays_mfr_305_T100, axis=0)
max_area_mfr_305_T100 = np.max(area_arrays_mfr_305_T100, axis=0)    

min_area_mfr_0_T140 = np.min(area_arrays_mfr_0_T140, axis=0)
max_area_mfr_0_T140 = np.max(area_arrays_mfr_0_T140, axis=0)

min_area_mfr_305_T140 = np.min(area_arrays_mfr_305_T140, axis=0)
max_area_mfr_305_T140 = np.max(area_arrays_mfr_305_T140, axis=0)


# Plot all averages with fill_between for com_x
plt.figure(figsize=(12, 8))

# Define color and linestyle mapping
color_map = {0: 'green', 305: 'red'}
linestyle_map = {60: '-', 100: '--', 140: ':'}
alpha_fill = 0.15  # Transparency for fill_between

# Plot for mfr=0 with fill_between
plt.plot(common_time, avg_com_x_arrays_mfr_0_T60, color=color_map[0], linestyle=linestyle_map[60], label='mfr0, T60')
plt.fill_between(common_time, min_com_x_mfr_0_T60, max_com_x_mfr_0_T60, 
                 color=color_map[0], alpha=alpha_fill)

plt.plot(common_time, avg_com_x_arrays_mfr_0_T140, color=color_map[0], linestyle=linestyle_map[140], label='mfr0, T140')
plt.fill_between(common_time, min_com_x_mfr_0_T140, max_com_x_mfr_0_T140, 
                 color=color_map[0], alpha=alpha_fill)

# Plot for mfr=305 with fill_between
plt.plot(common_time, avg_com_x_arrays_mfr_305_T60, color=color_map[305], linestyle=linestyle_map[60], label='mfr305, T60')
plt.fill_between(common_time, min_com_x_mfr_305_T60, max_com_x_mfr_305_T60, 
                 color=color_map[305], alpha=alpha_fill)

plt.plot(common_time, avg_com_x_arrays_mfr_305_T100, color=color_map[305], linestyle=linestyle_map[100], label='mfr305, T100')
plt.fill_between(common_time, min_com_x_mfr_305_T100, max_com_x_mfr_305_T100, 
                 color=color_map[305], alpha=alpha_fill)

plt.plot(common_time, avg_com_x_arrays_mfr_305_T140, color=color_map[305], linestyle=linestyle_map[140], label='mfr305, T140')
plt.fill_between(common_time, min_com_x_mfr_305_T140, max_com_x_mfr_305_T140, 
                 color=color_map[305], alpha=alpha_fill)

plt.grid(True)
plt.xlabel('Czas [s]', fontsize=12)
plt.ylabel('Średnie położenie środka masy w osi x', fontsize=12)
plt.title('Średnie położenie środka masy w osi x dla różnych wydatków masowych i temperatur', fontsize=14)
plt.legend(fontsize=10, loc='best')
plt.tight_layout()
plt.savefig('avg_com_x_all_conditions_with_ranges.png', dpi=300)

ft.plot_com_y_averages_with_ranges(
    common_time,
    avg_com_y_arrays_mfr_0_T60,
    avg_com_y_arrays_mfr_0_T140,
    avg_com_y_arrays_mfr_305_T60,
    avg_com_y_arrays_mfr_305_T100,
    avg_com_y_arrays_mfr_305_T140,
    com_y_arrays_mfr_0_T60,
    com_y_arrays_mfr_0_T140,
    com_y_arrays_mfr_305_T60,
    com_y_arrays_mfr_305_T100,
    com_y_arrays_mfr_305_T140,
    color_map,
    linestyle_map,
    alpha_fill
)

ft.plot_area_averages_with_ranges(
    common_time,
    avg_area_arrays_mfr_0_T60,
    avg_area_arrays_mfr_0_T140,
    avg_area_arrays_mfr_305_T60,
    avg_area_arrays_mfr_305_T100,
    avg_area_arrays_mfr_305_T140,
    com_area_arrays_mfr_0_T60,
    com_area_arrays_mfr_0_T140,
    com_area_arrays_mfr_305_T60,
    com_area_arrays_mfr_305_T100,
    com_area_arrays_mfr_305_T140,
    color_map,
    linestyle_map,
    alpha_fill
)

ft.animate_avg_com_x_vs_com_y(
    avg_com_x_arrays_mfr_0_T60, avg_com_y_arrays_mfr_0_T60,
    avg_com_x_arrays_mfr_0_T140, avg_com_y_arrays_mfr_0_T140,
    avg_com_x_arrays_mfr_305_T60, avg_com_y_arrays_mfr_305_T60,
    avg_com_x_arrays_mfr_305_T100, avg_com_y_arrays_mfr_305_T100,
    avg_com_x_arrays_mfr_305_T140, avg_com_y_arrays_mfr_305_T140,
    color_map, linestyle_map, common_time
)

