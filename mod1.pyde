
import math

##############################################################################
############################## GLOBAL VARIABLES ##############################
##############################################################################
scl = 8

col = 400
row = 400
depth = 40

file_name = None

terrain = [[0 for x in range(col/scl + 1)] for y in range(row/scl + 1)]

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
    pick_mode()
    rotate_shape()
    reset()
    draw_box()
    if Env.mode == 0 or Env.mode == 1:
        draw_surface()
        draw_water()
        draw_water_low()
        draw_sides()
        update_env()
    elif Env.mode == 2:
        draw_surface()
        draw_water()
        draw_sides()
        update_env()
    elif Env.mode == 3:
        draw_surface()
        draw_wave()
        draw_sides()
        update_env()
    # smooth_colors()
    # noLoop()

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
    global smooth_terrain
    smooth_terrain = [[0 for x in range(col/scl + 1)] for y in range(row/scl + 1)]
    for y in range(row/scl+1):
        for x in range(col/scl+1):
            smooth_terrain[x][y] = My_vertex(x, y, 0)
    r = 9
    for i in range(len(coord_arr)):
        make_circle(x_coord(i), y_coord(i), r, int(coord_arr[i].z))
    gradient()
    x_offset = 0
    for x in range(1, row/scl):
        y_offset = 0
        for y in range(1, col/scl):
            smooth_terrain[x][y].z = smooth_terrain[x][y].z + map(noise(y_offset, x_offset), 0, 1, 0, 10)
            y_offset += 1
        x_offset += 1
    global water_terrain
    water_terrain = [[0 for x in range(col/scl + 1)] for y in range(row/scl + 1)]
    r = 9
    for y in range(row/scl+1):
        for x in range(col/scl+1):
            water_terrain[x][y] = 0
    for water in water_arr:
        make_water_circle(water.x, water.y, r, int(water.stop_z)) 

def make_water_circle(cx, cy, r, z):
    for x in range(cx - r, cx + r):
        for y in range(cy - r, cy + r):
            z_dist = dist(cx, cy, x, y)
            # print z_dist
            z_dif = Water.water_max / 2
            z_new = (((cos(z_dist/2)+1)/PI)*z) + z_dif #change the z_dist divisor to influence and tweak
            # z_new = (z_dist ** (1/3)) / (z + 1)
            # print "z_dist = ", z_dist
            if z_dist <= r:
                # if z_dist == 0:
                #     print "z_new = ", z_new
                if z_new > water_terrain[x][y]:
                    # print "z_new = ", z_new
                    water_terrain[x][y] = z_new
                
