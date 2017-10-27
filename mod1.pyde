
import math

##############################################################################
############################## GLOBAL VARIABLES ##############################
##############################################################################
scl = 8

col = 400
row = 400
depth = 40

terrain = [[0 for x in range(col/scl + 1)] for y in range(row/scl + 1)]

##############################################################################
#################################### SETUP ###################################
##############################################################################
def setup():
    frameRate(30)
    size(col*3, row*3, P3D)
    input = take_input()
    global coord_arr
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
    change_view()
    translate(width/2, height/2 + 100)
    pick_mode()
    rotate_shape()
    reset()
    draw_box()
    if Env.mode == 0:
        draw_surface()
    elif Env.mode == 1:
        if Drop.rain is True:
            for i in range(1000):
                draw_rain()
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
    elif Env.mode == 4:
        draw_surface()
        draw_water_rise()
        draw_sides()
        update_env()

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
    scale_x = Coord.min_x + Coord.max_x
    scale_y = Coord.min_y + Coord.max_y
    if scale_y > scale_x:
        scale_z = scale_y
    else:
        scale_z = scale_x
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
    
    global water_rise_terrain
    water_rise_terrain = [[0 for x in range(col/scl + 1)] for y in range(row/scl + 1)]
    for y in range(row/scl+1):
        for x in range(col/scl+1):
            water_terrain[x][y] = 0
    for water in water_arr:
        r = 9
        make_water_circle(water.x, water.y, r, int(water.stop_z))
        r = 7
        make_water_rise_circle(water.x, water.y, r, int(water.stop_z))
    
    global water_wave_terrain
    water_wave_terrain = [[0 for x in range(col/scl + 1)] for y in range(row/scl + 1)]

##################################
###### MAKE_WATER_CIRCLE #########
##################################
def make_water_circle(cx, cy, r, z):
    for x in range(cx - r, cx + r):
        for y in range(cy - r, cy + r):
            z_dist = dist(cx, cy, x, y)
            z_dif = Water.water_max / 2
            z_new = (((cos(z_dist/2)+1)/PI)*z) + z_dif #change the z_dist divisor to influence and tweak
            if z_dist <= r:
                if z_new > water_terrain[x][y]:
                    water_terrain[x][y] = z_new

#######################################
###### MAKE_WATER_RISE_CIRCLE #########
#######################################
def make_water_rise_circle(cx, cy, r, z):
    for x in range(cx - r, cx + r):
        for y in range(cy - r, cy + r):
            z_dist = dist(cx, cy, x, y)
            z_dif = Water.water_max / 2
            z_new = - 30
            if z_dist <= r:
                if z_new < water_terrain[x][y]:
                    water_rise_terrain[x][y] = z_new
 
##################################
########### GRADIENT #############
##################################               
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
            else:
                continue
    
    global water_arr
    water_arr = [0 for x in range(len(My_vertex.low_points))]
    i = 0
    for low in My_vertex.low_points:
        x1 = 1
        x2 = 1
        current = smooth_terrain[low.x][low.y]
        while smooth_terrain[low.x-x1][low.y].grade == current:
            current = smooth_terrain[current.x-x1][current.y]
            x1 += 1
        z = smooth_terrain[(current.x-x1)+1][current.y].z
        z = min(current.z, z)
        current = smooth_terrain[low.x][low.y]
        while smooth_terrain[low.x+x2][low.y].grade == current:
            current = smooth_terrain[current.x+x2][current.y]
            x2 += 1
        y1 = 1
        y2 = 1
        z = smooth_terrain[(current.x+x2)-1][current.y].z
        z = min(current.z, z)
        current = smooth_terrain[low.x][low.y]
        while smooth_terrain[low.x][low.y-y1].grade == current:
            current = smooth_terrain[current.x][current.y-y1]
            y1 += 1
        z = smooth_terrain[current.x][(current.y-y1)+1].z
        z = min(current.z, z)
        current = smooth_terrain[low.x][low.y]
        while smooth_terrain[low.x][low.y+y2].grade == current:
            current = smooth_terrain[current.x][current.y+y2]
            y2 += 1
        z = smooth_terrain[current.x][(current.y+y2)-1].z
        z = min(current.z, z)
        Water.water_max = max(Water.water_max, z)
        water_arr[i] = Water_shape(low.x, low.y, (x1 + x2), (y1 + y2), low.z, z)
        i += 1
        
            
