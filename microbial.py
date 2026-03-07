import sys
import csv
import serial 
import os
import encodings
from model import Core

os.chdir("C:/Users/Computer Science 8/UTL/Project")

com = "11"
# ser = serial.Serial(f"COM{com}", 115200)
import time

core = Core()

ser = None

for com in range(0,25):
    try:
        ser = serial.Serial(f"COM{com}", 115200)
        print("Connected")
        break
    except serial.serialutil.SerialException:
        pass

if not ser:
    print("Failed to connect on COM's 0-24.")
    sys.exit()

import time
commed = True

def reconnection(com):
    commed = False
    print(f"Device connectivity failed or non-extent for COM{com}")
    while commed == False:
        time.sleep(5)
        for com in range(0,25):
            try:
                ser = serial.Serial(f"COM{com}", 115200)
                print(f"Reconnected for COM{com}")
                commed = True
                break
            except serial.serialutil.SerialException:
                pass
            if com == 24:
                print("Reconnection failed for COM's 0-24")
    return ser

with open("Recieved_data.csv", "w") as file:
    vis_mult = 6
    for mind in core.thinks:
        mind.clear()
    while True:
        try:
            line = ser.readline().decode("utf-8", errors="ignore")
            brecht = line.split(",")
            if "Conclusion" in str(line):
                file.close()
                print(line)
                sys.exit()
            elif line != " ":
                print(line)
                file.write(f"{line}")
                core.socratic.append(vis_mult*round(float(brecht[1])))
                core.platonic.append(vis_mult*round(float(brecht[0])))
                core.diogenic.append(vis_mult*round(float(brecht[2])*100))# multiplies risk for visual effect
                core.pulse()
        except serial.serialutil.SerialException:
            ser = reconnection(com)