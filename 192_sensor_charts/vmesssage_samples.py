import os, sys, math
import numpy as np
import pandas as pd


bit_frequency = 10
bit_frequency_scaling = 'u'
adc_bit_resolution = 12
adc_reference_voltage = 5


os.chdir(sys.path[0])


p_data = pd.read_csv('pressure_measurements.csv')['Pressure (kPa)']
t_data = pd.read_csv('temp_measurements.csv')['Temperature (Celsius)']
h_data = pd.read_csv('humidity_measurements.csv')['rel. humidity (%)']

p_data = (9/280 * p_data + 0.5) * 1.2
t_data = (10000 * math.e ** (3810 * (1/(t_data + 273.15) - 1/298.15))) * 5 / ((10000 * math.e ** (3810 * (1/(t_data + 273.15) - 1/298.15))) + 100000)
h_data = (7/1000 * h_data + 0.15) * 6


def get_adc_code(Vin):
    global adc_bit_resolution, adc_reference_voltage
    return round((Vin / adc_reference_voltage) * (2 ** adc_bit_resolution))

def get_message(min):
    global p_data, t_data, h_data
    p_adc = format(get_adc_code(p_data[min]), '#014b')[2:]
    t_adc = format(get_adc_code(t_data[min]), '#014b')[2:]
    h_adc = format(get_adc_code(h_data[min]), '#014b')[2:]
    return list(f'{p_adc}{t_adc}{h_adc}')


def generate_voltage(message):

    message_copy = message.copy()
    message_copy = [int(bit) for bit in message_copy]

    for start_bit in [0, 1, 1, 1, 1, 1, 1, 1]:
        message_copy.insert(0, start_bit)

    for end_bit in [0, 0, 0, 1]:
        message_copy.append(end_bit)

    is_even = message_copy.count(1) == 0

    message_copy.insert(-5, 1) if is_even else message_copy.insert(-5, 0)
    return message_copy

print(generate_voltage(get_message(40)))