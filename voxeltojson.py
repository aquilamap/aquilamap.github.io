import json

def getOffset(x1, y1, x2, y2, offsetX, offsetY):
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0:
        if dy > 0: # S
            return (offsetX, 1)
        else: # N
            return (offsetX, 0)
    else:
        direction = dy/dx
        if direction == 1:
            if dx > 0: # SE
                return (1, 1)
            else: # NW
                return (0, 0)
        elif direction == -1:
            if dx > 0: # NE
                return (1, 0)
            else: # SW
                return (0, 1)
        elif direction > 1 or direction < -1:
            if dy > 0: # S:
                return (offsetX, 1)
            else: # N
                return (offsetX, 0)
        elif direction < 1 and direction > -1:
            if dx > 0: # E
                return (1, offsetY)
            else: # W
                return (0, offsetY)
        else: # There's something wery wrong
            return (100, 100) # But at least we'll see it

f = open('way.points', 'r')
plots = []
last = "somethingthathopefullyisntthenameofthefirstwaypointorthewholethingwillcrash"
offset = (0, 0)
oldPoint = []
newPoint = []
for line in f:
    if line[0:4] == 'name':
        s = line.split(',')
        if last != s[0][5:8] or not plots:
            if plots: # fix the first point of the polygon
                newPoint = plots[-1]['positions'][0]
                offset = getOffset(oldPoint[1], oldPoint[0], newPoint[1], newPoint[0], *offset)
                plots[-1]['positions'][0][1] += offset[0]
                plots[-1]['positions'][0][0] += offset[1]
            last = s[0][5:8]
            newplot = {'name': last, 'number': last, 'positions': [], 'owner': ""}
            plots.append(newplot)
            plots[-1]['positions'].append([int(s[2][2:]), int(s[1][2:])])
            oldPoint = plots[-1]['positions'][-1]
            continue
        newPoint = [int(s[2][2:]), int(s[1][2:])]
        if newPoint == oldPoint:
            continue
        offset = getOffset(oldPoint[1], oldPoint[0], newPoint[1], newPoint[0], *offset)
        plots[-1]['positions'].append([newPoint[0], newPoint[1]])
        plots[-1]['positions'][-1][1] += offset[0]
        plots[-1]['positions'][-1][0] += offset[1]
        oldPoint = newPoint

f.close()

f = open('all-latest-plots.csv', 'r')
f.readline()

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

f.close()
f = open('plots.json', 'w')
json.dump(plots, f, separators=(',', ':'))
f.close()
