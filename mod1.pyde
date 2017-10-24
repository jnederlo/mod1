
import math

##############################################################################
############################## GLOBAL VARIABLES ##############################
##############################################################################
scl = 10

col = 400
row = 400
depth = 40

file_name = None

terrain = [[0 for x in range(col/scl + 1)] for y in range(row/scl + 1)]
smooth_terrain = [[0 for x in range(col/scl + 1)] for y in range(row/scl + 1)]
z_value = [0 for x in range(col)]

##############################################################################
#################################### SETUP ###################################
##############################################################################
def setup():
    # selectInput("Select a file to process:", "fileSelected")
    frameRate(30)
    size(col*3, row*3, P3D)
    # while file_name is None:
    #     print "waiting..."
    input = take_input()
    global coord_arr # make coord_array global so I can access in draw()
    coord_arr = set_coords(input)
    coord_arr = scale_input(coord_arr)
    set_terrain(coord_arr)

##############################################################################
#################################### DRAW ####################################
##############################################################################
def draw():
    background(0)
    stroke(255)
    noFill()
    #draw grid for reference
    # draw_grid()
    change_view()
    translate(width/2, height/2 + 100)
    rotate_shape()
    reset()
    draw_box()
    draw_surface()

##################################
######### TAKE_INPUT #############
##################################
def take_input():
    input = open("demo5.mod1").read()
    input = input.replace('\n', ' ')
    input = input.translate(None, '()')
    input = input.split(' ')
    return (input)

##################################
######### SET_COORDS #############
##################################
def set_coords(input):
    coord_arr = [0 for x in range(len(input) -1)]
    print("ACTUAL COORDS")
    for i in range(len(input) - 1):
        input[i] = input[i].split(',')
        coord_arr[i] = Coord(input[i][0], input[i][1], input[i][2])
        Coord.num_coords += 1
        print coord_arr[i].x, "\t", coord_arr[i].y, "\t", coord_arr[i].z

    Coord.min_x = min(X.x for X in coord_arr)
    Coord.min_y = min(Y.y for Y in coord_arr)
    Coord.min_z = min(Z.z for Z in coord_arr)
    Coord.max_x = max(X.x for X in coord_arr)
    Coord.max_y = max(Y.y for Y in coord_arr)
    Coord.max_z = max(Z.z for Z in coord_arr)

    return coord_arr

##################################
######### SCALE_INPUT ############
##################################
def scale_input(coord_arr):
    # scale_z = max(Coord.max_x, Coord.max_y)
    scale_x = Coord.min_x + Coord.max_x
    scale_y = Coord.min_y + Coord.max_y
    if scale_y > scale_x:
        scale_z = scale_y
    else:
        scale_z = scale_x
    # scale_y = scale_x
    print "scale_x,y,z = ", scale_x, scale_y, scale_z
    print("SCALED COORDS")
    for i in range(Coord.num_coords):
        coord_arr[i].x = round(map(coord_arr[i].x, 0, scale_x, 0, col), -1)
        coord_arr[i].y = round(map(coord_arr[i].y, 0, scale_y, 0, row), -1)
        coord_arr[i].z = round(map(coord_arr[i].z, 0, scale_z, 0, row), 0)
        print coord_arr[i].x, "\t", coord_arr[i].y, "\t", coord_arr[i].z
    return(coord_arr)

##################################
######### SET_TERRAIN ############
##################################
def set_terrain(coord_arr):
    for i in range(len(coord_arr)):
        terrain[x_coord(i)][y_coord(i)] = int(coord_arr[i].z)
    r = 9
    for i in range(len(coord_arr)):
        make_circle(x_coord(i), y_coord(i), r, int(coord_arr[i].z))
    x_offset = 0
    for x in range(1, row/scl):
        y_offset = 0
        for y in range(1, col/scl):
            smooth_terrain[x][y] = smooth_terrain[x][y] + map(noise(y_offset, x_offset), 0, 1, 0, 5)
            y_offset += 1
        x_offset += 1

##################################
######### SET_TERRAIN ############
##################################
def make_circle(cx, cy, r, z):
    for x in range(cx - r, cx + r):
        for y in range(cy - r, cy + r):
            z_dist = dist(cx, cy, x, y)
            z_new = (((cos(z_dist/3)+1)/PI)*z) #change the z_dist divisor to influence and tweak
            # z_new = (z_dist ** (1/3)) / (z + 1)
            # print "z_dist = ", z_dist
            if z_dist <= r:
                if z_new > smooth_terrain[x][y]:
                    # print "z_new = ", z_new
                    smooth_terrain[x][y] = z_new

