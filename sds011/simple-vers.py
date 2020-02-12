## Working version

## (!) When using this version the sensor remains active. 
## So sensor's lifetime will be shorter

import serial, time
from Adafruit_IO import Client


def get_pm25_pm10(ser):
    # ser = serial.Serial('/dev/ttyUSB0')

    data = []
    for index in range(0,10):
        datum = ser.read()
        data.append(datum)

    pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
    print(pmtwofive)
    return pmtwofive