
from collections import namedtuple

myStruct = namedtuple("MyStruct", "max_x, max_y")

scl = 40

def setup():
    frameRate(4)
    size(1000, 1000, P3D)
    
    input = open("demo5.mod1").read()
    input = input.replace('\n', ' ')
    input = input.translate(None, '()')
    input = input.split(' ')
    
    coordArray = [0 for x in range(len(input) - 1)]
    
    for i in range(len(input) - 1):
        input[i] = input[i].split(',')
        coordArray[i] = Coord(input[i][0], input[i][1], input[i][2])
    #     print(str(coordArray[i].x) + "\t " + str(coordArray[i].y) + "\t " + str(coordArray[i].z))
    # print

    myStruct.max_x = max(X.x for X in coordArray)
    myStruct.max_y = max(Y.y for Y in coordArray)
    # print myStruct.max_x, myStruct.max_y

def draw():
    background(0)
    
    # drawing a grid for reference (each square is 100x100)
    rects = [[0 for x in range(0, 100)] for y in range(0, 100)]
    noFill()
    stroke(255, 50)
    for i in range(0, height):
        for j in range(0, width):
            rect(i*100, j*100, 100, 100)
    
    
    
    cols = myStruct.max_x/scl
    rows = myStruct.max_y/scl
    
    stroke(255)
    # fill(1000, 200, 6000, 80)
    noFill()
    rotateX(PI/3)
    translate(500, -300, -600)

    box(cols, rows, 40)
    
    terrain = [[0 for x in range(cols)] for y in range(rows)]
    translate(-200, -300)
    for y in range(rows/16):
        beginShape(TRIANGLE_STRIP)
        for x in range(cols/16):
            stroke(255, 75)
            fill(0, 0, 250, 60)
            # this sets the vertex points for the triangles on the surface, i.e. the density
            vertex(x*20, y*20, terrain[x][y])
            vertex(x*20, (y+1)*20, terrain[x][y+1])
        endShape()

class Coord:
    def __init__(self, tempX, tempY, tempZ):
        self.x = int(tempX)
        self.y = int(tempY)
        self.z = int(tempZ)
        
        