def gradient():
    for y in range(5, row/scl - 5):
        for x in range(5, col/scl - 5):
            if smooth_terrain[x-1][y].z < smooth_terrain[x][y].z * 1.05:
                smooth_terrain[x][y].set_grade(smooth_terrain[x-1][y])
            if smooth_terrain[x+1][y].z < smooth_terrain[x][y].z * 1.05:
                smooth_terrain[x][y].set_grade(smooth_terrain[x+1][y])
            if smooth_terrain[x][y+1].z < smooth_terrain[x][y].z * 1.05:
                smooth_terrain[x][y].set_grade(smooth_terrain[x][y+1])
            if smooth_terrain[x][y-1].z < smooth_terrain[x][y].z * 1.05:
                smooth_terrain[x][y].set_grade(smooth_terrain[x][y-1])
            if smooth_terrain[x][y].grade == None:
                pass
            else:
                pass
                 # print "Lower", smooth_terrain[x][y].grade.x, smooth_terrain[x][y].grade.y, smooth_terrain[x][y].grade.z
                 # print "Actual", smooth_terrain[x][y].x, smooth_terrain[x][y].y, smooth_terrain[x][y].z
                 # print 
                 
    # for i in range(Coord.num_coords):
        # print "Actual", smooth_terrain[int(coord_arr[i].x)/scl][int(coord_arr[i].y)/scl].x, smooth_terrain[int(coord_arr[i].x)/scl][int(coord_arr[i].y)/scl].y
        # print "Lower", smooth_terrain[int(coord_arr[i].x)/scl][int(coord_arr[i].y)/scl].grade.x, smooth_terrain[int(coord_arr[i].x)/scl][int(coord_arr[i].y)/scl].grade.y
        # print
    edge_x = col/scl
    edge_y = row/scl
    for y in range(5, row/scl - 5):
        for x in range(5, col/scl - 5):
            if smooth_terrain[x][y].grade == None:
                if (smooth_terrain[x][y].x <= edge_x*.15 or smooth_terrain[x][y].y >= edge_y*.85):
                    continue
                if (smooth_terrain[x][y].x >= edge_x*.85 or smooth_terrain[x][y].y <= edge_y*.15):
                    continue
                My_vertex.low_points.append(smooth_terrain[x][y])
                # print "found low point"
                # print smooth_terrain[x][y].x, smooth_terrain[x][y].y
                # print
            else:
                continue
    
    
    global water_arr
    water_arr = [0 for x in range(len(My_vertex.low_points))]
    i = 0
    for low in My_vertex.low_points:
        x1 = 1
        x2 = 1
        # print "low x", low.x, "low y", low.y, "low z", low.z
        current = smooth_terrain[low.x][low.y]
        while smooth_terrain[low.x-x1][low.y].grade == current:
            current = smooth_terrain[current.x-x1][current.y]
            x1 += 1
        z = smooth_terrain[(current.x-x1)+1][current.y].z
        # print "z = ", z
        # print "current.z = ", current.z
        # print
        z = min(current.z, z)
        current = smooth_terrain[low.x][low.y]
        while smooth_terrain[low.x+x2][low.y].grade == current:
            current = smooth_terrain[current.x+x2][current.y]
            x2 += 1
        y1 = 1
        y2 = 1
        z = smooth_terrain[(current.x+x2)-1][current.y].z
        # print "z = ", z
        # print "current.z = ", current.z
        # print
        z = min(current.z, z)
        current = smooth_terrain[low.x][low.y]
        while smooth_terrain[low.x][low.y-y1].grade == current:
            current = smooth_terrain[current.x][current.y-y1]
            y1 += 1
        z = smooth_terrain[current.x][(current.y-y1)+1].z
        # print "z = ", z
        # print "current.z = ", current.z
        # print
        z = min(current.z, z)
        current = smooth_terrain[low.x][low.y]
        while smooth_terrain[low.x][low.y+y2].grade == current:
            current = smooth_terrain[current.x][current.y+y2]
            y2 += 1
            
        z = smooth_terrain[current.x][(current.y+y2)-1].z
        # print "z = ", z
        # print "current.z = ", current.z
        # print
        z = min(current.z, z)
        # print "z = ", z
        Water.water_max = max(Water.water_max, z)
        water_arr[i] = Water_shape(low.x, low.y, (x1 + x2), (y1 + y2), low.z, z)
        # print "orig = ", water_arr[i].x, water_arr[i].y, "\nw = ", water_arr[i].w, "h = ", water_arr[i].h
        # print
        i += 1
        
    # print "low", My_vertex.low_points
            
##################################
######### MAKE_CIRCLE ############
##################################
def make_circle(cx, cy, r, z):
    for x in range(cx - r, cx + r):
        for y in range(cy - r, cy + r):
            z_dist = dist(cx, cy, x, y)
            # print z_dist
            z_new = (((cos(z_dist/3)+1)/PI)*z) #change the z_dist divisor to influence and tweak
            # z_new = (z_dist ** (1/3)) / (z + 1)
            # print "z_dist = ", z_dist
            if z_dist <= r:
                # if z_dist == 0:
                #     print "z_new = ", z_new
                if z_new > smooth_terrain[x][y].z:
                    # print "z_new = ", z_new
                    smooth_terrain[x][y].z = z_new 
    
##################################
######### CHANGE_VIEW ############
##################################
def change_view():
    camera(Env.eyeX, Env.eyeY, Env.eyeZ, Env.centerX, Env.centerY, Env.centerZ, Env.upX, Env.upY, Env.upZ)
    zoom()
    pan()

##################################
######### ROTATE SHAPE ###########
##################################
def rotate_shape():
    rotateX(Env.x % 2*PI)
    rotateY(Env.y % 2*PI)
    rotateZ(Env.z % 2*PI)
    if keyPressed is True:
        if key == CODED:
            if keyCode == UP:
                Env.x += PI/256
            if keyCode == DOWN:
                Env.x -= PI/256
            if keyCode == LEFT:
                Env.y -= PI/256
            if keyCode == RIGHT:
                Env.y += PI/256
        if key == 'z':
            Env.z -= PI/256
        if key == 'x':
            Env.z += PI/256

