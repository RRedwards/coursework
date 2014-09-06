# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals, create & shuffle deck
def init():
    global card_set, CARD_WIDTH, BOARD_WIDTH, BOARD_HEIGHT, exposed, state, turns, card_up1, card_up2
    
    BOARD_WIDTH = 800
    BOARD_HEIGHT = 100
    card_up1 = None
    card_up2 = None
    state = 0
    turns = 0
    label.set_text("Moves = " + str(turns))
    
    card_list = range(8)
    card_matches = list(card_list)
    card_set = card_list + card_matches
    random.shuffle(card_set)
    
    exposed = []
    for n in range(len(card_set)):
        exposed.append(False)
    
    CARD_WIDTH = BOARD_WIDTH / len(card_set)

     
# define event handlers
def mouseclick(pos):
    global exposed, state, card_up1, card_up2, turns, CARD_WIDTH, card_set
    
    for n in range(len(card_set)):
        if not exposed[n] and pos[0] >= (CARD_WIDTH * n) and pos[0] < (CARD_WIDTH * (n + 1)):
            exposed[n] = True
            if state == 0:
                state = 1
                card_up1 = n
            elif state == 1:
                state = 2
                card_up2 = n
                turns += 1
                label.set_text("Moves = " + str(turns))
            else:
                state = 1
                if card_set[card_up1] != card_set[card_up2]:
                    exposed[card_up1] = False
                    exposed[card_up2] = False
                    card_up1 = None
                    card_up2 = None
                card_up1 = n

                        
# draw handler...cards are logically 50x100 pixels in size    
def draw(canvas):
    for n in range(len(card_set)):
        if not exposed[n]:
            canvas.draw_polygon([(((CARD_WIDTH * (n + 1)) - CARD_WIDTH), 0),\
                                 ((CARD_WIDTH * (n + 1)), 0),\
                                 ((CARD_WIDTH * (n + 1)), BOARD_HEIGHT),\
                                 (((CARD_WIDTH * (n + 1)) - CARD_WIDTH), BOARD_HEIGHT)],\
                                 2, "White", "Purple")
        else:    
            canvas.draw_text(str(card_set[n]),\
                            [((CARD_WIDTH * (n + 1)) - (CARD_WIDTH / 2 + 10)), (BOARD_HEIGHT / 2 + 10)],\
                            40, "White", "sans-serif")


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
label = frame.add_label("Moves = 0")

# initialize global variables, create & shuffle deck
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()


# I checked against grading rubric...