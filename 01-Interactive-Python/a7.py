# Spaceship --  Part B for Week 8
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False
message1 = ""
message2 = ""

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 25)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
soundtrack.set_volume(.4)
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
explosion_sound.set_volume(.5)

# helper functions to handle transformations, process groups, and reset sprites
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def choose_rock_vel():
    global rock_max_vel, score
    rock_vel = []
    for i in (0, 1):
        rock_vel.append(((random.randrange(-rock_max_vel * 60, rock_max_vel * 60)) / 60) * (1 + score * 0.05))
    return rock_vel

def choose_rock_pos():
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    return rock_pos

def process_sprite_group(sprite_set, canvas):
    for sprite in list(sprite_set):
        sprite.draw(canvas)
        if sprite.update():
            sprite_set.remove(sprite)
        
def group_collide(group, other_object):
    collisions = 0
    for sprite in list(group):
        if sprite.collide(other_object):
            group.remove(sprite)
            explosion_group.add(Sprite(sprite.get_pos(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound))
            collisions += 1
    return collisions

def group_group_collide(group_m, group_r):
    collisions = 0
    for sprite_m in list(group_m):
        if group_collide(group_r, sprite_m) > 0:
            collisions += 1
            group_m.remove(sprite_m)
    return collisions

def init_objs():
    global my_ship, rock_group, missile_group, explosion_group
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    rock_group = set([])
    missile_group = set([])
    explosion_group = set([])

# set constants for object behavior
turn_const = 0.05
frict_const = 0.99
acc_const = 0.1
missile_const = 6
rock_max_vel = 0.3
rock_max_ang_vel = 0.2

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.image_thrust_center = ((self.image_center[0] + self.image_size[0] + 0), self.image_center[1])
        
    def draw(self,canvas):
        if self.thrust == False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_thrust_center, self.image_size, self.pos, self.image_size, self.angle)
            
    def update(self):
        
        # position and angle update
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
        
        # friction update to decrease velocity
        self.vel[0] *= frict_const
        self.vel[1] *= frict_const
        
        # thrust update to add acceleration
        forward = angle_to_vector(self.angle)
        if self.thrust == True:
            self.vel[0] += (forward[0] * acc_const)
            self.vel[1] += (forward[1] * acc_const)
        
    def turn(self, turn_value):
        self.angle_vel = turn_value
        
    def thruster(self):
        if self.thrust == True:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
    
    def shoot(self):
        forward = angle_to_vector(self.angle)
        missile_group.add(Sprite([self.pos[0] + forward[0] * self.image_center[0], self.pos[1] + forward[1] * self.image_center[1]],\
                                 [self.vel[0] + forward[0] * missile_const, self.vel[1] + forward[1] * missile_const],\
                                 0, 0, missile_image, missile_info, missile_sound))
        
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated == True:
            explos_index = (self.age % self.lifespan) // 1
            canvas.draw_image(self.image,\
                              [self.image_center[0] + explos_index * self.image_size[0], self.image_center[1]],\
                              self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        
        # position and angle update
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
        
        # age update and check for removal
        self.age += 0.4
        if (self.lifespan != None) and (self.age >= self.lifespan):
            return True
         
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def collide(self, other_object):
        if dist(self.pos, other_object.get_pos()) < (self.radius + other_object.get_radius()):
            return True 
           
def draw(canvas):
    global time, lives, score, started, message1, message2
    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])

    # draw ship, update ship
    my_ship.draw(canvas)
    my_ship.update()
    
    # draw and update sprite groups
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # check for collisions betw. rocks and ship, update rocks and lives
    if group_collide(rock_group, my_ship) > 0:
        lives -= 1
        
    # check for collisions betw. missiles & rocks, update missiles & rocks and score
    score += group_group_collide(missile_group, rock_group)
    
    # draw lives and score info
    canvas.draw_text("Lives: " + str(lives), (10, 40), 36, "White", "sans-serif")
    canvas.draw_text("Score: " + str(score), ((WIDTH - 180), 40), 36, "White", "sans-serif")
    canvas.draw_text(str(message1), (168, 40), 22, "White", "sans-serif")
    canvas.draw_text(str(message2), (310, 70), 22, "White", "sans-serif")
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        
    # reset game when lives == 0
    if lives <= 0:
        started = False
        init_objs()
        message1 = "You died! Insert another coin to play again!"
        message2 = "Or just..."
        soundtrack.pause()
        soundtrack.rewind()
    
# timer handler that spawns a rock
#    I plan to split this into 2 functions later to make it less confusing
def rock_spawner():
    global rock_group, started
    rock_pos = choose_rock_pos()
    if len(rock_group) < 12 and started == True\
    and dist(rock_pos, my_ship.get_pos()) >= (40 + 3 * my_ship.get_radius()):
        rock_group.add(Sprite(rock_pos,\
                              choose_rock_vel(),\
                              0,\
                              random.random() * (rock_max_ang_vel * 2) - rock_max_ang_vel,\
                              asteroid_image, asteroid_info))

        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
init_objs()

# set key handlers
def keydown(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.turn(-turn_const)
    if key == simplegui.KEY_MAP["right"]:
        my_ship.turn(turn_const)
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust = True
        my_ship.thruster()
    if key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
            
def keyup(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.turn(0)
    if key == simplegui.KEY_MAP["right"]:
        my_ship.turn(0)
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust = False
        my_ship.thruster()

# mouseclick handler that resets UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score, message1, message2
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        message1 = ""
        message2 = ""
        soundtrack.play()

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# add labels to communicate the control keys to new users
frame.add_label("Left = Turn Counterclockwise")
frame.add_label("")
frame.add_label("Right = Turn Clockwise")
frame.add_label("")
frame.add_label("Up = Thrust/Accelerate")
frame.add_label("")
frame.add_label("Space Bar = Shoot")

# get things rolling
timer.start()
frame.start()

# Thanks for reviewing my code!!! :)