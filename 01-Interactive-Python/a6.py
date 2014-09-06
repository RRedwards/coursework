# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = "Hit or Stand?"
winner = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

#def debug_print(s):
    #print s

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []	# create Hand object

    def __str__(self):
        s = "Hand contains: "
        for i in range(len(self.cards)):
            s += str(self.cards[i]) + " "
        return s  # return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        hand_value = 0
        for card in self.cards:
            hand_value += VALUES[card.get_rank()]
        for card in self.cards:
            if card.get_rank() == 'A':
                if hand_value + 10 <= 21:
                    hand_value += 10
        return hand_value

    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        y = pos[1]
        x = pos[0]
        for card in self.cards:
            card.draw(canvas, [x, y])
            x += CARD_SIZE[0] + 10
 
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.deck.append(card)  # create a Deck object

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        card = self.deck.pop(0)
        return card  # deal a card object from the deck
    
    def __str__(self):
        s = "Deck contains: "
        for i in range(len(self.deck)):
            s += str(self.deck[i]) + " "
        return s   # return a string representing the deck



#define event handlers for buttons
def deal():
    global outcome, in_play, current_deck, player_hand, dealer_hand, winner, score
    
    if (in_play == True):
        winner = "Player resigned round. Dealer wins."
        score -= 1
        
    if (in_play == False):
        winner = ""

    current_deck = Deck()
    current_deck.shuffle()
    
    player_hand = Hand()
    dealer_hand = Hand()
    
    player_hand.add_card(current_deck.deal_card())
    player_hand.add_card(current_deck.deal_card())
    
    dealer_hand.add_card(current_deck.deal_card())
    dealer_hand.add_card(current_deck.deal_card())
    
    
    #print "Dealer ", dealer_hand, "Value: ", dealer_hand.get_value()
    #print "Player ", player_hand, "Value: ", player_hand.get_value()
    
    in_play = True
    outcome = "Hit or Stand?"

def hit():
    global in_play, player_hand, outcome, score, winner
 
    # if the hand is in play, hit the player
    if (in_play == True):
        player_hand.add_card(current_deck.deal_card())
        #print "Dealer ", dealer_hand, "Value: ", dealer_hand.get_value()
        #print "Player ", player_hand, "Value: ", player_hand.get_value()
        
    # if busted, assign a message to outcome, update in_play and score  
    if (in_play == True) and (player_hand.get_value() > 21):
        in_play = False
        outcome = "New Deal?"
        winner = "Dealer wins.  Player has busted."
        #print "You have busted"
        score -= 1
       
def stand():
    global in_play, player_hand, dealer_hand, outcome, score, winner
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    while (in_play == True) and (dealer_hand.get_value() < 17):
        dealer_hand.add_card(current_deck.deal_card())
        #print "Dealer ", dealer_hand, "Value: ", dealer_hand.get_value()

    if (in_play == True) and (dealer_hand.get_value() > 21):
        in_play = False
        outcome = "New Deal?"
        winner = "Player wins.  Dealer has busted."
        #print "Dealer has busted"
        score += 1
    else:
        if (in_play == True) and (player_hand.get_value() <= dealer_hand.get_value()):
            in_play = False
            outcome = "New Deal?"
            winner = "Dealer wins."
            #print "Dealer wins!"
            score -= 1
        elif (in_play == True) and (player_hand.get_value() > dealer_hand.get_value()) and (player_hand.get_value() <= 21):
            in_play = False
            outcome = "New Deal?"
            winner = "Player wins."
            #print "Player wins!"
            score += 1
        else:
            #print "You need to press deal!!!"
            outcome = "Press 'Deal'."
    in_play = False
            
# draw handler    
def draw(canvas):
    global player_hand, dealer_hand, outcome, score, winner
    
    canvas.draw_text("Blackjack", (30, 50), 50, "White")
    canvas.draw_text("Score: " + str(score), (400, 50), 40, "White", "sans-serif")
    canvas.draw_text("Dealer", (30, 130), 35, "White", "sans-serif")
    canvas.draw_text("Player", (30, 380), 35, "White", "sans-serif")
    canvas.draw_text(str(outcome), (250, 380), 35, "White", "sans-serif")
    canvas.draw_text(str(winner), (180, 130), 25, "White", "sans-serif")
    
    dealer_hand.draw(canvas, [30, 150])
    player_hand.draw(canvas, [30, 400])
    
    # hide dealer's hole card while game is in play
    if (in_play == True):
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [65.5, 198], CARD_BACK_SIZE)

# initialization of frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#initialize globals for deck and hand objects
current_deck = Deck()
player_hand = Hand()
dealer_hand = Hand()

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
frame.start()

# call deal so that game begins upon opening frame
deal()

# test against grading rubric