##################################
######### RESET ##################
##################################
def reset():
    if keyPressed is True:
        if key == 'r':
            Env.x = 0.3927
            Env.y = 0
            Env.z = 1.2395
            Env.eyeZ = ((row*3)/2.0) / tan(PI*30.0 / 180.0)
            Env.centerX = (col*3)/2
            Env.centerY = (row*3)/2
        elif key == 't':
            Water.water_rate = 0
            Water.water_level = 0

def pick_mode():
    if keyPressed is True:
        if key == ' ':
            Env.freeze = not Env.freeze
        elif key == '1':
            reset_env()
            Env.mode = 1
        elif key == '2':
            reset_env()
            Env.mode = 2
        elif key == '3':
            reset_env()
            Env.mode = 3
        elif key == 'f':
            Env.water_flush = not Env.water_flush
            

##################################
######### DRAW_BOX ###############
##################################
def draw_box():
    stroke(0, 140, 0)
    noStroke()
    fill(0, 100, 200)
    pushMatrix()
    box(col, row, depth)
    popMatrix()

##################################
######### DRAW_SURFACE ###########
##################################
def draw_surface():
    pushMatrix()
    translate((col / -2), (row / -2), (depth / 2))
    for y in range(row/scl):
        beginShape(TRIANGLE_STRIP)
        for x in range(col/scl + 1):
            stroke(45, 80)
            noStroke()
            fill(color_red(smooth_terrain[x][y].z), color_green(smooth_terrain[x][y].z), color_blue(smooth_terrain[x][y].z))
            vertex(x*scl, y*scl, smooth_terrain[x][y].z)
            fill(color_red(smooth_terrain[x][y+1].z), color_green(smooth_terrain[x][y+1].z), color_blue(smooth_terrain[x][y+1].z))
            vertex(x*scl, (y+1)*scl, smooth_terrain[x][y+1].z)
        endShape()
    popMatrix()

##################################
######### DRAW_WATER #############
##################################
def draw_water():
    translate((col / -2), (row / -2), (depth / 2))
    #TRYING TO ADD WAVE
    # translate((col / -2), (row / -2), (depth / -2)) # I changed the depth to divide by -2 instead of 2
    # rotateX(Water.x % PI) # I added a rotate to make it appear it's coming from one side.
    # Water.x += PI/5000 # I increase the rotate slowly.
    pushMatrix()
    for y in range(row/scl):
        beginShape(TRIANGLE_STRIP)
        for x in range(col/scl + 1):
            noStroke()
            fill(0, 100, 200, 100)
            # fill(color_red(x, y), color_green(x, y), color_blue(x, y))
            # fill(0, 100, 200, 200)
            vertex(x*scl, y*scl, Water.water_level)
            # fill(color_red(x, y + 1), color_green(x, y + 1), color_blue(x, y + 1))
            vertex(x*scl, (y+1)*scl, Water.water_level)
        endShape()
    popMatrix()

def draw_wave():
    translate((col / -2), (row / -2), (depth / 2))
    #TRYING TO ADD WAVE
    # translate((col / -2), (row / -2), (depth / -2)) # I changed the depth to divide by -2 instead of 2
    # rotateX(Water.x % PI) # I added a rotate to make it appear it's coming from one side.
    # Water.x += PI/5000 # I increase the rotate slowly.
    
    pushMatrix()
    yoff = 0
    for y in range(row/scl):
        beginShape(TRIANGLE_STRIP)
        xoff = 0
        for x in range(col/scl + 1):
            noStroke()
            fill(0, 100, 200, 100)
            # if x == wave:
                # map(noise(y_offset, x_offset), 0, 1, 0, 10)
            vertex(x*scl, y*scl, Water.water_level + map(noise(xoff), 0, 1, 0, 5))
            vertex(x*scl, (y+1)*scl, Water.water_level + map(noise(yoff), 0, 1, 0, 5))
            # else:
            #     vertex(x*scl, y*scl, Water.water_level)
            #     vertex(x*scl, (y+1)*scl, Water.water_level)
            xoff += 0.05
        endShape()
        yoff += 0.01
    popMatrix()

