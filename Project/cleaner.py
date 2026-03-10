import json

def cleans(falsify=False):
    with open("Recieved_data.csv", "r") as file:
        handled = [x for x in file]
        filt = ""
        for x in handled:
            filt += x
        handled = filt.strip()
        handled = handled.replace(" ", "")
        while True:
            handled = handled.replace("\n", ",", 1)
            handled = handled.replace("\n", "", 1)
            if not "\n" in handled:
                break
        iter = 0
    cleanish = handled.split(",")
    lines = []
    line = []
    iter = 0
    for num in cleanish:
        line.append(float(num))
        if iter > 1:
            lines.append(line)
            line = []
            iter = 0
        else:
            iter += 1
    if falsify:
        pass
    filed = json.dumps(lines)
    with open("Cleaned_data.json", "w") as file:
        file.write(filed)
    return lines

if __name__ == "__main__":
    cleans()