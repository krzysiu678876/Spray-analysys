import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import funkcjetopt as ft


def analiza_csv(filename):
    fields = []
    rows = []

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

    return Area,X ,Y ,Com_x, Com_y, time, p_x, p_y, X_avg, Y_avg, Area_avg
#zwraca Area=0,X=1 ,Y=2 ,Com_x-3, Com_y-4, time-5, p_x-6, p_y-7, X_avg-8, Y_avg-9, Area_avg-10    
#transformacja plików
if 1==0:
    ft.transform_csv('Tc_140_mfr_0T1_C001H001S0001.csv')
    ft.transform_csv('Tc_140_mfr_0T1_C001H001S0002.csv')
    ft.transform_csv('Tc_140_mfr_0T1_C001H001S0003.csv')
    ft.transform_csv('Tc_140_mfr_0T1_C001H001S0004.csv')
    ft.transform_csv('Tc_140_mfr_0T1_C001H001S0005.csv')
    ft.transform_csv('Tc_140_mfr_0T1_C001H001S0006.csv')
    ft.transform_csv('Tc_140_mfr_0T1_C001H001S0007.csv')
    ft.transform_csv('Tc_140_mfr_305T1_C001H001S0001.csv')
    ft.transform_csv('Tc_140_mfr_305T1_C001H001S0002.csv')
    ft.transform_csv('Tc_140_mfr_305T1_C001H001S0003.csv')

#czytanie plików 
dane = {}
for i in range(7):  # For files 0001 to 0007
    filename = f'Tc_140_mfr_0T1_C001H001S{i+1:04d}.csv'
    dane[f'Tc140mfr0{i+1}'] = ft.analiza_csv(filename)

for i in range(3):  # For files 0001 to 0003
    filename = f'Tc_140_mfr_305T1_C001H001S{i+1:04d}.csv'
    dane[f'Tc140mfr305{i+1}'] = ft.analiza_csv(filename)
#jak doda kolumne z MFR???
#stworzone kolumny z MFR 0 i 305 od dlugości kolumny z czasem
#mfr_305 = np.full_like(len(dane[5][5]),305)
#mfr_0 = np.full_like(len(dane[5][5]),0)
#stare już te mfr

for key in dane.keys():
    if 'mfr0' in key:
        dane[key] = (*dane[key], 0)  # Append MFR 0
    elif 'mfr305' in key:
        dane[key] = (*dane[key], 305)  # Append MFR 305

com_x_1_4_sum_mfr_0 = 0
com_x_2_4_sum_mfr_0 = 0
com_x_3_4_sum_mfr_0 = 0
com_x_4_4_sum_mfr_0 = 0
com_y_1_4_sum_mfr_0 = 0
com_y_2_4_sum_mfr_0 = 0
com_y_3_4_sum_mfr_0 = 0
com_y_4_4_sum_mfr_0 = 0

com_x_1_4_sum_mfr_305 = 0
com_x_2_4_sum_mfr_305 = 0
com_x_3_4_sum_mfr_305 = 0
com_x_4_4_sum_mfr_305 = 0
com_y_1_4_sum_mfr_305 = 0
com_y_2_4_sum_mfr_305 = 0
com_y_3_4_sum_mfr_305 = 0
com_y_4_4_sum_mfr_305 = 0

mfr0_count=7
mfr305_count=3

