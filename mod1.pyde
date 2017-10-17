

############### THIS IS HOW YOU MAKE QUICK STRUCT LIKE ELEMENTS OUT OF TUPLES##########
#from collections import namedtuple

# myStruct = namedtuple("MyStruct", "max_x, max_y")

scl = 30

def setup():
    frameRate(4)
    size(1000, 1000, P3D)
    input = take_input()
    set_coords(input)

def draw():
    background(0)
    stroke(255)
    noFill()
    #draw grid for reference
    draw_grid()
    #draw 3D box
    draw_box()
    draw_surface()

def take_input():
    input = open("demo1.mod1").read()
    input = input.replace('\n', ' ')
    input = input.translate(None, '()')
    input = input.split(' ')
    return (input)

def set_coords(input):
    coord_arr = [0 for x in range(len(input) -1)]
    for i in range(len(input) - 1):
        input[i] = input[i].split(',')
        coord_arr[i] = Coord(input[i][0], input[i][1], input[i][2])

    Coord.max_x = max(X.x for X in coord_arr)
    Coord.max_y = max(Y.y for Y in coord_arr)

def draw_box():
    cols = Coord.max_x/scl
    rows = Coord.max_y/scl
    
    stroke(255, 140, 0)
    fill(255, 165, 0, 80)
    pushMatrix()
    translate(width/2, height/2)
    rotateX(PI/3)
    box(cols, rows, rows/3)
    popMatrix()

def draw_surface():
    cols = Coord.max_x/scl
    rows = Coord.max_y/scl

    translate(width/2 - cols/2, height/2 - rows/2, 0)
    rotateX(PI/3)
    for y in range(rows/20):
        beginShape(TRIANGLE_STRIP)
        for x in range(cols/18):
            stroke(255, 75)
            fill(0, 0, 250, 60)
            # this sets the vertex points for the triangles on the surface, i.e. the density
            vertex(x*20, y*20)
            vertex(x*20, (y+1)*20)
        endShape()

def draw_grid():
    pushMatrix()
    # stroke(255, 50)
    # noFill()
    for i in range(0, height):
        for j in range(0, width):
            rect(i*100, j*100, 100, 100)
    popMatrix()

class Coord(object):
    def __init__(self, tempX, tempY, tempZ):
        self.x = int(tempX)
        self.y = int(tempY)
        self.z = int(tempZ)
        
    def max_coord(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        
    # def cols(self, max_x):
    #     self.cols = max_x/scl

    # def rows(self, max_y):
    #     self.rows = max_y/scl
       

        

