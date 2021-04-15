# TO RUN THIS CODE, INSTALL FIRST ITS DEPENDENCIES
# Run in the terminal 'pip install requirements.txt'
# When the code is running, input # 1 - 9 to view a chart
# Input q to quit the program

import sys, math
import numpy as np
import matplotlib.pyplot as plt 

plt.style.use('fivethirtyeight')


def within(num, lo, hi):
    return lo <= num and num <= hi


@np.vectorize
def pressure(t): 
    if within(t, 0, 25):
        return 100 - 3.4 * t 
    elif within(t, 25, 60):
        return 15 - 3/7 * (t - 25)
    elif within(t, 60, 85):
        return 3/5 * (t - 60)
    elif within(t, 85, 105):
        return 15 + 3/2 * (t - 85)
    elif within(t, 105, 120):
        return 45 + 11/3 * (t - 105)
    else:
        return None


def p_sensor(p):
    return 9/280 * p + 0.5


def pressure_1():
    x = np.linspace(0, 120, 10000)    
    y = pressure(x)

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
    x = np.linspace(0, 120, 10000)
    y = p_sensor(pressure(x))

    plt.title("Sensor Voltage Observed")
    plt.xlabel("Time [min]")
    plt.ylabel("Voltage [V]")

    plt.yticks(np.arange(min(y), max(y)+1, 0.2))

    plt.grid(True)
    plt.plot(x, y)
    plt.show()



@np.vectorize
def temp(t): 
    if within(t, 0, 10):
        return 20 - 7 * t 
    elif within(t, 10, 20):
        return -50
    elif within(t, 20, 40):
        return -50 + 0.5 * (t - 20)
    elif within(t, 40, 60):
        return -40 + 2 * (t - 40)
    elif within(t, 60, 95):
        return -10/7 * (t - 60)
    elif within(t, 95, 120):
        return -50 + 14/5 * (t - 95)
    else:
        return None


def t_sensor(C):
    return 10000 * math.e ** (3810 * (1/(C + 273.15) - 1/298.15))


def temp_1():
    x = np.linspace(0, 120, 10000)    
    y = temp(x)

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
    x = np.linspace(0, 120, 10000)
    y = t_sensor(temp(x))
    y = 3.7 * (y / (y + 100000))

    plt.title("Sensor Voltage Observed")
    plt.xlabel("Time [min]")
    plt.ylabel("Voltage [V]")

    plt.yticks(np.arange(min(y), max(y)+1, 0.2))

    plt.grid(True)
    plt.plot(x, y)
    plt.show()


@np.vectorize
def humidity(t): 
    if within(t, 0, 15):
        return 10 + 8/3 * t 
    elif within(t, 15, 25):
        return 50 - 5/2 * (t - 15)
    elif within(t, 25, 40):
        return 25 + 11/3 * (t - 25)
    elif within(t, 40, 60):
        return 80 - 7/2 * (t - 40)
    elif within(t, 60, 80):
        return 10 + 4 * (t - 60)
    elif within(t, 80, 95):
        return 90 - 14/3 * (t - 80)
    elif within(t, 95, 120):
        return 20 + 6/5 * (t - 95)
    else:
        return None


def h_sensor(RH):
    return 7/1000 * RH + 0.15


def humidity_1():
    x = np.linspace(0, 120, 10000)    
    y = humidity(x)

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
    x = np.linspace(0, 120, 10000)
    y = h_sensor(humidity(x))

    plt.title("Sensor Voltage Observed")
    plt.xlabel("Time [min]")
    plt.ylabel("Voltage [V]")

   # plt.yticks(np.arange(min(y), max(y)+1, 0.2))

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
