import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import funkcjetopt as ft
from pathlib import Path
import os
from matplotlib.animation import FFMpegWriter, PillowWriter
import matplotlib.animation as animation


def analiza_csv(filename):
    fields = []
    rows = []
    # Always use the specified directory for CSV files
    data_dir = r"C:\Users\Salami\Documents\GitHub\Spray-analysys\data_in_csv"
    if not os.path.isabs(filename):
        filename = os.path.join(data_dir, filename)
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")
    with open(filename, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        fields = next(csvreader)
        rows = [row for row in csvreader if row]  # Skip empty rows

    area_index = fields.index('Area')
    x_index = fields.index('X') 
    y_index = fields.index('Y')
    slice_index = fields.index('Slice')

    # Remove outlier rows based on Area
    area_values = np.array([float(row[area_index]) for row in rows])
    median_area = np.median(area_values)
    # Remove rows where Area is more than 100x the median
    filtered_rows = [row for row in rows if abs(float(row[area_index])) <= 100 * median_area]

    # Use filtered rows for further processing
    rows = filtered_rows

    # Convert data to NumPy arrays
    Slice = np.array([float(row[slice_index]) for row in rows])
    Time = Slice / 10000  # Convert to seconds
    Area = np.array([float(row[area_index]) for row in rows])
    X = np.array([float(row[x_index]) for row in rows])
    Y = np.array([float(row[y_index]) for row in rows])
    X_avg=np.mean(X)
    Y_avg=np.mean(Y)
    Area_avg=np.mean(Area)
    # Get all unique Slice values and sort them
    slices = np.unique(Slice)
    Com_x = np.zeros_like(slices)  # Pre-allocate array for Com-x
    Com_y = np.zeros_like(slices)  # Pre-allocate array for CoM_y
    fps = 10000  # Assuming 10000 frames per second, adjust as necessary
    time=slices/fps  # Convert to 
    for i, target_slice in enumerate(slices):
        mask = (Slice == target_slice)
        X_slice = X[mask]
        Area_slice = Area[mask]
        if len(Area_slice) > 0:  # Check if data exists
            numerator = np.sum(X_slice * Area_slice)
            denominator = np.sum(Area_slice)
            Com_x[i] = numerator / denominator if denominator != 0 else np.nan
        else:
            Com_x[i] = np.nan  # Mark missing data
    for i, target_slice in enumerate(slices):
        mask = (Slice == target_slice)
        y_slice = Y[mask]
        Area_slice = Area[mask]
        if len(Area_slice) > 0:  # Check if data exists
            numerator = np.sum(y_slice * Area_slice)
            denominator = np.sum(Area_slice)
            Com_y[i] = numerator / denominator if denominator != 0 else np.nan
        else:
            Com_y[i] = np.nan  # Mark missing data
    z_x = np.polyfit(time, Com_x, 1)
    p_x = np.poly1d(z_x)
    z_y = np.polyfit(time, Com_y, 1)
    p_y = np.poly1d(z_y)
    total_area_per_slice = np.zeros(len(slices))
    for i, target_slice in enumerate(slices):
        mask = (Slice == target_slice)
        total_area_per_slice[i] = np.sum(Area[mask])
    return Area, X, Y, Com_x, Com_y, time, p_x, p_y, X_avg, Y_avg, Area_avg,total_area_per_slice

#zwraca Area=0,X=1 ,Y=2 ,Com_x-3, Com_y-4, time-5, p_x-6, p_y-7, X_avg-8, Y_avg-9, Area_avg-10, Area_total_per_slice-11


def file_reading(): #This function basically just reads the csv in given path and set

    print(os.access("C:\\Users\\Salami\\Documents\\GitHub\\Spray-analysys\\data_in_csv", os.R_OK))  # Check if the directory is writable

    dane = {}

    data_dir = Path("C:\\Users\\Salami\\Documents\\GitHub\\Spray-analysys\\data_in_csv")  

    for i in range(7):  

        filename = data_dir / f'T60mfr0_0{i+1:01d}.csv'

        dane[f'T60mfr0_0{i+1}'] = ft.analiza_csv(str(filename))



    for i in range(7): 

        filename = data_dir / f'T60mfr305_0{i+1:01d}.csv'

        dane[f'T60mfr305_0{i+1}'] = ft.analiza_csv(str(filename))



    for i in range(7):

        filename = data_dir / f'T100mfr305_0{i+1:01d}.csv'

        dane[f'T100mfr305_0{i+1}'] = ft.analiza_csv(str(filename))

    for i in range(7):

        filename = data_dir / f'T140mfr0_0{i+1:01d}.csv'

        dane[f'T140mfr0_0{i+1}'] = ft.analiza_csv(str(filename))

    for i in range(7):

        filename = data_dir / f'T140mfr305_0{i+1:01d}.csv'

        dane[f'T140mfr305_0{i+1}'] = ft.analiza_csv(str(filename))



    for key in dane.keys():

        if 'mfr0' in key:

            dane[key] = (*dane[key], 0)  # Appending MFR 0

        elif 'mfr305' in key:

            dane[key] = (*dane[key], 305)  # Append MFR 305

    return dane


def plot_com_y_averages_with_ranges(
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
):
    # Plot all averages with fill_between for com_y
    plt.figure(figsize=(12, 8))

    # Plot for mfr=0 with fill_between
    plt.plot(common_time, avg_com_y_arrays_mfr_0_T60, color=color_map[0], linestyle=linestyle_map[60], label='mfr0, T60')
    plt.fill_between(common_time, np.min(com_y_arrays_mfr_0_T60, axis=0), np.max(com_y_arrays_mfr_0_T60, axis=0),
                     color=color_map[0], alpha=alpha_fill)

    plt.plot(common_time, avg_com_y_arrays_mfr_0_T140, color=color_map[0], linestyle=linestyle_map[140], label='mfr0, T140')
    plt.fill_between(common_time, np.min(com_y_arrays_mfr_0_T140, axis=0), np.max(com_y_arrays_mfr_0_T140, axis=0),
                     color=color_map[0], alpha=alpha_fill)

    # Plot for mfr=305 with fill_between
    plt.plot(common_time, avg_com_y_arrays_mfr_305_T60, color=color_map[305], linestyle=linestyle_map[60], label='mfr305, T60')
    plt.fill_between(common_time, np.min(com_y_arrays_mfr_305_T60, axis=0), np.max(com_y_arrays_mfr_305_T60, axis=0),
                     color=color_map[305], alpha=alpha_fill)

    plt.plot(common_time, avg_com_y_arrays_mfr_305_T100, color=color_map[305], linestyle=linestyle_map[100], label='mfr305, T100')
    plt.fill_between(common_time, np.min(com_y_arrays_mfr_305_T100, axis=0), np.max(com_y_arrays_mfr_305_T100, axis=0),
                     color=color_map[305], alpha=alpha_fill)

    plt.plot(common_time, avg_com_y_arrays_mfr_305_T140, color=color_map[305], linestyle=linestyle_map[140], label='mfr305, T140')
    plt.fill_between(common_time, np.min(com_y_arrays_mfr_305_T140, axis=0), np.max(com_y_arrays_mfr_305_T140, axis=0),
                     color=color_map[305], alpha=alpha_fill)

    plt.grid(True)
    plt.xlabel('Czas [s]', fontsize=12)
    plt.ylabel('Średnie położenie środka masy w osi y', fontsize=12)
    plt.title('Średnie położenie środka masy w osi y dla różnych wydatków masowych i temperatur', fontsize=14)
    plt.legend(fontsize=10, loc='best')
    plt.tight_layout()
    plt.savefig('avg_com_y_all_conditions_with_ranges.png', dpi=300)
    plt.show()


def plot_area_averages_with_ranges(
        common_time,
        avg_area_arrays_mfr_0_T60,
        avg_area_arrays_mfr_0_T140,
        avg_area_arrays_mfr_305_T60,
        avg_area_arrays_mfr_305_T100,
        avg_area_arrays_mfr_305_T140,
        area_arrays_mfr_0_T60,
        area_arrays_mfr_0_T140,
        area_arrays_mfr_305_T60,
        area_arrays_mfr_305_T100,
        area_arrays_mfr_305_T140,
        color_map,
        linestyle_map,
        alpha_fill
    ):
        # First plot: with fill_between
        plt.figure(figsize=(12, 8))

        # Plot for mfr=0 with fill_between
        plt.plot(common_time, avg_area_arrays_mfr_0_T60, color=color_map[0], linestyle=linestyle_map[60], label='mfr0, T60')
        plt.fill_between(common_time, np.min(area_arrays_mfr_0_T60, axis=0), np.max(area_arrays_mfr_0_T60, axis=0),
                         color=color_map[0], alpha=alpha_fill)

        plt.plot(common_time, avg_area_arrays_mfr_0_T140, color=color_map[0], linestyle=linestyle_map[140], label='mfr0, T140')
        plt.fill_between(common_time, np.min(area_arrays_mfr_0_T140, axis=0), np.max(area_arrays_mfr_0_T140, axis=0),
                         color=color_map[0], alpha=alpha_fill)

        # Plot for mfr=305 with fill_between
        plt.plot(common_time, avg_area_arrays_mfr_305_T60, color=color_map[305], linestyle=linestyle_map[60], label='mfr305, T60')
        plt.fill_between(common_time, np.min(area_arrays_mfr_305_T60, axis=0), np.max(area_arrays_mfr_305_T60, axis=0),
                         color=color_map[305], alpha=alpha_fill)

        plt.plot(common_time, avg_area_arrays_mfr_305_T100, color=color_map[305], linestyle=linestyle_map[100], label='mfr305, T100')
        plt.fill_between(common_time, np.min(area_arrays_mfr_305_T100, axis=0), np.max(area_arrays_mfr_305_T100, axis=0),
                         color=color_map[305], alpha=alpha_fill)

        plt.plot(common_time, avg_area_arrays_mfr_305_T140, color=color_map[305], linestyle=linestyle_map[140], label='mfr305, T140')
        plt.fill_between(common_time, np.min(area_arrays_mfr_305_T140, axis=0), np.max(area_arrays_mfr_305_T140, axis=0),
                         color=color_map[305], alpha=alpha_fill)

        plt.grid(True)
        plt.xlabel('Czas [s]', fontsize=12)
        plt.ylabel('Średnia powierzchnia', fontsize=12)
        plt.title('Średnia powierzchnia dla różnych wydatków masowych i temperatur (z zakresem)', fontsize=14)
        plt.legend(fontsize=10, loc='best')
        plt.tight_layout()
        plt.savefig('avg_area_all_conditions_with_ranges.png', dpi=300)
        plt.show()

        # Second plot: only averages, no fill_between
        plt.figure(figsize=(12, 8))

        plt.plot(common_time, avg_area_arrays_mfr_0_T60, color=color_map[0], linestyle=linestyle_map[60], label='mfr0, T60')
        plt.plot(common_time, avg_area_arrays_mfr_0_T140, color=color_map[0], linestyle=linestyle_map[140], label='mfr0, T140')
        plt.plot(common_time, avg_area_arrays_mfr_305_T60, color=color_map[305], linestyle=linestyle_map[60], label='mfr305, T60')
        plt.plot(common_time, avg_area_arrays_mfr_305_T100, color=color_map[305], linestyle=linestyle_map[100], label='mfr305, T100')
        plt.plot(common_time, avg_area_arrays_mfr_305_T140, color=color_map[305], linestyle=linestyle_map[140], label='mfr305, T140')

        plt.grid(True)
        plt.xlabel('Czas [s]', fontsize=12)
        plt.ylabel('Średnia powierzchnia', fontsize=12)
        plt.title('Średnia powierzchnia dla różnych wydatków masowych i temperatur (tylko średnie)', fontsize=14)
        plt.legend(fontsize=10, loc='best')
        plt.tight_layout()
        plt.savefig('avg_area_all_conditions_averages_only.png', dpi=300)
        plt.show()


def animate_avg_com_x_vs_com_y(
    avg_com_x_arrays_mfr_0_T60, avg_com_y_arrays_mfr_0_T60,
    avg_com_x_arrays_mfr_0_T140, avg_com_y_arrays_mfr_0_T140,
    avg_com_x_arrays_mfr_305_T60, avg_com_y_arrays_mfr_305_T60,
    avg_com_x_arrays_mfr_305_T100, avg_com_y_arrays_mfr_305_T100,
    avg_com_x_arrays_mfr_305_T140, avg_com_y_arrays_mfr_305_T140,
    color_map, linestyle_map, common_time
):
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Set axis limits based on all data
    all_x = np.concatenate([
        avg_com_x_arrays_mfr_0_T60,
        avg_com_x_arrays_mfr_0_T140,
        avg_com_x_arrays_mfr_305_T60,
        avg_com_x_arrays_mfr_305_T100,
        avg_com_x_arrays_mfr_305_T140
    ])
    all_y = np.concatenate([
        avg_com_y_arrays_mfr_0_T60,
        avg_com_y_arrays_mfr_0_T140,
        avg_com_y_arrays_mfr_305_T60,
        avg_com_y_arrays_mfr_305_T100,
        avg_com_y_arrays_mfr_305_T140
    ])
    
    ax.set_xlim(np.min(all_x) - 50, np.max(all_x) + 50)
    ax.set_ylim(np.min(all_y) - 50, np.max(all_y) + 50)
    
    # Data arrays for each condition
    data = [
        (avg_com_x_arrays_mfr_0_T60, avg_com_y_arrays_mfr_0_T60, 'mfr0, T60'),
        (avg_com_x_arrays_mfr_0_T140, avg_com_y_arrays_mfr_0_T140, 'mfr0, T140'),
        (avg_com_x_arrays_mfr_305_T60, avg_com_y_arrays_mfr_305_T60, 'mfr305, T60'),
        (avg_com_x_arrays_mfr_305_T100, avg_com_y_arrays_mfr_305_T100, 'mfr305, T100'),
        (avg_com_x_arrays_mfr_305_T140, avg_com_y_arrays_mfr_305_T140, 'mfr305, T140')
    ]
    
    # Create lines and dots for each trajectory
    lines = []
    dots = []
    for (x, y, label) in data:
        color = color_map[0] if 'mfr0' in label else color_map[305]
        linestyle = (
            linestyle_map[60] if 'T60' in label else
            linestyle_map[100] if 'T100' in label else
            linestyle_map[140]
        )
        
        line, = ax.plot([], [], color=color, linestyle=linestyle, label=label)
        dot, = ax.plot([], [], 'o', color=color, markersize=8)
        lines.append(line)
        dots.append(dot)
    
    # Add time text
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12)
    
    ax.set_xlabel('Średnie położenie środka masy w osi x')
    ax.set_ylabel('Średnie położenie środka masy w osi y')
    ax.set_title('Trajektorie średniego środka masy (x vs y) dla różnych warunków')
    ax.legend(fontsize=10, loc='best')
    ax.grid(True)
    plt.tight_layout()

    n_frames = len(common_time)
    
    def init():
        for line in lines:
            line.set_data([], [])
        for dot in dots:
            dot.set_data([], [])
        time_text.set_text('')
        return lines + dots + [time_text]
    
    def update(frame):
        current_time = common_time[frame]
        time_text.set_text(f'Czas: {current_time:.2f} s')
        
        for i, (line, dot, (x_data, y_data, _)) in enumerate(zip(lines, dots, data)):
            # Update line with trajectory up to current frame
            line.set_data(x_data[:frame+1], y_data[:frame+1])
            
            # Update dot with current position
            if frame < len(x_data) and frame < len(y_data):
                dot.set_data([x_data[frame]], [y_data[frame]])
        
        return lines + dots + [time_text]

    # Create animation with smooth timing
    fps = 30  # Frames per second
    interval = 1000 / fps  # ms between frames
    
    ani = animation.FuncAnimation(
        fig, update, frames=n_frames, init_func=init,
        blit=True, interval=interval, repeat_delay=3000
    )
    
    # Save with appropriate writer
    try:
        writer = animation.FFMpegWriter(fps=fps)
        ext = 'mp4'
    except (RuntimeError, ImportError):
        writer = animation.PillowWriter(fps=fps)
        ext = 'gif'
    
    filename = f'avg_com_x_vs_com_y_all_conditions_anim.{ext}'
    ani.save(filename, writer=writer, dpi=150)
    plt.show()
    plt.close(fig)
    print(f"Animation saved as {filename}")