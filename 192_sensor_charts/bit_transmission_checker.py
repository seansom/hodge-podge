adc_bit_resolution = 12
adc_reference_voltage = 5


def get_adc_code(Vin):
    global adc_bit_resolution, adc_reference_voltage
    return round((Vin / adc_reference_voltage) * (2 ** adc_bit_resolution))


def get_voltage(code):
    global adc_bit_resolution, adc_reference_voltage
    return (code * adc_reference_voltage) / (2 ** adc_bit_resolution)


def main():
    print([7.3, 8.8])
    print(get_voltage(0b111001100101) / 1.2)
    print(get_voltage(0b000111011010))
    print(get_voltage(0b010001011011) / 6)

    print("===")    

    print([127.5, 129.2])
    print(get_voltage(0b110110101010) / 1.2)
    print(get_voltage(0b001100111001))
    print(get_voltage(0b010100010011) / 6)

    print("===")    

    print([677.3, 679.2])
    print(get_voltage(0b101000100001) / 1.2)
    print(get_voltage(0b111000010111))
    print(get_voltage(0b100001011011) / 6)


if __name__ == '__main__':
    main()