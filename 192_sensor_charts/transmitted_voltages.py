import os, sys, math
import numpy as np
import pandas as pd

bit_transmit_time = 20
transmit_delay_time = 0
time_scale = 'u'

adc_bit_resolution = 12
adc_reference_voltage = 5

os.chdir(sys.path[0])

p_data = pd.read_csv('pressure_measurements.csv')['Pressure (kPa)']
t_data = pd.read_csv('temp_measurements.csv')['Temperature (Celsius)']
h_data = pd.read_csv('humidity_measurements.csv')['rel. humidity (%)']

p_data = (9/280 * p_data + 0.5)
t_data = (10000 * math.e ** (3810 * (1/(t_data + 273.15) - 1/298.15))) * 5 / ((10000 * math.e ** (3810 * (1/(t_data + 273.15) - 1/298.15))) + 100000)
h_data = (7/1000 * h_data + 0.15)



def get_data_bits(Vin):
    global adc_bit_resolution, adc_reference_voltage
    return [int(i) for i in list(format(round((Vin / adc_reference_voltage) * (2 ** adc_bit_resolution)), '012b'))]



def print_data_voltage():

    time = 0 + transmit_delay_time

    if time != 0:
        print(f'0{time_scale}, 0')
        print(f'{time}{time_scale}, 0')

    for minute in range(len(t_data)):

        for bit in get_data_bits(p_data[minute]):
            print(f'{time}{time_scale}, {5 if bit else 0}')
            print(f'{time + bit_transmit_time}{time_scale}, {5 if bit else 0}')
            time += bit_transmit_time

        parity = get_data_bits(p_data[minute]).count(1) % 2 == 0
        print(f'{time}{time_scale}, {0 if parity else 5}')
        print(f'{time + bit_transmit_time}{time_scale}, {0 if parity else 5}')
        time += bit_transmit_time

        for bit in get_data_bits(t_data[minute]):
            print(f'{time}{time_scale}, {5 if bit else 0}')
            print(f'{time + bit_transmit_time}{time_scale}, {5 if bit else 0}')
            time += bit_transmit_time

        parity = get_data_bits(t_data[minute]).count(1) % 2 == 0
        print(f'{time}{time_scale}, {0 if parity else 5}')
        print(f'{time + bit_transmit_time}{time_scale}, {0 if parity else 5}')
        time += bit_transmit_time

        for bit in get_data_bits(h_data[minute]):
            print(f'{time}{time_scale}, {5 if bit else 0}')
            print(f'{time + bit_transmit_time}{time_scale}, {5 if bit else 0}')
            time += bit_transmit_time

        parity = get_data_bits(h_data[minute]).count(1) % 2 == 0
        print(f'{time}{time_scale}, {0 if parity else 5}')
        print(f'{time + bit_transmit_time}{time_scale}, {0 if parity else 5}')
        time += bit_transmit_time



def print_clock_voltage():

    time = 0 + transmit_delay_time

    if time != 0:
        print(f'0{time_scale}, 0')
        print(f'{time}{time_scale}, 0')

    curr_voltage = 0

    for _ in range(len(t_data)):
        for _ in range(39):
            print(f'{time}{time_scale}, {5 if not curr_voltage else 0}')
            print(f'{time + bit_transmit_time}{time_scale}, {5 if not curr_voltage else 0}')
            curr_voltage = 5 if not curr_voltage else 0
            time += bit_transmit_time
    


print_data_voltage()
# print_clock_voltage()

    