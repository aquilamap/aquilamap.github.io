import json
import getpass
import sys
from optparse import OptionParser

def get_options():
    parser = OptionParser()

    parser.add_option("-f", "--inputjson", dest="input", default="plots.json", help="input plots file")
    parser.add_option("-o", "--outputjson", dest="output", default="plots.json", help="output plots file")
    parser.add_option("-p", "--properties", dest="properties", default="plots-info.csv", help="additional properties file")
    parser.add_option("-c", "--owners", dest="owners", default=None, help="csv file with owners and coords of their house")
    parser.add_option("-i", "--interactive", action="store_true", dest="interactive", default=False, help="interactive mode")
    
    (options, args) = parser.parse_args()
    return options

def interactiveMode(inputFile, outputFile):
    print("Entering interactive mode.")
    print("Ctrl+c to exit")
    file = open(inputFile, "r")
    plots = json.load(file)
    file.close()

    while True:
        try:
            text = input("Paste JSON data:")
            indata = json.loads(text)
            found = False
            for plot in plots:
                if plot['number'] == indata['number']:
                    plot.update(indata)
                    found = True
                    break
            if not found:
                plots.append(indata)
        except KeyboardInterrupt:
            print("Saving plot file...")
            file = open(outputFile, "w")
            json.dump(plots, file, separators=(',', ':'))
            file.close()
            print(outputFile, "saved!")
            sys.exit()
        except:
            print("Error, incorrect JSON data")

def ownersMatch(plots, ownersFile):
    f = open(ownersFile, "r")
    for line in f:
        stuff = line.split(',')
        owner = stuff[0]
        x = int(stuff[2])
        y = int(stuff[1])
        for plot in plots:
            poly = plot['positions']
            num = len(poly)
            i = 0
            j = num - 1
            c = False
            for i in range(num):
                if  ((poly[i][1] > y) != (poly[j][1] > y)) and \
                        (x < (poly[j][0] - poly[i][0]) * (y - poly[i][1]) / (poly[j][1] - poly[i][1]) + poly[i][0]):
                    c = not c
                j = i
            if c:
                plot['owner'] = owner
                break
        if c:
            continue

def getColor(zone, empty):
    if zone == "government":
        return "#ff0000"
    elif zone == "residential":
        if empty == "yes":
            return "#bbffff"
        else:
            return "#00ffff"
    elif zone == "highend":
        if empty == "yes":
            return "#ffffbb"
        else:
            return "#ffff00"
    elif zone == "downtown":
        if empty == "yes":
            return "#bbffbb"
        else:
            return "#00ff00"
    elif zone == "highrise":
        if empty == "yes":
            return "#bbd7ff"
        else:
            return "#0000ff"
    else:
        return "#ffffff"

def updateInfo(plots, infoFile):
    f = open(infoFile, 'r')
    lines = f.read().splitlines()
    if len(lines) == 0:
        return
    header = lines[0].split(",")
    del lines[0]
        
    for line in lines:
        props = line.split(",")
        newDic = {}
        for i in range(len(header)):
            if props[i]:
                newDic.update({header[i]:props[i]})
        
        for plot in plots:
            if plot["number"] == newDic["number"]:
                plot.update(newDic)
                if newDic.get("zone") or newDic.get("empty"):
                    plot.update({"color":getColor(newDic["zone"], plot.get("open", "no"))})

def main():
    options = get_options()
    
    if options.interactive:
        interactiveMode(options.input, options.output)
    else:
        file = open(options.input, "r")
        plots = json.load(file)
        file.close()

        updateInfo(plots, options.properties)

        if options.owners: # This is optional, so it has priority over plots-info.csv, i.e. owners from this file will override any existing owners
            ownersMatch(plots, options.owners)

        file = open(options.output, "w")
        json.dump(plots, file, separators=(',', ':'))
        file.close()
        print(options.output, "saved!")
        
if __name__ == "__main__":
    main()
