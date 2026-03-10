import csv
import os

os.chdir("UTL/Project/Artefact")

reader = csv.reader(open("OrthopteraOfIreland.csv"))

# for line in reader:
#     keys = line
#     break
# print(keys)
class container:
    """creates a container for the keys"""

    def __init__(self, reader):
        self.titles = {}
        for line in reader:
            self.keys = line
            break
        for title in self.keys:
            self.titles[title] = {}
        self.reader = reader
        self.lines = [x for x in self.reader]
    
    def irradiate(self):
        eight = [x for x in self.titles.keys()][8]
        for line in self.lines:
            if line[8] in self.titles[eight]:
                self.titles[eight][line[8]] += 1
            else:
                self.titles[eight][line[8]] = 1
        self.taxonomics = self.titles[eight]
        for key, value in self.taxonomics.items():
            print(key,value)

cleansed = container(reader)
cleansed.irradiate()