for key in dane.keys():
    if 'mfr0' in key:
        time = dane[key][5]
        com_x = dane[key][3]
        com_y = dane[key][4]
        max_time = np.max(time)
        min_time = np.min(time)
        time_1_4 = min_time + (max_time - min_time) / 4
        time_2_4 = min_time + 2 * (max_time - min_time) / 4
        time_3_4 = min_time + 3 * (max_time - min_time) / 4
        time_4_4 = max_time  # xd kocham copilota
        # teraz szukam wartosci dla tych czasów
        com_x_1_4 = com_x[np.abs(time - time_1_4).argmin()]
        com_x_2_4 = com_x[np.abs(time - time_2_4).argmin()]
        com_x_3_4 = com_x[np.abs(time - time_3_4).argmin()]
        com_x_4_4 = com_x[np.abs(time - time_4_4).argmin()]
        com_y_1_4 = com_y[np.abs(time - time_1_4).argmin()]
        com_y_2_4 = com_y[np.abs(time - time_2_4).argmin()]
        com_y_3_4 = com_y[np.abs(time - time_3_4).argmin()]
        com_y_4_4 = com_y[np.abs(time - time_4_4).argmin()]
        plt.scatter(0, com_x_1_4, label=f't={time_1_4}s', alpha=0.5)
        plt.scatter(0, com_x_2_4, label=f't={time_2_4}s', alpha=0.5)
        plt.scatter(0, com_x_3_4, label=f't={time_3_4}s', alpha=0.5)
        plt.scatter(0, com_x_4_4, label=f't={time_4_4}s', alpha=0.5)
        com_x_1_4_sum_mfr_0 += com_x_1_4
        com_x_2_4_sum_mfr_0 += com_x_2_4
        com_x_3_4_sum_mfr_0 += com_x_3_4
        com_x_4_4_sum_mfr_0 += com_x_4_4
        com_y_1_4_sum_mfr_0 += com_y_1_4
        com_y_2_4_sum_mfr_0 += com_y_2_4
        com_y_3_4_sum_mfr_0 += com_y_3_4
        com_y_4_4_sum_mfr_0 += com_y_4_4
    com_x_1_4_avg = com_x_1_4_sum_mfr_0 / mfr0_count
    com_x_2_4_avg = com_x_2_4_sum_mfr_0 / mfr0_count
    com_x_3_4_avg = com_x_3_4_sum_mfr_0 / mfr0_count
    com_x_4_4_avg = com_x_4_4_sum_mfr_0 / mfr0_count
    com_y_1_4_avg = com_y_1_4_sum_mfr_0 / mfr0_count
    com_y_2_4_avg = com_y_2_4_sum_mfr_0 / mfr0_count
    com_y_3_4_avg = com_y_3_4_sum_mfr_0 / mfr0_count
    com_y_4_4_avg = com_y_4_4_sum_mfr_0 / mfr0_count
        

    if 'mfr305' in key:
        time = dane[key][5]
        com_x = dane[key][3]
        com_y = dane[key][4]
        max_time = np.max(time)
        min_time = np.min(time)
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
        plt.scatter(305,com_x_1_4, label=f't={time_1_4}s', alpha=0.5)
        plt.scatter(305,com_x_2_4,label=f't={time_2_4}s', alpha=0.5)
        plt.scatter(305,com_x_3_4, label=f't={time_3_4}s', alpha=0.5)
        plt.scatter(305,com_x_4_4, label=f't={time_4_4}s', alpha=0.5)
        com_x_1_4_sum_mfr_305 += com_x_1_4
        com_x_2_4_sum_mfr_305 += com_x_2_4
        com_x_3_4_sum_mfr_305 += com_x_3_4
        com_x_4_4_sum_mfr_305 += com_x_4_4
        com_y_1_4_sum_mfr_305 += com_y_1_4
        com_y_2_4_sum_mfr_305 += com_y_2_4
        com_y_3_4_sum_mfr_305 += com_y_3_4
        com_y_4_4_sum_mfr_305 += com_y_4_4
    
    com_x_1_4_avg_mfr305 = com_x_1_4_sum_mfr_305 / mfr305_count
    com_x_2_4_avg_mfr305 = com_x_2_4_sum_mfr_305 / mfr305_count
    com_x_3_4_avg_mfr305 = com_x_3_4_sum_mfr_305 / mfr305_count
    com_x_4_4_avg_mfr305 = com_x_4_4_sum_mfr_305 / mfr305_count
    com_y_1_4_avg_mfr305 = com_y_1_4_sum_mfr_305 / mfr305_count
    com_y_2_4_avg_mfr305 = com_y_2_4_sum_mfr_305 / mfr305_count
    com_y_3_4_avg_mfr305 = com_y_3_4_sum_mfr_305 / mfr305_count
    com_y_4_4_avg_mfr305 = com_y_4_4_sum_mfr_305 / mfr305_count

