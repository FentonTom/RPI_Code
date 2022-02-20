# Modified by TJF from code from 
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# This will output Tempature a humidity  only once in text and JSON format
# Output formated for Edge DX

import time
import datetime
import board
import adafruit_dht
import json

# Initial the dht device, with data pin connected to:
## dhtDevice = adafruit_dht.DHT22(board.D18)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

KeepGoing = True
while KeepGoing:
    try:
        # Print the values to the serial port
        KeepGoing = False
        temperature_c = dhtDevice.temperature
        temperature_f = round(temperature_c * (9 / 5) + 32)
        humidity = dhtDevice.humidity
        now = datetime.datetime.now()

        # a Python object (dict):
        x = {
          "TempC": temperature_c,
          "TempF": temperature_f,
          "Hum": dhtDevice.humidity,
       }

# convert into JSON:
        y = json.dumps(x)

# the result is a JSON string:
        print("### SIP DATA BEGINS ###")
        print(y)
        print("### SIP DATA ENDS ###")



        print("### SIP EVENT BEGINS ###")
        print(now.strftime("%Y-%m-%d %H:%M:%S   "), end='')
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )
        print("### SIP EVENT ENDS ###")

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        KeepGoing = True
##        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)
