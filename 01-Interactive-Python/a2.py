# my "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

# initialize global variables used in your code
num_range = 100
secret_num = 0
guess_count = 7

#helper function to initialize game
def init():
    global num_range
    global guess_count
    global secret_num
    if num_range == 100:
        secret_num = random.randrange(0,100)
        guess_count = 7
        print "New Game.  Range is from 0 to 100"
        print "Number of remaining guesses is ", guess_count
        #print "Secret number is: ", secret_num # for testing
        print
    elif num_range == 1000:
        secret_num = random.randrange(0,1000)
        guess_count = 10
        print "New Game.  Range is from 0 to 1000"
        print "Number of remaining guesses is ", guess_count
        #print "Secret number is: ", secret_num # for testing
        print
    else:
        print "Error in determining num_range"


# define event handlers for control panel
    
def range100():
    # button that changes range to range [0,100) and restarts
    global num_range
    num_range = 100
    init()

def range1000():
    # button that changes range to range [0,1000) and restarts
    global num_range
    num_range = 1000
    init()
    
def get_input(guess):
    # input field handler: main game logic goes here
    global num_range
    global guess_count
    global secret_num
    
    guess_count -= 1
    
    if (guess_count >= 1) and (float(guess) != secret_num):
        print "Guess was ", guess
        print "Number of remaining guesses is ", guess_count
        #print "Secret number is: ", secret_num # for testing
        if float(guess) > secret_num:
            print "Lower!"
            print
        else:
            print "Higher!"
            print
    elif float(guess) == secret_num:
        print "Guess was ", guess
        print "Number of remaining guesses is ", guess_count
        #print "Secret number is: ", secret_num # for testing
        print "Correct!!!"
        print
        print
        init()
    else:    
        print "Guess was ", guess
        print "Number of remaining guesses is ", guess_count
        print "You Lost!!!"
        print "The secret number was: ", secret_num
        print
        print
        init()
        
    
# create frame
f = simplegui.create_frame("Guess the Number", 200, 200)


# register event handlers for control elements
f.add_button("Range is [0, 100)", range100, 200)
f.add_button("Range is [0, 1000)", range1000, 200)
f.add_input("Enter a guess", get_input, 200)


# start frame
f.start()

init()

# checked completed program against the grading rubric