plt.ylabel('środek masy x')
plt.legend()
plt.xlabel('MFR(wydatek masowy)')
plt.title('polożenie środka masy w czasie')
plt.show()
#zrobione dla 4 czasów 1/4 2/4,3/4,4/4 t max(zobaczymy co wyjdzie)
com_x_avg_mfr0 = [com_x_1_4_avg, com_x_2_4_avg, com_x_3_4_avg, com_x_4_4_avg]
com_y_avg_mfr0 = [com_y_1_4_avg, com_y_2_4_avg, com_y_3_4_avg, com_y_4_4_avg]
com_x_avg_mfr305 = [com_x_1_4_avg_mfr305, com_x_2_4_avg_mfr305, com_x_3_4_avg_mfr305, com_x_4_4_avg_mfr305]
com_y_avg_mfr305 = [com_y_1_4_avg_mfr305, com_y_2_4_avg_mfr305, com_y_3_4_avg_mfr305, com_y_4_4_avg_mfr305]

for i in range(4):
    plt.scatter(0, com_x_avg_mfr0[i],alpha=0.5,label = f't={i+1}/4')
    plt.scatter(305, com_x_avg_mfr305[i],alpha=0.5,label = f't={i+1}/4')

plt.ylabel('uśrednione wartości dla położenia środka masy w osi x')  # XDD ale wtedy t=1/4 tmax ale liczbowo czasy pewnie się nie będą zgadzać
plt.xlabel('wtryskiwany wydatek masowy')
plt.legend()
plt.title('położenie środka masy na osi X w funkcji wydatku i czasu')
plt.show()
plt.savefig('uśrednionowe SMX')

for i in range(4):
    plt.scatter(0, com_y_avg_mfr0[i],alpha=0.5,label = f't={i+1}/4')
    plt.scatter(305, com_y_avg_mfr305[i],alpha=0.5,label = f't={i+1}/4')
plt.ylabel('uśrednione wartości dla położenia środka masy w osi y')  # XDD ale wtedy t=1/4 tmax ale liczbowo czasy pewnie się nie będą zgadzać
plt.xlabel('wtryskiwany wydatek masowy')
plt.legend()
plt.title('położenie środka masy na osi Y w funkcji wydatku i czasu')
plt.show()
plt.savefig('uśrednionowe SMY')
 
