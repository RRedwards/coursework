"""
Implementation of classic arcade game Pong
"""

# imports:
import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2  # simpler to put paddle_pos on front (gutter edge)
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

paddle1_pos = [0, 0]
paddle2_pos = [0, 0]
paddle1_vel = 0
paddle2_vel = 0
ball_pos = [0, 0]
ball_vel = [0, 0]
score1 = 0
score2 = 0


def ball_init(right):
    """
    Helper fn that spawns a ball
    by updating the ball's position vector and velocity vector.
    If right is True, the ball's velocity is upper right, else upper left.
    """
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    x_randvel = float(random.randrange(120, 270))/60
    y_randvel = float(random.randrange(5, 180))/60
    if right == True:
        ball_vel = [x_randvel, -y_randvel]
    else:
        ball_vel = [-x_randvel, -y_randvel]

        
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    if score1 > score2:
        right = False
    else:
        right = True
    score1 = 0
    score2 = 0
    paddle1_vel = 0
    paddle2_vel = 0
    paddle1_pos = [PAD_WIDTH, HEIGHT / 2]
    paddle2_pos = [(WIDTH - PAD_WIDTH), HEIGHT / 2]
    ball_init(right)

   
# define event handlers    
    
def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos[1] + paddle1_vel >= HALF_PAD_HEIGHT) and\
    (paddle1_pos[1] + paddle1_vel <= HEIGHT - HALF_PAD_HEIGHT):
        paddle1_pos[1] += paddle1_vel
    if (paddle2_pos[1] + paddle2_vel >= HALF_PAD_HEIGHT) and\
    (paddle2_pos[1] + paddle2_vel <= HEIGHT - HALF_PAD_HEIGHT):
        paddle2_pos[1] += paddle2_vel
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddle 1
    c.draw_polygon([(PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT),\
                   (0, paddle1_pos[1] - HALF_PAD_HEIGHT),\
                   (0, paddle1_pos[1] + HALF_PAD_HEIGHT),\
                   (PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT)],\
                   1, "White", "White")
    
    # draw paddle 2
    c.draw_polygon([(WIDTH - PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT),\
                   (WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT),\
                   (WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT),\
                   (WIDTH - PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT)],\
                   1, "White", "White")
     
    # update ball
    incr = 1.1  # scalar to increase ball_vel after paddle strike
    
    if ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]         # BOTTOM bounce
    elif ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]         # TOP bounce
        
    elif (ball_pos[0] >= (WIDTH - PAD_WIDTH - 1) - BALL_RADIUS) and\
    (ball_pos[1] <= paddle2_pos[1] + HALF_PAD_HEIGHT and\
    ball_pos[1] >= paddle2_pos[1] - HALF_PAD_HEIGHT):
        ball_vel[0] = - incr * ball_vel[0]  # RIGHT SIDE, paddle behind ball
        ball_vel[1] = incr * ball_vel[1]
    elif (ball_pos[0] >= (WIDTH - PAD_WIDTH - 1) - BALL_RADIUS):
        score1 += 1
        ball_init(False)                    # RIGHT SIDE, paddle NOT behind ball
        
    elif (ball_pos[0] <= BALL_RADIUS + PAD_WIDTH) and\
    (ball_pos[1] <= paddle1_pos[1] + HALF_PAD_HEIGHT and\
    ball_pos[1] >= paddle1_pos[1] - HALF_PAD_HEIGHT):
        ball_vel[0] = - incr * ball_vel[0]  # LEFT SIDE, paddle behind ball
        ball_vel[1] = incr * ball_vel[1]
    elif (ball_pos[0] <= BALL_RADIUS + PAD_WIDTH):
        score2 += 1
        ball_init(True)                     # LEFT SIDE, paddle NOT behind ball
        
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
            
    # draw ball and scores
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    c.draw_text(str(score1), (150, 40), 36, "White")
    c.draw_text(str(score2), (450, 40), 36, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 5
    if key == simplegui.KEY_MAP['w']:
            paddle1_vel = -acc
    elif key == simplegui.KEY_MAP['s']:
            paddle1_vel = acc
    elif key == simplegui.KEY_MAP['up']:
            paddle2_vel = -acc
    elif key == simplegui.KEY_MAP['down']:
            paddle2_vel = acc
            
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
            paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s']:
            paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up']:
            paddle2_vel = 0
    elif key == simplegui.KEY_MAP['down']:
            paddle2_vel = 0
            
def restart():
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("RESTART", restart, 175)
# add some labels
frame.add_label('')
frame.add_label("It's 1972...Let's Play Pong!!!")
frame.add_label('')
frame.add_label('')
frame.add_label('Controls for up / down:')
frame.add_label('')
frame.add_label('Player 1: W / S')
frame.add_label('Player 2: Up / Down Arrows')

# get things moving
new_game()

# start frame
frame.start()

# Thanks for reviewing!!!