def draw_water_low():    
    if len(coord_arr) > 10:
        pushMatrix()
        for y in range(10, row/scl - 10):
            beginShape(TRIANGLE_STRIP)
            for x in range(10, col/scl - 9):
                # stroke(255, 255, 255)
                fill(0, 100, 200, 100)
                noStroke()
                # fill(0, 100, 200)
                # flag = False
                # for water in water_arr:
                #     if water.x == x and water.y == y:
                #         flag = True
                #         vertex(x*scl, y*scl, (water.stop_z - 0.04))
                #         vertex(x*scl, (y+1)*scl, (water.stop_z - 0.04))
                #         break
                # if flag is False:
                vertex(x*scl, y*scl, (water_terrain[x][y] - 15) + Water.water_rate)
                vertex(x*scl, (y+1)*scl, (water_terrain[x][y+1] - 15) + Water.water_rate)
            endShape()
        popMatrix()
    
    # for water in water_arr:
    #     pushMatrix()
    #     # fill(0, 100, 200)
    #     print water.z
    #     print "water.z = ", water.z
    #     print "water.stop_z = ", water.stop_z
    #     print
    #     # if (water.z + Water.water_rate) < water.stop_z:
    #     #     water.z = water.z + Water.water_rate
    #     # translate(0, 0, water.z)
    #     # rect(water.x * scl, water.y * scl, water.w * scl, water.h * scl)
    #     popMatrix()
    # fill(0, 100, 200)

def draw_sides():
    pushMatrix()
    translate(0, 0, Water.water_level)
    rotateY(PI/2)
    rect(0, 0, Water.water_level, col)
    translate(0, col)
    rotateX(PI/2)
    rect(0, 0, Water.water_level, col)
    popMatrix()
    
    pushMatrix()
    rotateX(PI)
    rotateZ(3*PI/2)
    rotateY(PI/2)
    rect(0, 0, Water.water_level, col)
    translate(0, col)
    rotateX(PI/2)
    rect(0, 0, Water.water_level, col)
    popMatrix()

def update_env():
    if Env.freeze is False:
        if Env.water_flush is True:
            # Env.transparency = (Env.transparency - 0.05)
            # print Water.water_level
            if Water.water_level <= 0.21:
                # print "STOP"
                # Water.water_rate = 0
                Water.water_level = 0.2
                Env.transparency = 0
            else:
                Water.water_level = (Water.water_level - 0.2) % 65
        else:
            Water.water_level = (Water.water_level + 0.05) % 65
            # Env.transparency = (Env.transparency + 0.05)
            if Water.water_level <= 0.05:
                Water.water_rate = 0
                Env.transparency = 0
            if Water.water_rate >= 14.9:
                Water.water_rate = 14.9
            else:
                Water.water_rate = Water.water_rate + 0.05
        # print Water.water_level


def reset_env():
    Env.water_flush = False
    Env.transparency = 0
    Water.water_level = 0
    Water.water_rate = 0
    Water.wave = 1







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
    
def color_red(z):
    return map(z, 0, 52, 30, 195)

def color_green(z):
    return map(z, 0, 45, 100, 160)

def color_blue(z):
    return map(z, 10, 60, 30, 140)

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
            Env.eyeZ += 10
        if key == '+':
            Env.eyeZ -= 10

def pan():
    if keyPressed is True:
        if key == 'a':
            Env.centerX += 10
        if key == 'd':
            Env.centerX -= 10
        if key == 'w':
            Env.centerY += 10
        if key == 's':
            Env.centerY -= 10


class My_vertex(object):
    
    low_points = []
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.grade = None

    def set_grade(self, My_vertex):
        self.grade = My_vertex

class Water_shape(object):

    def __init__(self, x, y, w, h, z, stop_z):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.z = z
        self.stop_z = stop_z

class Water(object):
    
    water_level = 1
    water_max = 0
    water_rate = 0
    x = .07
    
    def __init__(self):
        pass
    
class Coord(object):
    
    num_coords = 0
   
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
        

class Env(object):
    
    # x = 0.3927
    # y = 0
    # z = 1.2395
    z = 0
    x = 0
    y = 0
    freeze = False
    water_flush = False
    mode = 0
    transparency = 0
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