Area_1_4_sum_mfr_0 = 0
Area_2_4_sum_mfr_0 = 0
Area_3_4_sum_mfr_0 = 0
Area_4_4_sum_mfr_0 = 0
Area_1_4_sum_mfr_305 = 0
Area_2_4_sum_mfr_305 = 0
Area_3_4_sum_mfr_305 = 0
Area_4_4_sum_mfr_305 = 0 
for key in dane.keys():
    if 'mfr0' in key:
        time = dane[key][5]
        Area = dane[key][0]
        max_time = np.max(time)
        min_time = np.min(time)
        time_1_4 = min_time + (max_time - min_time) / 4
        time_2_4 = min_time + 2 * (max_time - min_time) / 4
        time_3_4 = min_time + 3 * (max_time - min_time) / 4
        time_4_4 = max_time
        Area_1_4 = np.sum(Area[np.abs(time - time_1_4).argmin()])
        Area_2_4 = np.sum(Area[np.abs(time - time_2_4).argmin()])
        Area_3_4 = np.sum(Area[np.abs(time - time_3_4).argmin()])
        Area_4_4 = np.sum(Area[np.abs(time - time_4_4).argmin()])
        plt.scatter(0, Area_1_4, alpha=0.5, label='t=1/4')
        plt.scatter(0, Area_2_4, alpha=0.5, label='t=2/4')
        plt.scatter(0, Area_3_4, alpha=0.5, label='t=3/4')
        plt.scatter(0, Area_4_4, alpha=0.5, label='t=4/4')
        Area_1_4_sum_mfr_0 += Area_1_4  
        Area_2_4_sum_mfr_0 += Area_2_4
        Area_3_4_sum_mfr_0 += Area_3_4
        Area_4_4_sum_mfr_0 += Area_4_4
    Area_1_4_avg_mfr0 = Area_1_4_sum_mfr_0 / mfr0_count
    Area_2_4_avg_mfr0 = Area_2_4_sum_mfr_0 / mfr0_count
    Area_3_4_avg_mfr0 = Area_3_4_sum_mfr_0 / mfr0_count
    Area_4_4_avg_mfr0 = Area_4_4_sum_mfr_0 / mfr0_count
    if 'mfr305' in key:
        time = dane[key][5]
        Area = dane[key][0]
        max_time = np.max(time)
        min_time = np.min(time)
        time_1_4 = min_time + (max_time - min_time) / 4
        time_2_4 = min_time + 2 * (max_time - min_time) / 4
        time_3_4 = min_time + 3 * (max_time - min_time) / 4
        time_4_4 = max_time
        Area_1_4 = np.sum(Area[np.abs(time - time_1_4).argmin()])
        Area_2_4 = np.sum(Area[np.abs(time - time_2_4).argmin()])
        Area_3_4 = np.sum(Area[np.abs(time - time_3_4).argmin()])
        Area_4_4 = np.sum(Area[np.abs(time - time_4_4).argmin()])
        plt.scatter(305, Area_1_4, alpha=0.5, label='t=1/4')
        plt.scatter(305, Area_2_4, alpha=0.5, label='t=2/4')
        plt.scatter(305, Area_3_4, alpha=0.5, label='t=3/4')
        plt.scatter(305, Area_4_4, alpha=0.5, label='t=4/4')
        Area_1_4_sum_mfr_305 += Area_1_4
        Area_2_4_sum_mfr_305 += Area_2_4
        Area_3_4_sum_mfr_305 += Area_3_4
        Area_4_4_sum_mfr_305 += Area_4_4
    Area_1_4_avg_mfr305 = Area_1_4_sum_mfr_305 / mfr305_count
    Area_2_4_avg_mfr305 = Area_2_4_sum_mfr_305 / mfr305_count
    Area_3_4_avg_mfr305 = Area_3_4_sum_mfr_305 / mfr305_count
    Area_4_4_avg_mfr305 = Area_4_4_sum_mfr_305 / mfr305_count
plt.ylabel('Pole powierzchni')
plt.xlabel('wydatek masowy')
plt.legend()
plt.title('Pole powierzchni wtryskiwanego paliwa w zależności od czasu i wydatku masowego')
plt.legend()
plt.show()
plt.savefig('A(mft,t)')



Area_avg_mfr0 = [Area_1_4_avg_mfr0, Area_2_4_avg_mfr0, Area_3_4_avg_mfr0, Area_4_4_avg_mfr0]
Area_avg_mfr305 = [Area_1_4_avg_mfr305, Area_2_4_avg_mfr305, Area_3_4_avg_mfr305, Area_4_4_avg_mfr305]

for i in range(4):
    plt.scatter(0, Area_avg_mfr0[i], alpha=0.5, label=f't={i+1}/4')
    plt.scatter(305, Area_avg_mfr305[i], alpha=0.5, label=f't={i+1}/4')
plt.xlabel('Wydatek masowy wtryskiwanego paliwa')
plt.ylabel('Pole powierzchni wtryskiwanego paliwa')
plt.legend()
plt.title('Pole powierzchni wtryskiwanego paliwa w zależności od czasu i wydatku masowego')
plt.show()
plt.savefig('A_avg(mft,t)')