##################################
######### MAKE_CIRCLE ############
##################################
def make_circle(cx, cy, r, z):
    for x in range(cx - r, cx + r):
        for y in range(cy - r, cy + r):
            z_dist = dist(cx, cy, x, y)
            z_new = (((cos(z_dist/3)+1)/PI)*z)
            if z_dist <= r:
                if z_new > smooth_terrain[x][y].z:
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
        elif key == '0':
            reset_env()
            Env.mode = 0
        elif key == '1':
            reset_env()
            Env.mode = 1
        elif key == '2':
            reset_env()
            Env.mode = 2
        elif key == '3':
            reset_env()
            Env.mode = 3
        elif key == '4':
            reset_env()
            Env.mode = 4
        elif key == 'f':
            Env.water_flush = not Env.water_flush
        elif key == '.':
            Drop.rain = not Drop.rain
            

##################################
######### DRAW_BOX ###############
##################################
def draw_box():
    stroke(0, 140, 0)
    noStroke()
    fill(0, 100, 0)
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

#######################################
######### DRAW_WATER_RISE #############
#######################################

def draw_water_rise():
    if len(coord_arr) > 10:
        pushMatrix()
        translate((col / -2), (row / -2), (depth / 2))
        
        for y in range(row/scl):
            beginShape(TRIANGLE_STRIP)
            for x in range(col/scl +1):
                
                if Water.water_stop > 0:
                        print water_rise_terrain[x][y], Water.water_stop
                        if water_rise_terrain[x][y] == -30:
                            water_rise_terrain[x][y] += Water.water_stop
                            water_rise_terrain[x][y+1] += Water.water_stop
                if water_rise_terrain[x][y] == -30 + Water.water_stop:
                    fill(0, 100, 200, 0)
                    vertex(x*scl, y*scl, (water_rise_terrain[x][y]) + Water.water_rise_rate)
                    vertex(x*scl, (y+1)*scl, (water_rise_terrain[x][y+1]) + Water.water_rise_rate)
                else:
                    fill(0, 100, 200, 110)
                    noStroke()
                    vertex(x*scl, y*scl, (water_rise_terrain[x][y]) + Water.water_rise_rate)
                    vertex(x*scl, (y+1)*scl, (water_rise_terrain[x][y+1]) + Water.water_rise_rate)
                    Water.water_z = (water_rise_terrain[x][y]) + Water.water_rise_rate
            endShape()
        popMatrix()
        # draw_water()
    else:
        draw_water()

##################################
######### DRAW_WATER #############
##################################
def draw_water():
    pushMatrix()
    translate((col / -2), (row / -2), (depth / 2))
    for y in range(row/scl):
        beginShape(TRIANGLE_STRIP)
        for x in range(col/scl + 1):
            noStroke()
            fill(0, 100, 200, 110)
            vertex(x*scl, y*scl, Water.water_level)
            vertex(x*scl, (y+1)*scl, Water.water_level)
        if Water.blue_opaq >= 160:
            Water.blue_opaq = 160
        else:
            Water.blue_opaq += .005
        print(Water.blue_opaq)
        endShape()
    popMatrix()
        
        