##################################
######### CHANGE_VIEW ############
##################################
def change_view():
    camera(Coord.eyeX, Coord.eyeY, Coord.eyeZ, Coord.centerX, Coord.centerY, Coord.centerZ, Coord.upX, Coord.upY, Coord.upZ)
    zoom()
    pan()

##################################
######### ROTATE SHAPE ###########
##################################
def rotate_shape():
    rotateX(Coord.x % 2*PI)
    rotateY(Coord.y % 2*PI)
    rotateZ(Coord.z % 2*PI)
    if keyPressed is True:
        if key == CODED:
            if keyCode == UP:
                Coord.x += PI/256
            if keyCode == DOWN:
                Coord.x -= PI/256
            if keyCode == LEFT:
                Coord.y -= PI/256
            if keyCode == RIGHT:
                Coord.y += PI/256
        if key == 'z':
            Coord.z -= PI/256
        if key == 'x':
            Coord.z += PI/256

##################################
######### RESET ##################
##################################
def reset():
    if keyPressed is True:
        if key == 'r':
            Coord.x = 0.3927
            Coord.y = 0
            Coord.z = 1.2395
            Coord.eyeZ = ((row*3)/2.0) / tan(PI*30.0 / 180.0)
            Coord.centerX = (col*3)/2
            Coord.centerY = (row*3)/2

##################################
######### DRAW_BOX ###############
##################################
def draw_box():
    stroke(0, 140, 0)
    fill(0, 165, 0, 80)
    pushMatrix()
    box(col, row, depth)
    popMatrix()

##################################
######### DRAW_SURFACE ###########
##################################
def draw_surface():
    translate((col / -2), (row / -2), (depth / 2))
    for y in range(row/scl):
        beginShape(TRIANGLE_STRIP)
        for x in range(col/scl + 1):
            stroke(45, 80)
            noStroke()
            fill(color_red(x, y), color_green(x, y), color_blue(x, y))
            vertex(x*scl, y*scl, smooth_terrain[x][y])
            fill(color_red(x, y + 1), color_green(x, y + 1), color_blue(x, y + 1))
            vertex(x*scl, (y+1)*scl, smooth_terrain[x][y+1])
        endShape()






###################################
######### UTILITY FUNCTIONS #######
###################################
def dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def x_coord(i):
    return int(coord_arr[i].x)/scl

def y_coord(i):
    return int(coord_arr[i].y)/scl

def fileSelected(selection):
    if selection == None:
        print("Window was closed or the user hit cancel.")
    else:
        print("User selected" + selection.getAbsolutePath())
    file_name = selection
    print type(selection)
    
def color_red(x, y):
    return map(smooth_terrain[x][y], 0, 50, 30, 225)

def color_green(x, y):
    return map(smooth_terrain[x][y], 0, 50, 100, 160)

def color_blue(x, y):
    return map(smooth_terrain[x][y], 10, 50, 30, 90)

def draw_grid():
    pushMatrix()
    # stroke(255, 50)
    # noFill()
    for i in range(0, height):
        for j in range(0, width):
            rect(i*100, j*100, 100, 100)
    popMatrix()

def zoom():
    if keyPressed is True:
        if key == '-':
            Coord.eyeZ += 10
        if key == '+':
            Coord.eyeZ -= 10

def pan():
    if keyPressed is True:
        if key == 'a':
            Coord.centerX += 10
        if key == 'd':
            Coord.centerX -= 10
        if key == 'w':
            Coord.centerY += 10
        if key == 's':
            Coord.centerY -= 10

class Coord(object):
    
    x = 0.3927
    y = 0
    z = 1.2395
    
    num_coords = 0
    
    # camera variables at default settings
    eyeX = (col*3)/2
    eyeY = (row*3)/2
    eyeZ = ((row*3)/2.0) / tan(PI*30.0 / 180.0)
    centerX = (col*3)/2
    centerY = (row*3)/2
    centerZ = 0
    upX = 0
    upY = 1
    upZ = 0
    min_x = 0
    min_y = 0
    min_z = 0
    max_x = 0
    max_y = 0
    max_z = 0
    
    def __init__(self, tempX, tempY, tempZ):
        self.x = int(tempX)
        self.y = int(tempY)
        self.z = int(tempZ)
