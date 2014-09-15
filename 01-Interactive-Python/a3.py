# template for "Stopwatch: The Game"

import simplegui

# define global variables
current_time = 0
tries = 0
wins = 0
game_in_prog = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format_time(t):
    a = t // 600
    b = (t - a*600) // 100
    c = t // 10 - (t // 100 * 10)
    d = t % 10
    return str(a) + ":" + str(b) + str(c) + "." + str(d)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
# also toggle game_in_prog variable
def start_timer():
    global game_in_prog
    timer.start()
    game_in_prog = True
    
def stop_timer():
    global tries
    global wins
    global game_in_prog
    timer.stop()
    if game_in_prog and (current_time % 10 == 0):
        wins += 1
        tries += 1
        game_in_prog = False
    elif game_in_prog:
        tries += 1
        game_in_prog = False
    else:
        pass
    
def reset_timer():
    global current_time
    global tries
    global wins
    global game_in_prog
    timer.stop()
    current_time = 0
    tries = 0
    wins = 0
    game_in_prog = False

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global current_time
    current_time += 1    

# define draw handler
def draw(canvas):
    global current_time
    canvas.draw_text(format_time(current_time), (90, 110), 36, "White")
    canvas.draw_text(str(wins) + "/" + str(tries), (240, 30), 24, "Yellow")
    
# create frame, create timer
frame = simplegui.create_frame("Stopwatch Game", 300, 200)
timer = simplegui.create_timer(100, timer_handler)

# register event handlers
frame.add_button("Start", start_timer, 50)
frame.add_button("Stop", stop_timer, 50)
frame.add_button("Reset", reset_timer, 50)
frame.set_draw_handler(draw)

# add instructions
frame.add_label('Goal is to stop on a whole second (e.g., 0:03.0)')

# start frame
frame.start()


# Checked against the grading rubric
# Thanks for reviewing!