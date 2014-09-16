"""GUI-based version of RPSLS"""


import simplegui
import random


# images:
# could use image.get_width() and .get_height(), if choosing other images
# -----------------------------------------------------------------------
rock_image = simplegui.load_image("http://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Omak_lake_balancing_rock.jpg/640px-Omak_lake_balancing_rock.jpg")
rock_size = (640, 427)

Spock_image = simplegui.load_image("http://img2.wikia.nocookie.net/__cb20101114221317/bigbangtheory/images/a/a7/Spock.jpg")
Spock_size = (559, 504)

paper_image = simplegui.load_image("http://upload.wikimedia.org/wikipedia/commons/c/c2/Blank_Notebook.jpg")
paper_size = (470, 310)

lizard_image = simplegui.load_image("http://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Chlamydosaurus_kingii.jpg/640px-Chlamydosaurus_kingii.jpg")
lizard_size = (640, 419)

scissors_image = simplegui.load_image("http://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Zackenschere.jpg/640px-Zackenschere.jpg")
scissors_size = (640, 309)

rpsls_image = simplegui.load_image("http://img4.wikia.nocookie.net/__cb20120822205915/bigbangtheory/images/7/7d/RPSLS.png")
rpsls_size = (600, 600)

tie_image = simplegui.load_image("http://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Necktie_Atlantic_knot.jpg/360px-Necktie_Atlantic_knot.jpg")
tie_size = (360, 480)
# -----------------------------------------------------------------------

# global text messages and image to display:
query = 'rock, paper, scissors, lizard, or Spock?'
player_choice = ''
comp_choice = ''
winner = ''
image_num = 5

# conversion dictionaries
item_dict = {'rock': 0, 'Spock': 1, 'paper': 2, 'lizard': 3, 'scissors': 4}
image_dict = {0: (rock_image, rock_size), \
              1: (Spock_image, Spock_size), \
              2: (paper_image, paper_size), \
              3: (lizard_image, lizard_size), \
              4: (scissors_image, scissors_size), \
              5: (rpsls_image, rpsls_size), \
              6: (tie_image, tie_size)}
              
# constants
MSG2_SIZE = 24
MSG2_COLOR = "White"


# Functions that compute RPSLS
     
def number_to_name(number):
    """converts number back to corresponding name in rpsls"""
    for name, value in item_dict.items():
        if number == value:
            return name

def rpsls(name):
    """
    takes player's choice as input, randomly generates computer's choice,
    calculates and prints result of game
    """
    global player_choice, comp_choice, winner, image_num
    
    # convert name to player_number
    player_number = item_dict.get(name)
    
    # determine if input is valid
    if player_number == None:
        player_choice = 'Invalid input. No ' + name + " in RPSLS."
        comp_choice = ''
        winner = ''
        image_num = 5
        return

    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0,5)

    # compute difference of player_number and comp_number modulo five
    difference = (player_number - comp_number) % 5

    # use if/elif/else to determine winner
    if (difference == 1) or (difference == 2):
        winner = "Player wins!"
        image_num = player_number
    elif (difference == 3) or (difference == 4):
        winner = "Computer wins!"
        image_num = comp_number
    elif difference == 0:
        winner = "Player and computer tie!"
        image_num = 6
    else:
        winner = "Error computing winner."

    # convert comp_number to name using number_to_name
    comp_name = number_to_name(comp_number)
    
    # update player and computer choice for display
    player_choice = "Player chooses " + name
    comp_choice = "Computer chooses " + comp_name
     
    
# Handler for input field
def get_guess(guess):
    rpsls(guess)
        
# Handler to draw on canvas
def draw(canvas):
    canvas.draw_text(query, [50, 35], 32, "LightGreen")
    canvas.draw_text(player_choice, [50, 70], MSG2_SIZE, MSG2_COLOR)
    canvas.draw_text(comp_choice, [50, 100], MSG2_SIZE, MSG2_COLOR)
    canvas.draw_text(winner, [50, 130], MSG2_SIZE, MSG2_COLOR)
    canvas.draw_image(image_dict[image_num][0], \
                      (image_dict[image_num][1][0] // 2, image_dict[image_num][1][1] // 2), \
                      (image_dict[image_num][1][0], image_dict[image_num][1][1]), \
                      (400, 475), \
                      (image_dict[image_num][1][0], image_dict[image_num][1][1]))
    canvas.draw_polygon([[0, 150], [800, 150]], 2, "White")


# Create frame and assign callbacks to event handlers
frame = simplegui.create_frame("GUI-based RPSLS", 800, 800)
frame.add_input("Enter guess for RPSLS", get_guess, 200)
frame.set_draw_handler(draw)


# Start the frame animation
frame.start()


###################################################
# idea for upgrade:
# add matrix for how items beat other items
# and output messages like "Paper disproves Spock.  Paper wins!"