##################################
########### DRAW_WAVE ############
##################################
def draw_wave():
    pushMatrix()
    translate((col / -2), (row / -2), (depth / 2))
    Env.flying -= 0.02
    yoff = Env.flying
    for y in range(row/scl):
        xoff = 0 
        for x in range(col/scl + 1):
            water_wave_terrain[x][y] = map(noise(xoff, yoff), 0, 1, 0, 50)
            xoff = xoff + 0.05
        yoff = yoff + 0.05
    
    for y in range(row/scl):
        beginShape(TRIANGLE_STRIP)
        for x in range(col/scl + 1):
            if len(coord_arr) > 12:
                if (x <= col/scl - 15 and x >= 15) and (y <=row/scl - 15 and y >= 10):
                    fill(0, 100, 200, 0)
                else:
                    fill(0, 100, 200, 100)
            else:
                fill(0, 100, 200, 100)
            noStroke()
            vertex(x*scl, y*scl, -8 + water_wave_terrain[x][y]) # map(noise(xoff), 0, 1, 0, 5))
            vertex(x*scl, (y+1)*scl, -8 + water_wave_terrain[x][y+1])# map(noise(yoff), 0, 1, 0, 5))
        endShape()
    Water.water_level = 0
    Water.water_rate = 0
    Water.water_rise_rate = 0
    popMatrix()
    

##################################
######## DRAW_WATER_LOW ##########
##################################
def draw_water_low():    
    if len(coord_arr) > 10:
        pushMatrix()
        translate((col / -2), (row / -2), (depth / 2))
        for y in range(10, row/scl - 10):
            beginShape(TRIANGLE_STRIP)
            for x in range(10, col/scl - 9):
                fill(0, 100, 200, 50)
                noStroke()
                vertex(x*scl, y*scl, (water_terrain[x][y] - 15) + Water.water_rate)
                vertex(x*scl, (y+1)*scl, (water_terrain[x][y+1] - 15) + Water.water_rate)
            endShape()
        popMatrix()

##################################
########## DRAW_SIDES ############
##################################
def draw_sides():
    translate((col / -2), (row / -2), (depth / 2))
    fill(0, 100, 200, Water.blue_opaq)
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


##################################
########## UPDATE_ENV ############
##################################
def update_env():
    if Env.freeze is False:
        if Env.water_flush is True:
            if Water.water_level <= 0.21:
                Water.water_level = 0.2
                Env.transparency = 0
            else:
                Water.water_level = (Water.water_level - 0.2) % 65
        else:
            Water.water_level = (Water.water_level + 0.05) % 65
            if Water.water_level <= 0.04:
                Water.water_rate = 0
                Water.water_rise_level = 0
                Env.transparency = 0
                Water.water_level = 0
                Water.water_rise_rate = 0
            if Env.mode == 4:
                if Water.water_rise_rate > 45:
                    Water.water_rise_rate = 45
                    # print "Water.water_stop = ", Water.water_stop
                    # if Water.water_stop + Water.water_z:    
                elif Water.water_rise_rate == 45:
                    Water.water_stop += 0.05
                else:
                    Water.water_rise_rate = Water.water_rise_rate + 0.09
            else:
                if Water.water_rate >= 14.9:
                    Water.water_rate = 14.9
                Water.water_rate = Water.water_rate + 0.05
                Env.water_rise = Env.water_rise + .05

def reset_env():
    Env.water_flush = False
    Env.transparency = 0
    Water.water_level = 0
    Water.water_rate = 0
    Water.water_rise_rate = 0
    Water.wave = 1
    Env.water_rise = 0

##################################
########## DRAW_RAIN ############
##################################
def draw_rain():
    pushMatrix()
    translate(-col/2, 0, depth*2)
    drops = [0 for x in range(1)]
    x1 = random(0, col)
    y1 = random(-row/2, row/2)
    z1 = random(-60, 60)
    for i in range(len(drops)):
        drops[i] = Drop(x1, y1, z1, x1, y1, z1+7)
    for i in range(len(drops)):
        drops[i].show()
    popMatrix()
            


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
    water_rise_rate = 0
    water_stop = 0
    water_z = 0
    x = .07
    blue_opaq = 110
    
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
        
class Drop(object):
    
    rain = True
    
    def __init__(self, x1, y1, z1, x2, y2, z2):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
    
    def show(self):
        stroke(0, 100, 200)
        line(self.x1, self.y1, self.z1, self.x2, self.y2, self.z2)

class Env(object):
    
    x = 0.3927
    y = 0
    z = 1.2395

    freeze = False
    water_flush = False
    mode = 0
    transparency = 0
    water_rise = 0
    flying = 0
    
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