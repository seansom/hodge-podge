import os, sys, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 


max_allowable_error = 0.01
adc_bit_resolution = 12
adc_reference_voltage = 5


os.chdir(sys.path[0])


p_data = pd.read_csv('pressure_measurements.csv')['Pressure (kPa)']
t_data = pd.read_csv('temp_measurements.csv')['Temperature (Celsius)']
h_data = pd.read_csv('humidity_measurements.csv')['rel. humidity (%)']

p_error = max_allowable_error * (max(p_data) - min(p_data))
t_error = max_allowable_error * (max(t_data) - min(t_data))
h_error = max_allowable_error * (max(h_data) - min(h_data))

p_data = (9/280 * p_data + 0.5) * 1.2
t_data = (10000 * math.e ** (3810 * (1/(t_data + 273.15) - 1/298.15))) * 5 / ((10000 * math.e ** (3810 * (1/(t_data + 273.15) - 1/298.15))) + 100000)
h_data = (7/1000 * h_data + 0.15) * 6



def get_adc_code(Vin):
    global adc_bit_resolution, adc_reference_voltage
    return round((Vin / adc_reference_voltage) * (2 ** adc_bit_resolution))


def get_adc_max_change(data):

    max_change = 0
    x, y = -1, -1

    for i in range(0, len(data) - 1):
        if abs(data[i + 1] - data[i]) > max_change:
            max_change = abs(data[i + 1] - data[i])
            x, y = i, i + 1

    # print(y, x)

    return abs(get_adc_code(data[y]) - get_adc_code(data[x]))


def get_adc_relative_resolution(data):
    return math.log(get_adc_code(max(data)) - get_adc_code(min(data)), 2)


def get_min_sampling_freq(data):
    global max_allowable_error

    return (get_adc_max_change(data) / (max_allowable_error * (2 ** get_adc_relative_resolution(data))))


def get_max_sampling_freq(data):
    return get_adc_max_change(data)



print('===========================================')

print(f'ADC bit resolution: {adc_bit_resolution}')
print(f'Error Percent: {max_allowable_error}')

print('===========================================')

print(f'pressure error: {round(p_error, 4)} kPa')
print(f'temp error: {round(t_error, 4)} °C')
print(f'humidity error: {round(h_error, 4)} %')

print('===========================================')

print(f'pressure relative bit resolution: {round(get_adc_relative_resolution(p_data), 6)}')
print(f'temp relative bit resolution: {round(get_adc_relative_resolution(t_data), 6)}')
print(f'humidity relative bit resolution: {round(get_adc_relative_resolution(h_data), 6)}')

print('===========================================')

print(f'pressure min freq : {round(get_min_sampling_freq(p_data), 4)} samples/min')
print(f'temp min freq : {round(get_min_sampling_freq(t_data), 4)} samples/min')
print(f'humidity min freq : {round(get_min_sampling_freq(h_data), 4)} samples/min')

print('===========================================')

print(f'pressure max freq : {round(get_max_sampling_freq(p_data), 4)} samples/min')
print(f'temp max freq : {round(get_max_sampling_freq(t_data), 4)} samples/min')
print(f'humidity max freq : {round(get_max_sampling_freq(h_data), 4)} samples/min')