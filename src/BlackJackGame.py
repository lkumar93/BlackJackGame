#
# THIS IS AN IMPLEMENTATION OF THE CLASSIC BLACKJACK GAME IN 2D
#
# COPYRIGHT BELONGS TO THE AUTHOR OF THIS CODE
#
# AUTHOR : LAKSHMAN KUMAR
# AFFILIATION : UNIVERSITY OF MARYLAND, MARYLAND ROBOTICS CENTER
# EMAIL : LKUMAR93@UMD.EDU
# LINKEDIN : WWW.LINKEDIN.COM/IN/LAKSHMANKUMAR1993
#
# THE WORK (AS DEFINED BELOW) IS PROVIDED UNDER THE TERMS OF THE MIT LICENSE
# THE WORK IS PROTECTED BY COPYRIGHT AND/OR OTHER APPLICABLE LAW. ANY USE OF
# THE WORK OTHER THAN AS AUTHORIZED UNDER THIS LICENSE OR COPYRIGHT LAW IS PROHIBITED.
# 
# BY EXERCISING ANY RIGHTS TO THE WORK PROVIDED HERE, YOU ACCEPT AND AGREE TO
# BE BOUND BY THE TERMS OF THIS LICENSE. THE LICENSOR GRANTS YOU THE RIGHTS
# CONTAINED HERE IN CONSIDERATION OF YOUR ACCEPTANCE OF SUCH TERMS AND
# CONDITIONS.
#

###########################################
##
##	LIBRARIES
##
###########################################

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

###########################################
##
##	VARIABLES
##
###########################################

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
dealer = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

###########################################
##
##	CLASSES
##
###########################################

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
        self.cards = []
        # create Hand object

    def __str__(self):
        n = 0
        str1 = ""
        for c in self.cards :
            n += 1
            str1 += " card number " + str(n) +" Value " + str(c)
             
        return str1
        # return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card)
        # add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand
	value = 0
        aces = 0
        global dealer
        for v in self.cards :
            
            if VALUES[v.get_rank()] == 1 :
                if (value + 11) < 22 :
                    if dealer == 1 and (value + 11) > 16 :
                         value += VALUES[v.get_rank()]
                            
                    else :   
                        value += VALUES[v.get_rank()] + 10 
                        aces += 1
                else :
                    value += VALUES[v.get_rank()]
                    aces += 1
            else:
                
                if aces == 2 and (VALUES[v.get_rank()]+value) > 21:
                    value -= 10
                    aces = 0
                
                value += VALUES[v.get_rank()]
                
                
        return value     
                
            
        
        
    def draw(self, canvas, pos):
        
        n = 1.5
        for d in self.cards :
            d.draw(canvas,[ n * pos[0] , pos [1]])
            n += 1.5
        
       # draw a hand on the canvas, use the draw method for cards
    

        
# define deck class 
class Deck:
    def __init__(self):
               
        self.deck = []
        
        for s in SUITS :
            for r in RANKS :
                card1 = Card(s,r)
                self.deck.append(card1)
        
        
    def shuffle(self):
        # shuffle the deck 
    
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        c = self.deck[-1]
        self.deck.pop()
        return c
   
        
    def __str__(self):
        
        str1 = " Deck Contains "
        
        for d in self.deck:
            str1 += " " + str(d)
        
        
        return str1 
        # return a string representing the deck


###########################################
##
##	FUNCTIONS
##
###########################################


 #define event handlers for buttons
def deal():
    global outcome, in_play , dealer , score
    global deck1
    
    if in_play  :
        score -= 1
    
    dealer = 0
    deck1 = Deck()
    deck1.shuffle()
    global player_hand
    player_hand = Hand()
    global dealer_hand
    dealer_hand = Hand()
    
    player_hand.add_card(deck1.deal_card())
    player_hand.add_card(deck1.deal_card())
    dealer_hand.add_card(deck1.deal_card())
    dealer_hand.add_card(deck1.deal_card())
    
    outcome = "Hit or Stand?"
    in_play = True

def hit():

    global in_play,score,outcome
    # if the hand is in play, hit the player
    if in_play :
        player_hand.add_card(deck1.deal_card())

        if player_hand.get_value() >21 :
            
            outcome = "You are Busted , New Deal ?"
            in_play = False
            score -= 1
      
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global in_play , score , outcome , dealer
    dealer = 1
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        if player_hand .get_value() < 22 :

            if in_play :
                while dealer_hand.get_value() < 17 :
                    dealer_hand.add_card(deck1.deal_card())

            if dealer_hand.get_value() > 21:
                outcome = "Dealer has busted , New Deal ?"
                score += 1
                #print dealer_hand
                #print outcome



            else :
                #print dealer_hand

                if dealer_hand.get_value() >= player_hand.get_value() :
                    outcome = "Dealer wins , New Deal ?"
                    #print outcome
                    score -= 1

                else :
                    outcome = "Player wins , New Deal ?"
                    #print outcome
                    score += 1

            in_play = False 

        else :
              outcome = "You are busted , New Deal ?"
              #print outcome
              in_play = False

        
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
   
    global outcome,dealer,score
    #card = Card("S", "A")
    player_hand.draw(canvas, [50, 400])
    dealer_hand.draw(canvas, [50 ,150])
    canvas.draw_text(outcome, (225, 570), 30, 'White')
    canvas.draw_text("Blackjack", (250, 50), 30, 'White')
    scoretext = "Score = " + str(score)
    canvas.draw_text(scoretext , (450, 90), 25, 'White')
    canvas.draw_text("Dealer's Hand" , (50, 120), 20, 'White')
    canvas.draw_text("Player's Hand" , (50, 370), 20, 'White')
    
    if  dealer_hand.cards[0].get_suit() == 'S' or dealer_hand.cards[0].get_suit() == 'C'  :
        card_loc = [ 36 , 48]
    else :        
        card_loc = [ 108 ,48 ]
        
    
    if(dealer == 0) :
        canvas.draw_image(card_back,card_loc , CARD_BACK_SIZE, [ 110 , 198 ], CARD_BACK_SIZE)

###########################################
##
##	MAIN FUNCTION
##
###########################################	

if __name__ == '__main__':

	# initialization frame
	frame = simplegui.create_frame("Blackjack", 600, 600)
	frame.set_canvas_background("Green")

	#create buttons and canvas callback
	frame.add_button("Deal", deal, 200)
	frame.add_button("Hit",  hit, 200)
	frame.add_button("Stand", stand, 200)
	frame.set_draw_handler(draw)



	# get things rolling
	deal()
	frame.start()