x_avg = {}
plotted_mfr0 = False
plotted_mfr305 = False

for key in dane.keys():
    if 'mfr0' in key:
        time = dane[key][5]
        com_x = dane[key][3]

        label = 'mfr0' if not plotted_mfr0 else None
        plt.plot(time, com_x, 'green', label=label)
        plotted_mfr0 = True

        for t, x in zip(time, com_x):
            if t not in x_avg:
                x_avg[t] = []
            x_avg[t].append(x)

# Compute and plot average x
time_sorted = sorted(x_avg)
x_avg_vals = [sum(x_avg[t]) / len(x_avg[t]) for t in time_sorted]
plt.plot(time_sorted, x_avg_vals, 'orange', label='avg mfr0')  # changed to blue for clarity

x_avg = {}
for key in dane.keys():
    if 'mfr305' in key:
        time = dane[key][5]
        com_x = dane[key][3]

        label='mfr305' if not plotted_mfr305 else None
        plt.plot(time, com_x, 'red', label=label)
        plotted_mfr305 = True

        for t, x in zip(time, com_x):
            if t not in x_avg:
                x_avg[t] = []
            x_avg[t].append(x)

time_sorted = sorted(x_avg)
x_avg_vals = [sum(x_avg[t]) / len(x_avg[t]) for t in time_sorted]
plt.plot(time_sorted, x_avg_vals, 'blue', label='avg mfr305')

plt.ylabel('położenie cząsteczek x')
plt.xlabel('czas')
plt.legend()
plt.title('Położenie cząsteczek w osi x w funkcji czasu i wydatku masowego')

plt.savefig('x(t).png')  # Save before show
plt.show()

y_avg = {}

for key in dane.keys():

    if 'mfr0' in key:
        time = dane[key][5]
        com_x = dane[key][3]
        com_y = dane[key][4]

        label='mfr0' if not plotted_mfr0 else None
        plt.plot(time, com_y,'green', label=label)
        plotted_mfr0 = True

        for t, x in zip(time, com_y):
            if t not in y_avg:
                y_avg[t] = []
            y_avg[t].append(x)

time_sorted = sorted(y_avg)
y_avg_vals = [sum(y_avg[t]) / len(y_avg[t]) for t in time_sorted]
plt.plot(time_sorted, y_avg_vals, 'orange', label='avg mfr0')

y_avg = {}
for key in dane.keys():
    if 'mfr305' in key:
        time = dane[key][5]
        com_y = dane[key][4]
        label='mfr305' if not plotted_mfr305 else None
        plt.plot(time, com_y,'purple',label=label)
        plotted_mfr305 = True

        for t, x in zip(time, com_y):
            if t not in y_avg:
                y_avg[t] = []
            y_avg[t].append(x)

time_sorted = sorted(y_avg)
y_avg_vals = [sum(y_avg[t]) / len(y_avg[t]) for t in time_sorted]
plt.plot(time_sorted, y_avg_vals, 'blue', label='avg mfr305')

plt.xlabel('czas')
plt.ylabel('położenie cząsteczek y')
plt.legend()
plt.title('położenie cząsteczek w osi y w funkcji czasu i wydatku masowego')
plt.show()  
plt.savefig('y(t)') 
#dodatkowo zamiast x(t) można zrobić deltx(t) czyli dać początek układu równań w punkcie wtrysku
#DOKUMENTACJA

'''בדרך כלל אין לי מושג מה אני כותב פה
הפרםגרם הזה מקל קבוצות קבצי CSV עם נתונים על תנועת דלק במנועי טורבו דיזל
הוא מנתח את הנתונים ומחשב את מרכז המסה של הדלק במנוע
אבל לא צריך להיות במנוע
הוא גם מחשב את שטח הפנים של הדלק במנוע
'''

