
import math

############### THIS IS HOW YOU MAKE QUICK STRUCT LIKE ELEMENTS OUT OF TUPLES##########
#from collections import namedtuple

# myStruct = namedtuple("MyStruct", "max_x, max_y")

scl = 10

col = 400
row = 400
depth = 40

terrain = [[0 for x in range(col/scl + 1)] for y in range(row/scl + 1)]
smooth_terrain = [[0 for x in range(col/scl + 1)] for y in range(row/scl + 1)]
z_value = [0 for x in range(col)]

def dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

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

def x_coord(i):
    return int(coord_arr[i].x)/scl

def y_coord(i):
    return int(coord_arr[i].y)/scl

def set_terrain(coord_arr):
    for i in range(len(coord_arr)):
        terrain[x_coord(i)][y_coord(i)] = int(coord_arr[i].z)
    r = 8
    for i in range(len(coord_arr)):
        # for j in range(1):
        make_circle(x_coord(i), y_coord(i), r, int(coord_arr[i].z))
            # r += 1

# function to scale the input to fit the shape.
def scale_input(coord_arr):
    scale_factor = max(Coord.max_x, Coord.max_y, Coord.max_z) * 1.25 # I'm scaling above the max_coord by 2 to get the points off the edge.
    print "scale_factor = ", scale_factor
    print("SCALED COORDS")
    for i in range(Coord.num_coords):
        coord_arr[i].x = round(map(coord_arr[i].x, 0, scale_factor, 0, col), -1)
        coord_arr[i].y = round(map(coord_arr[i].y, 0, scale_factor, 0, row), -1)
        coord_arr[i].z = round(map(coord_arr[i].z, 0, scale_factor, 0, row), 0)
        print coord_arr[i].x, "\t", coord_arr[i].y, "\t", coord_arr[i].z
    return(coord_arr)

def setup():
    frameRate(30)
    size(col*3, row*3, P3D)
    input = take_input()
    global coord_arr # make coord_array global so I can access in draw()
    coord_arr = set_coords(input)
    coord_arr = scale_input(coord_arr)
    set_terrain(coord_arr)
    yOffset = 0
    # for y in range(3, row/scl - 2):
    #     xOffset = 0
    #     for x in range(3, col/scl - 2):
    #         terrain[x][y] = map(noise(xOffset, yOffset), 0, 1, 0, 30)
    #         xOffset += 0.08
    #     yOffset += 0.08

def draw_surface():
    translate((col / -2), (row / -2), (depth / 2))
    for y in range(row/scl):
        beginShape(TRIANGLE_STRIP)
        for x in range(col/scl + 1):
            stroke(255, 75)
            fill(0, 0, 265, 80)
            vertex(x*scl, y*scl, smooth_terrain[x][y])
            vertex(x*scl, (y+1)*scl, smooth_terrain[x][y+1])
        endShape()

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

def take_input():
    input = open("demo1.mod1").read()
    input = input.replace('\n', ' ')
    input = input.translate(None, '()')
    input = input.split(' ')
    return (input)

def set_coords(input):
    coord_arr = [0 for x in range(len(input) -1)]
    print("ACTUAL COORDS")
    for i in range(len(input) - 1):
        input[i] = input[i].split(',')
        coord_arr[i] = Coord(input[i][0], input[i][1], input[i][2])
        Coord.num_coords += 1
        print coord_arr[i].x, "\t", coord_arr[i].y, "\t", coord_arr[i].z

    print
    # sum_x = 0
    # sum_y = 0
    # sum_z = 0
    # print sum_x
    # for i in range(Coord.num_coords):
    #     sum_x += coord_arr[i].x
    #     sum_y += coord_arr[i].y
    #     sum_z += coord_arr[i].z
    # Coord.ave_x = sum_x / Coord.num_coords
    # Coord.ave_y = sum_y / Coord.num_coords
    # Coord.ave_z = sum_z / Coord.num_coords
    print Coord.ave_x, Coord.ave_y, Coord.ave_z
    Coord.max_x = max(X.x for X in coord_arr)
    Coord.max_y = max(Y.y for Y in coord_arr)
    Coord.max_z = max(Z.z for Z in coord_arr)

    return coord_arr

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
    box(col, row, depth)
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

def change_view():
    camera(Coord.eyeX, Coord.eyeY, Coord.eyeZ, Coord.centerX, Coord.centerY, Coord.centerZ, Coord.upX, Coord.upY, Coord.upZ)
    zoom()
    pan()

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

def reset():
    if keyPressed is True:
        if key == 'r':
            Coord.x = 0.3927
            Coord.y = 0
            Coord.z = 1.2395
            Coord.eyeZ = ((row*3)/2.0) / tan(PI*30.0 / 180.0)
            Coord.centerX = (col*3)/2
            Coord.centerY = (row*3)/2


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
    ave_x = 0
    ave_y = 0
    ave_z = 0
    
    def __init__(self, tempX, tempY, tempZ):
        self.x = int(tempX)
        self.y = int(tempY)
        self.z = int(tempZ)
        
    def max_coord(self, max_x, max_y, max_z):
        self.max_x = int(max_x)
        self.max_y = int(max_y)
        self.max_z = int(max_z)
    
  
        
    # def cols(self, max_x):
    #     self.cols = max_x/scl

    # def rows(self, max_y):
    #     self.rows = max_y/scl











# def set_smooth_terrain():
#     for y in range(0, row, 10):
#         for x in range(0, col, 10):
#             adjacent_sec = 0
#             section_tot = 0.0
#             if ((x/scl) - 1) > 0:
#                 section_tot += terrain_copy[((x-1)/scl)][(y/scl)]
#                 adjacent_sec += 1
#                 if ((y/scl) - 1) > 0:
#                     section_tot += terrain_copy[((x-1)/scl)][((y-1)/scl)]
#                     adjacent_sec += 1
#                 if ((y/scl) + 1) < row:
#                     section_tot += terrain_copy[((x-1)/scl)][((y+1)/scl)]
#                     adjacent_sec += 1
#             # print "adjacent_sec = ", adjacent_sec
#             # print "section_tot = ", section_tot
#             if ((x/scl) + 1) < col:
#                 section_tot += terrain_copy[((x+1)/scl)][(y/scl)]
#                 adjacent_sec += 1
#                 if ((y/scl) - 1) > 0:
#                     section_tot += terrain_copy[((x+1)/scl)][((y-1)/scl)]
#                     adjacent_sec += 1
#                 if ((y/scl) + 1) < row:
#                     section_tot += terrain_copy[((x+1)/scl)][((y+1)/scl)]
#                     adjacent_sec += 1
#             if ((y/scl) - 1) > 0:
#                 section_tot += terrain_copy[(x/scl)][((y-1)/scl)]
#                 adjacent_sec += 1
#             if ((y/scl) + 1) < row:
#                 section_tot += terrain_copy[(x/scl)][((y+1)/scl)]
#                 adjacent_sec += 1
#             print "adjacent_sec = ", adjacent_sec
#             print "section_tot = ", section_tot
#             smooth_terrain[(x/scl)][(y/scl)] = terrain_copy[(x/scl)][(y/scl)] + section_tot // adjacent_sec * 1.9
#     return smooth_terrain