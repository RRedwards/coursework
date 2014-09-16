# GUI-based version of RPSLS

###################################################
# Student should add code where relevant to the following.

import simplegui
import random

# Functions that compute RPSLS
     
def number_to_name(number):
    """converts number back to corresponding name in rpsls"""
    if number == 0:
        name = 'rock'
    elif number == 1:
        name = 'Spock'
    elif number == 2:
        name = 'paper'
    elif number == 3:
        name = 'lizard'
    elif number == 4:
        name = 'scissors'
    else:
        print "Oops! " + str(number) + " is not an integer between 0 and 4."
    return name

def name_to_number(name):
    """converts player's string to number between 0 and 4"""
    if name == 'rock':
        number = 0
    elif name == 'Spock':
        number = 1
    elif name == 'paper':
        number = 2
    elif name == 'lizard':
        number = 3
    elif name == 'scissors':
        number = 4
    else:
        print ""
        print name + " does not exist in rpsls.  Try again!"
    return number

def rpsls(name):
    """
    takes player's choice as input, randomly generates computer's choice,
    caluculates and prints result of game
    """
    
    # convert name to player_number using name_to_number
    player_number = name_to_number(name)

    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0,5)

    # compute difference of player_number and comp_number modulo five
    difference = (player_number - comp_number) % 5

    # use if/elif/else to determine winner
    if (difference == 1) or (difference == 2):
        winner = "Player wins!"
    elif (difference == 3) or (difference == 4):
        winner = "Computer wins!"
    elif difference == 0:
        winner = "Player and computer tie!"
    else:
        winner = "Error computing winner."

    # convert comp_number to name using number_to_name
    comp_name = number_to_name(comp_number)
    
    # print results
    print ""
    print "Player chooses " + name
    print "Computer chooses " + comp_name
    print winner
     
    
# Handler for input field
def get_guess(guess):
    if guess == 'rock' \
    or guess == 'paper' \
    or guess == 'scissors' \
    or guess == 'lizard' \
    or guess == 'Spock':
        rpsls(guess)
    else:
        print
        print "Error: Bad input ", '"', guess, '"', " to rpsls."


# Create frame and assign callbacks to event handlers
frame = simplegui.create_frame("GUI-based RPSLS", 200, 200)
frame.add_input("Enter guess for RPSLS", get_guess, 200)


# Start the frame animation
frame.start()


###################################################
# Test

get_guess("Spock")
get_guess("dynamite")
get_guess("paper")
get_guess("lazer")

###################################################
# Sample expected output from test
# Note that computer's choices may vary from this sample.

#Player chose Spock
#Computer chose paper
#Computer wins!
#
#Error: Bad input "dynamite" to rpsls
#
#Player chose paper
#Computer chose scissors
#Computer wins!
#
#Error: Bad input "lazer" to rpsls
#
