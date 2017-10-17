

############### THIS IS HOW YOU MAKE QUICK STRUCT LIKE ELEMENTS OUT OF TUPLES##########
#from collections import namedtuple

# myStruct = namedtuple("MyStruct", "max_x, max_y")

scl = 50

def setup():
    frameRate(4)
    size(1000, 1000, P3D)
    input = take_input()
    
    coordArray = [0 for x in range(len(input) - 1)]
    
    for i in range(len(input) - 1):
        input[i] = input[i].split(',')
        coordArray[i] = Coord(input[i][0], input[i][1], input[i][2])
    #     print(str(coordArray[i].x) + "\t " + str(coordArray[i].y) + "\t " + str(coordArray[i].z))
    # print

    max_xy.max_x = max(X.x for X in coordArray)
    max_xy.max_y = max(Y.y for Y in coordArray)

def take_input():
    input = open("demo1.mod1").read()
    input = input.replace('\n', ' ')
    input = input.translate(None, '()')
    input = input.split(' ')
    return (input)

def draw():
    background(0)
    
    # drawing a grid for reference (each square is 100x100)
    noFill()
    stroke(255, 50)
    rects = gridlines(height, width)
    # gridlines.make_grid(rects) #identical to below.
    rects.make_grid() #identical to above.

    cols = max_xy.max_x/scl
    rows = max_xy.max_y/scl
    
    stroke(255)
    # fill(1000, 200, 6000, 80)
    noFill()
    # rotateX(.7)
    # rotateZ(-.5)
    # rotateY(1)
    #first parameter moves -left +right, second parameter moves -up +down, third parameter moves -away +towards
    pushMatrix()
    translate(cols + cols/2, cols + cols/2)

    # the origin of the box is in the middle.
    box(cols, rows, rows/2)
    popMatrix()
    
    ##################
    #NEED TO COME UP WITH A WAY TO BIND THE SURFACE TO THE BOX
    
    # terrain = [[0 for x in range(cols)] for y in range(rows)]
    translate(rows, cols, rows/4)
    for y in range(rows/20):
        beginShape(TRIANGLE_STRIP)
        for x in range(cols/18):
            stroke(255, 75)
            fill(0, 0, 250, 60)
            # this sets the vertex points for the triangles on the surface, i.e. the density
            vertex(x*20, y*20)
            vertex(x*20, (y+1)*20)
        endShape()

class gridlines:
    def __init__(self, grid_height, grid_width):
        self.grid_height = grid_height
        self.grid_width = grid_width
      
    def make_grid(self):
        for i in range(0, self.grid_height):
            for j in range(0, self.grid_width):
                rect(i*10, j*10, 10, 10)

class Coord:
    def __init__(self, tempX, tempY, tempZ):
        self.x = int(tempX)
        self.y = int(tempY)
        self.z = int(tempZ)
        
class max_xy:
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        



