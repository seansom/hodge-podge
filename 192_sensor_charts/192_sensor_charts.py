# TO RUN THIS CODE, INSTALL FIRST ITS DEPENDENCIES
# Run in the terminal 'pip install requirements.txt'
# When the code is running, input # 1 - 9 to view a chart
# Input q to quit the program

import os, sys, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

os.chdir(sys.path[0])

plt.style.use('fivethirtyeight')


def within(num, lo, hi):
    return lo <= num and num <= hi

def pressure():
    p_data = pd.read_csv('pressure_measurements.csv')
    return (p_data['Time (min)'], p_data['Pressure (kPa)'])

# function for voltage(pressure)
def p_sensor(p):
    return 9/280 * p + 0.5


def pressure_1():
    x, y = pressure()

    plt.title("Observed CanSat Pressure")
    plt.xlabel("Time [min]")
    plt.ylabel("Pressure [kPa]")

    plt.grid(True)
    plt.plot(x, y)
    plt.show()


def pressure_2():
    x = np.linspace(0, 140, 10000)
    y = p_sensor(x)

    plt.title("Pressure Sensor Behavior")
    plt.xlabel("Pressure [kPa]")
    plt.ylabel("Voltage [V]")

    plt.grid(True)
    plt.plot(x, y)
    plt.show()


def pressure_3():
    x, y = pressure()
    y = p_sensor(y)

    plt.title("Pressure Sensor Voltage Observed")
    plt.xlabel("Time [min]")
    plt.ylabel("Voltage [V]")

    plt.yticks(np.arange(0, 3.8, 0.25))

    plt.grid(True)
    plt.plot(x, y)
    plt.show()


def temp(): 
    p_data = pd.read_csv('temp_measurements.csv')
    return (p_data['Time (min)'], p_data['Temperature (Celsius)'])


# function for thermistor resistance(temperature)
def t_sensor(C):
    return 10000 * math.e ** (3810 * (1/(C + 273.15) - 1/298.15))


def temp_1():
    x, y = temp()

    plt.title("Observed CanSat Temperature")
    plt.xlabel("Time [min]")
    plt.ylabel("Temp [°C]")

    plt.grid(True)
    plt.plot(x, y)
    plt.show()


def temp_2():
    x = np.linspace(-60, 30, 10000)
    y = t_sensor(x)

    plt.title("Temperature Sensor Behavior")
    plt.xlabel("Temp [°C]")
    plt.ylabel("Resistance [Ω]")

    plt.grid(True)
    plt.plot(x, y)
    plt.show()


def temp_3():
    x, y = temp()
    y = t_sensor(y)
    y = 5 * (y / (y + 100000))

    plt.title("Temperature Sensor Voltage Observed")
    plt.xlabel("Time [min]")
    plt.ylabel("Voltage [V]")

    plt.yticks(np.arange(0, 5, 0.25))

    plt.grid(True)
    plt.plot(x, y)
    plt.show()


def humidity(): 
    p_data = pd.read_csv('humidity_measurements.csv')
    return (p_data['time (min)'], p_data['rel. humidity (%)'])


# function for voltage(relative humidity)
def h_sensor(RH):
    return 7/1000 * RH + 0.15


def humidity_1():
    x, y = humidity()

    plt.title("Observed CanSat Humidity")
    plt.xlabel("Time [min]")
    plt.ylabel("Relative Humidity [%]")

    plt.grid(True)
    plt.plot(x, y)
    plt.show()


def humidity_2():
    x = np.linspace(0, 100, 10000)    
    y = h_sensor(x)

    plt.title("Humidity Sensor Behavior")
    plt.xlabel("Relative Humidity [%]")
    plt.ylabel("Voltage [V]")
    
    plt.grid(True)
    plt.plot(x, y)
    plt.show()


def humidity_3():
    x, y = humidity()
    y = h_sensor(y)

    plt.title("Humidity Sensor Voltage Observed")
    plt.xlabel("Time [min]")
    plt.ylabel("Voltage [V]")

    plt.yticks(np.arange(0, 0.85, 0.05))

    plt.grid(True)
    plt.plot(x, y)
    plt.show()



if __name__ == '__main__':

    commands = [pressure_1, pressure_2, pressure_3, temp_1, temp_2, temp_3, humidity_1, humidity_2, humidity_3]
    print([command.__name__ for command in commands])
    
    while True:
        try:
            command = input(">")

            if command.lower() == 'q':
                break
                
            commands[int(command) - 1]()

        except:
            continue
