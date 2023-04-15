# SPDX-FileCopyrightText: 2022 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import board
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20

#  function to convert celcius to fahrenheit
def c_to_f(temp):
    temp_f = (temp * 9/5) + 32
    return temp_f

# thermometer class
class uDS18X20:
    def __init__(self, dataPin = board.GP5, units="C"):
        # keep track of units
        self.units = units

        # one-wire bus for DS18B20
        self.ow_bus = OneWireBus(dataPin)

        # scan for temp sensor
        self.scan = self.ow_bus.scan()
        self.sensors = []
        for sensor in self.scan:
            self.sensors.append(DS18X20(self.ow_bus, sensor))
        print("Sensors:", self.sensors)


    def read(self):

        T = self.sensors[0].temperature
        if self.units == "F":
            return c_to_f(T)
        else:
            return T
        
    def readAll(self):
        T = []
        for sensor in self.sensors:
            T.append(sensor.temperature)
        return T


    def log_to_file(self, fname="log.dat", dt=5):
        startTime = time.monotonic() 
        mesTime = startTime

        while True:
            try:
                currentTime = time.monotonic()
                if (mesTime + dt) >= currentTime:
                    mesTime = currentTime
                    T = self.read()
                    runTime = mesTime - startTime
                    print(runTime, T)
                    with open(fname, "a") as logFile:
                        logFile.write(f'{runTime},{T}')
                    
            except Exception:
                continue




