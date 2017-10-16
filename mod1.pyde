
from collections import namedtuple

myStruct = namedtuple("MyStruct", "max_x, max_y")

scl = 40

def setup():
    size(1000, 1000, P3D)

    input1 = open("demo5.mod1").read()
    input1 = input1.replace('\n', ' ')
    input1 = input1.translate(None, '()')
    input1 = input1.split(' ')
    coordArray = [0 for x in range(len(input1) - 1)]
    for i in range(len(input1) - 1):
        input1[i] = input1[i].split(',')
        coordArray[i] = Coord(input1[i][0], input1[i][1], input1[i][2])
        print(str(coordArray[i].x) + "\t " + str(coordArray[i].y) + "\t " + str(coordArray[i].z))
    print

    myStruct.max_x = max(X.x for X in coordArray)
    myStruct.max_y = max(Y.y for Y in coordArray)
    print myStruct.max_x, myStruct.max_y

def draw():
    background(0)
    stroke(255)
    # fill(1000, 200, 6000, 80)
    noFill()
    rotateX(PI/2.5)
    translate(500, -300, -500)
    cols = myStruct.max_x/scl
    rows = myStruct.max_y/scl

    box(cols, rows, 50)
    terrain = [[0 for x in range(cols/scl)] for y in range(rows/scl)]
    translate(-200, -300, -100)
    for y in range(rows/scl - 1):
        beginShape(TRIANGLE_STRIP)
        for x in range(cols/scl):
            fill(0, 0, random(50, 250))
            vertex(x*scl, y*scl, terrain[x][y])
            vertex(x*scl, (y+1)*scl, terrain[x][y+1])
        endShape()


class Coord:
    def __init__(self, tempX, tempY, tempZ):
        self.x = int(tempX)
        self.y = int(tempY)
        self.z = int(tempZ)
        
        






