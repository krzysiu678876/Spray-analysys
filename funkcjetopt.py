import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import funkcjetopt as ft
from pathlib import Path
import os


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
    #print("Columns in the CSV file:", fields)
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

    return Area, X, Y, Com_x, Com_y, time, p_x, p_y, X_avg, Y_avg, Area_avg
#zwraca Area=0,X=1 ,Y=2 ,Com_x-3, Com_y-4, time-5, p_x-6, p_y-7, X_avg-8, Y_avg-9, Area_avg-10    


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
