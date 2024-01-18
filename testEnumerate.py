# Saw some code online, wanted to use it, so I figured it out before I just shoved it into my code

mapFile = open("map.txt", "r")
mapData = []

i = 0
for row in mapFile.read().split("\n"):
    rowArray = []
    print(row)
    for char in row:
        rowArray.append(int(char))

    mapData.insert(i, rowArray)
    i += 1

for y, row in enumerate(mapData):
    for x, tile in enumerate(row):
        pass
        # print(y)
        # print(row)

        # print(x)
        # print(tile)

print(list(enumerate(mapData)))