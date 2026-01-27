import sys
import csv
import serial 

com = "11"
# ser = serial.Serial(f"COM{com}", 115200)
import time

for com in range(0,13):
    try:
        ser = serial.Serial(f"COM{com}", 115200)
        print("Connected")
        break
    except serial.serialutil.SerialException:
        pass

if not ser:
    print("Failed to connect on COM's 0-12.")
    sys.exit()

import time
commed = True

def reconnection(com):
    commed = False
    print(f"Device connectivity failed or non-extent for COM{com}")
    while commed == False:
        time.sleep(5)
        for com in range(0,13):
            try:
                ser = serial.Serial(f"COM{com}", 115200)
                print(f"Reconnected for COM{com}")
                commed = True
                break
            except serial.serialutil.SerialException:
                pass
            if com == 12:
                print("Reconnection failed for COM's 0-12")
    return ser


while True:
    try:
        line = ser.readline().decode("utf-8", errors="ignore")

        print(line)
    except serial.serialutil.SerialException:
        ser = reconnection(com)