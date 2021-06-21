import os, sys, math
import numpy as np
import pandas as pd

reading_delay_time = 60
time_scale = 'm'

adc_bit_resolution = 12
adc_reference_voltage = 5

os.chdir(sys.path[0])

p_data = pd.read_csv('pressure_measurements.csv')['Pressure (kPa)']
t_data = pd.read_csv('temp_measurements.csv')['Temperature (Celsius)']
h_data = pd.read_csv('humidity_measurements.csv')['rel. humidity (%)']

p_data = (9/280 * p_data + 0.5)
t_data = (10000 * math.e ** (3810 * (1/(t_data + 273.15) - 1/298.15))) * 5 / ((10000 * math.e ** (3810 * (1/(t_data + 273.15) - 1/298.15))) + 100000)
h_data = (7/1000 * h_data + 0.15)


def print_sensor(data):
    global reading_delay_time, time_scale

    time = 0

    for i in data:
        print(f'{time}{time_scale}, {i}')
        time += reading_delay_time



print_sensor(h_data)