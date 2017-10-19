

############### THIS IS HOW YOU MAKE QUICK STRUCT LIKE ELEMENTS OUT OF TUPLES##########
#from collections import namedtuple

# myStruct = namedtuple("MyStruct", "max_x, max_y")

scl = 30

def setup():
    frameRate(30)
    size(1000, 1000, P3D)
    input = take_input()
    set_coords(input)
    
    print(Coord.max_x)
    print(Coord.max_y)

def draw():
    background(0)
    stroke(255)
    noFill()
    #draw grid for reference
    # draw_grid()
    # camera(width/2, height*2, (height/2.0) / tan(PI*30.0 / 180.0), width/2.0, height/2.0, 0, 0, 1, 0)
    translate(width/2, height/2 + 100)
    rotateX(Coord.i % 2*PI)
    rotateY(Coord.j % 2*PI)
    # rotateZ(Coord.i % PI/2)
    pushMatrix()
    if keyPressed is True:
        if key == CODED:
            if keyCode == UP:
                Coord.i += PI/256
            elif keyCode == DOWN:
                Coord.i -= PI/256
            elif keyCode == LEFT:
                Coord.j -= PI/256
            elif keyCode == RIGHT:
                Coord.j += PI/256
        elif key == 'r' or 'R':
            resetMatrix()
    draw_box()
    draw_surface()
    popMatrix()


    
    

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

def draw_grid():
    pushMatrix()
    # stroke(255, 50)
    # noFill()
    for i in range(0, height):
        for j in range(0, width):
            rect(i*100, j*100, 100, 100)
    popMatrix()

def draw_box():
    stroke(0, 140, 0)
    fill(0, 165, 0, 80)
    pushMatrix()
    box(Coord.x, Coord.y, Coord.z)
    popMatrix()

def draw_surface():
    translate((Coord.x / -2), (Coord.y / -2), (Coord.z / 2))
    for y in range(height/50):
        beginShape(TRIANGLE_STRIP)
        for x in range(width/50 + 1):
            stroke(255, 75)
            fill(0, 165, 0, 80)
            # this sets the vertex points for the triangles on the surface, i.e. the density
            vertex(x*20, y*20)
            vertex(x*20, (y+1)*20)
        endShape()

class Coord(object):
    
    i = 0
    j = 0
    x = 400
    y = 400
    z = 150
    
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
       

        