# BLOCK BREAKER WITH CLASS
''' A very simple version of the block breaker game, with 2 blocks
    that the user must destroy by bouncing the ball on them using a controlled bar
    at the bottom'''

import pygame, sys
from pygame.locals import *
import random as rm

# This is the level number that our class will read in and generate
level = 3


# I want to define a class to put everything associated with our blocks to be broken
class Block_objects(object):
    
    
    # These are some initial values that are used throughout the class    
    block_length = 75    
    block_width = 40
    block = []
    block_colour = []
    sub_block = []
    blockx = []
    blocky = []



    
    # my init function.  I only want to read in the level number for now
    def __init__(self, level):
        self.level = level
        

    
    # This will generate two arrays: one for the x-positions of the blocks and the other for the y-position
    # Note the positions will depend on the level number
    def block_positions(self):
            
        if self.level == 1: # if in level 1, just have a single row of 8 blocks side by side
            
            for i in range(0, int(screen_pixel_width/self.block_length)):          
                self.blockx.append((self.block_length)*i) # blocks nestled next to one another
                self.blocky.append(self.block_width*1.5)


        elif self.level == 2: # in in level 2, just have a single row of 4 blocks equally spaced
            
            for i in range(0, int(screen_pixel_width/(2*self.block_length))):          
                self.blockx.append(self.block_length/2 + 2*self.block_length*i)
                self.blocky.append(self.block_width*1.5) 
                
        elif self.level == 3: # two rows of 4 blocks
            
            for i in range (0, int(screen_pixel_width/(2*self.block_length))):
                self.blockx.append(self.block_length/2 + 2*self.block_length*i)
                self.blocky.append(self.block_width*1)
                self.blockx.append(self.block_length/2 + 2*self.block_length*i)
                self.blocky.append(self.block_width*2)
                #self.cat = pygame.image.load('surprise.png')
                #DISPLAYSURF.blit(self.cat, (100,100))
                
        elif self.level == 4: # three rows of 4 blocks
            
            for i in range(0, int(screen_pixel_width/(2*self.block_length))): 
                self.blockx.append(self.block_length/2 + 2*self.block_length*i)
                self.blocky.append(self.block_width/4)
                self.blockx.append(2*self.block_length*i)
                self.blocky.append(self.block_width/4 + self.block_width*1.2)
                self.blockx.append(self.block_length/2 + 2*self.block_length*i)
                self.blocky.append(self.block_width/4 + 2*self.block_width*1.2)

        
    

    
    
    # Now that we have chosen the positions of our blocks, let's actually create them using this function, create_blocks
    # Note this depends on the previous function, which itself depends on the level number
    def create_blocks(self, block_positions):
    
        # So our number of blocks, block_count is the same as the number of array elements in blockx (or blocky).
        # This is just to make it a bit clearere when we remove blocks throughout the game
        self.block_count = len(self.blockx)        
        
        
        # Now I want our blocks to be created and appended to another list, called block.
        # My blocks actually consist of a smaller one inside another (both different colours) to give the illusion of borders to our blocks
        for i in range (0, len(self.blockx)):
    
    
            # larger blocks
            self.block.append(pygame.Surface([self.block_length, self.block_width])) # need to use pygame.Surface to blit
            self.block[i].fill(block_border_colour)
    

            # smaller blocks inside larger blocks
            self.sub_block.append(pygame.Surface([self.block_length-2, self.block_width-2]))
            self.sub_block[i].fill(RED)
            
            # Let's append the names of the colours of the sub-blocks to another array, block_colour.  This will make it easier to change the colour
            # of the sub-blocks when they are hit by the ball
            self.block_colour.append('red')
            

        
        
        
    # If the ball collides with a block, I want the ball to bounce off it.  Then, I want the block to change colour to yellow, then to green and then
    # for it to be removed (actually I am placing the block outside the observable screen and giving it zero size.
    # Then the block_count will be made 1 smaller.  If block_count reaches zero, then user has completed the game
        
    # I need to do this first for if the ball hits the left or right sides of a block.  You see, when it does this, I want the
    # x velocity to reverse direction.  I then want this value retured.
    # If I have both the x and y velocity returned, calling these two returned numbers in the same function becomes problematic:
    # I esentially got two colour changes in a row because I called the block_colour_change funtion twice.
    # Thus, I am doing 1 function for x colour change, and another for y colour change
        
    def block_colour_change_x(self, create_blocks, ball_x_velocity, ballx, bally):
            

        for i in range(0, len(self.blockx)):
            
            
            # if ball travelling right and hits left edge            
            if ball_x_velocity >= 0 and \
                ballx + 2*ball_radius >= self.blockx[i] and \
                ballx +2*ball_radius <= self.blockx[i] + ball_x_velocity and \
                bally + 2*ball_radius >= self.blocky[i] and \
                bally <= self.blocky[i] + self.block_width:
                
                    ball_x_velocity *= -1
                    ballx += ball_x_velocity
                    bally += ball_y_velocity
                    print ("ball x velocity after bounce: ", ball_x_velocity)
                    colour_change = 'initiate'

            # if ball travelling left and hits right edge
            elif ball_x_velocity < 0 and \
                ballx >= self.blockx[i] + self.block_length + ball_x_velocity and \
                ballx <= self.blockx[i] + self.block_length and \
                bally + 2*ball_radius >= self.blocky[i] and \
                bally <= self.blocky[i] + self.block_width:
            
                    ball_x_velocity *= -1
                    ballx += ball_x_velocity
                    bally += ball_y_velocity
                    print ("ball x velocity after bounce: ", ball_x_velocity)
                    colour_change = 'initiate'
                    
            
            # if no hit, then we won't have a colour change
            else:
                    colour_change = 'deactivate'
                    
                    
            # now, if there was a hit, (i.e. colour_change is set to 'initiate', then I went the block to actually change colour)
            if colour_change == 'initiate':
                
                colour_change = 'deactivate' # once in if statement, immediately deactivate colour change to ensure 1 colour change at a time
                
                
                # if block colour is red and is hit, then first turn yellow
                if self.block_colour[i] == 'red':
                    self.sub_block[i].fill(YELLOW)
                    self.block_colour[i] = 'yellow'
                    print ('block colour: ', self.block_colour[i])
                    
                elif self.block_colour[i] == 'yellow':
                    self.sub_block[i].fill(GREEN)
                    self.block_colour[i] = 'green'
                    print ('block colour: ', self.block_colour[i])
                    

               
               # if block colour is green (i.e. already having being hit twice), and is hit again, then 'remove' block from window
                elif self.block_colour[i] == 'green':
                    
            
                    # this puts the block position outside the observable window
                    self.blockx[i] = -100
                    self.blocky[i] = -100
                    
                    # shrink block and sub-block to zero size
                    self.block[i] = pygame.Surface([0,0])
                    self.sub_block[i] = pygame.Surface([0,0])
                    
                    # take 1 from block_count number                    
                    self.block_count -= 1
                    print ("Blocks remaining: ", self.block_count)   # just for de-bugging - shows the number of remaining blocks now
                    
            
        # give our new reversed x velocity which we shall use later
        return ball_x_velocity
                    
        


            
    # Same for y 
            
    def block_colour_change_y(self, create_blocks, ball_y_velocity, ballx, bally):   

        for i in range(0, len(self.blockx)):        
            
            # if travelling down and ball hits top of a block            
            if ball_y_velocity >= 0 and \
                bally + 2*ball_radius >= self.blocky[i] and \
                bally + 2*ball_radius <= self.blocky[i] + ball_y_velocity and \
                ballx + 2*ball_radius >= self.blockx[i] and \
                ballx <= self.blockx[i] + self.block_length:
    	
                    ball_y_velocity *= -1
                    ballx += ball_x_velocity
                    bally += ball_y_velocity
                    print ("ball y velocity after bounce: ", ball_y_velocity)
                    colour_change = 'initiate'
    
            # if ball travelling up and hits bottom of a block
            elif ball_y_velocity < 0 and \
                bally >= self.blocky[i] + self.block_width + ball_y_velocity and \
                bally <= self.blocky[i] + self.block_width and \
                ballx + 2*ball_radius >= self.blockx[i] and \
                ballx <= self.blockx[i] + self.block_length:
                
                    ball_y_velocity *= -1
                    ballx += ball_x_velocity
                    bally += ball_y_velocity
                    print ("ball y velocity after bounce: ", ball_y_velocity)
                    colour_change = 'initiate'
                    
    
            else:
                    colour_change = 'deactivate'
                    
                    
            if colour_change == 'initiate':
                
                colour_change = 'deactivate'
                
                
                # if block colour is red and is hit, then first turn yellow
                if self.block_colour[i] == 'red':
                    self.sub_block[i].fill(YELLOW)
                    self.block_colour[i] = 'yellow'
                    print ('block colour: ', self.block_colour[i])
                    
                elif self.block_colour[i] == 'yellow':
                    self.sub_block[i].fill(GREEN)
                    self.block_colour[i] = 'green'
                    print ('block colour: ', self.block_colour[i])
                    

               
               # if block colour is green (i.e. already having being hit twice), and is hit again, then 'remove' block from window
                elif self.block_colour[i] == 'green':
                    
            
                    # this puts the block position outside the observable window
                    self.blockx[i] = -100
                    self.blocky[i] = -100
                    
                    # shrink block and sub-block to zero size
                    self.block[i] = pygame.Surface([0,0])
                    self.sub_block[i] = pygame.Surface([0,0])
                    
                    # take 1 from block_count number                    
                    self.block_count -= 1
                    print ("Blocks remaining: ", self.block_count)   # just for de-bugging - shows the number of remaining blocks now
                    
                
        # now return new reversed y velocity
        return ball_y_velocity
        

        
    
    
    # This function I am deliberating about keeping in this class.  It's purpose is if the block_count reaches zero, then to throw a 
    # success message and then end the game
    # It takes in the block_colour_change function (to pass the block_count to it)
    def get_completed_status(self, block_colour_change_x, block_colour_change_y):
        
        if self.block_count == 0:
            self.textSurfaceObj = fontObj.render('WELL DONE!', True, WHITE) # our success message
            print ("Level complete!")
    
            
            # The following just display the success message, the ball, bar and blocks to the screen when we complete the game        
            
            DISPLAYSURF.blit(self.textSurfaceObj, textRectObj) # copy message to DISPLAYSURF, our screen
            DISPLAYSURF.blit(bar, (barx, bary)) # copies bar to DISPLAYSURF
            DISPLAYSURF.blit(ball, (ballx, bally)) # copies ball to DISPLAYSURF
            DISPLAYSURF.blit(textSurfaceObj2, textRectObj2) # copies quit instruction to DISPLAYSURF
            for i in range (0, len(level_number.blockx)):
                DISPLAYSURF.blit(self.block[i], (self.blockx[i], self.blocky[i])) # copies blocks to DISPLAYSURF
                DISPLAYSURF.blit(self.sub_block[i], (self.blockx[i]+1, self.blocky[i]+1)) # copies sub-blocks to DISPLAYSURF
            pygame.display.update() # show on screen
            pygame.time.wait(2000) # pause this many milliseconds
            pygame.quit() # quit game
            sys.exit()
        
        
        
        
# random number function to give number between two values
def my_random_number(lower, upper):
    r = round(rm.random() * (upper-lower) + lower, 3)
    return r
 

# If the user doesn't pass level, then give a fail message.
# Might integrate into above class function get_completed_state
def level_fail():

    textSurfaceObj = fontObj.render('FAIL!', True, WHITE) # our fail message
    print ('Level failed!')
    
    DISPLAYSURF.blit(textSurfaceObj, textRectObj) # copy message to DISPLAYSURF
    DISPLAYSURF.blit(bar, (barx, bary)) # copies bar to DISPLAYSURF
    DISPLAYSURF.blit(ball, (ballx, bally)) # copies ball to DISPLAYSURF
    DISPLAYSURF.blit(textSurfaceObj2, textRectObj2) # copies quit instruction to DISPLAYSURF
    for i in range (0, len(level_number.blockx)):
        DISPLAYSURF.blit(level_number.block[i], (level_number.blockx[i], level_number.blocky[i])) # copies blocks to DISPLAYSURF
        DISPLAYSURF.blit(level_number.sub_block[i], (level_number.blockx[i]+1, level_number.blocky[i]+1)) # copies sub-blocks to DISPLAYSURF
    pygame.display.update() # show on screen
    pygame.time.wait(1000) # pause this many milliseconds
    pygame.quit() # quit game
    sys.exit()






'''Right, now we have declared our class and functions, let's set up the game'''

# initiate game
pygame.init()


FPS = 30 # frames per second
fpsClock = pygame.time.Clock()


# set up the user window
screen_pixel_width = 600
screen_pixel_height = 400
DISPLAYSURF = pygame.display.set_mode((screen_pixel_width, screen_pixel_height)) # size of screen
pygame.display.set_caption('Block Breaker') # heading on screen


# set up the colours for our game
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (175, 0, 0)
GREEN = (0, 155, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 200, 200)
YELLOW = (255, 255, 0)
AWESOME_COLOUR = GREEN
TRANSPARENT_COLOUR = (0, 0, 0, 0)

background_colour = BLACK # needed as want screen and box surrounding ball to be the same colour
block_border_colour = WHITE

# I want my background to be a nice picture, which I took off the internet
#background = pygame.image.load('bckrd.jpg')


# welcome message
fontObj = pygame.font.SysFont("arial", 50)
textSurfaceObj1 = fontObj.render('BLOCK BREAKER', True, WHITE)
textSurfaceObj = fontObj.render('Press left arrow key to start.', True, WHITE)
textRectObj1 = textSurfaceObj1.get_rect()
textRectObj = textSurfaceObj.get_rect()
textRectObj1.center = (215, 250)
textRectObj.center = (300, 300)

# How to quit game
fontObj2 = pygame.font.SysFont("arial", 15)
textSurfaceObj2 = fontObj2.render('q = quit game', True, WHITE)
textRectObj2 = textSurfaceObj1.get_rect()
textRectObj2.center = (screen_pixel_width+80, 30)

############################################
# NOW SET UP OUR OTHER OBJECTS IN THE GAME #
############################################

# Maybe these could be classes later on as well

# User-moved bar at the bottom
bar_length = 100
bar_width = 15
barx = screen_pixel_width - bar_length - 50
bary = screen_pixel_height - bar_width - 35
bar = pygame.Surface([bar_length, bar_width])
bar.fill(AWESOME_COLOUR)

# Moving ball
ball_radius = 15
ballx = screen_pixel_width - 2*ball_radius - my_random_number(0, screen_pixel_width-2*ball_radius)
bally = ball_radius + my_random_number(110, 110)
ball_x_velocity = my_random_number(5,8)
ball_y_velocity = my_random_number(5,8)
ball = pygame.Surface([ball_radius*2, ball_radius*2])
ball.fill(TRANSPARENT_COLOUR) # ensures box surrounding circle is background colour
ball.set_colorkey(TRANSPARENT_COLOUR)
pygame.draw.circle(ball, GREEN, (ball_radius, ball_radius), ball_radius)

# Our blocks, which we are now calling
level_number = Block_objects(level)
level_number.block_positions()
level_number.create_blocks(level_number.block_positions)





##################
# MAIN GAME LOOP #
##################

# some initial states of our variables
beginning = 'yes'
colour_change = 'deactivate'


while True:
    
    #DISPLAYSURF.blit(background, (0,0))
    DISPLAYSURF.fill(background_colour)

    
    #if level == 3:
        #DISPLAYSURF.blit(level_number.cat, (50,50))
    
    
    # I want the use to have to press the left key to start the game.  This will tell the user to do so.
    if beginning == 'yes':
        DISPLAYSURF.blit(textSurfaceObj1, textRectObj1)        
        DISPLAYSURF.blit(textSurfaceObj, textRectObj)
        DISPLAYSURF.blit(textSurfaceObj2, textRectObj2)
        for event in pygame.event.get():
        
            # if user presses a key:
            if event.type == pygame.KEYDOWN:

                # if user presses left key, move bar left only if it won't go outside the screen
                if event.key == pygame.K_LEFT:
                    beginning = 'no'
                    
                # if user presses q key, then quit game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                    
    elif beginning == 'no':
        # make ball move in time    
        ballx += ball_x_velocity
        bally += ball_y_velocity
        
        

    
    
    
    # get numbers from block_colour_change functions in our class and set to variables 
    ball_y_velocity_from_class = level_number.block_colour_change_y(level_number.create_blocks, ball_y_velocity, ballx, bally)
    ball_x_velocity_from_class = level_number.block_colour_change_x(level_number.create_blocks, ball_x_velocity, ballx, bally)

    
    
        
    if ball_y_velocity == - ball_y_velocity_from_class and abs(ball_y_velocity) > 0: # if y vecloity from class is minus that of ball_y_velocity, then we have hit a block
        ball_y_velocity = ball_y_velocity_from_class # so rename ball_y_velocity with this new negative velovity
        bally += ball_y_velocity # and update
        level_number.get_completed_status(level_number.block_colour_change_x, level_number.block_colour_change_y)
        
    elif ball_x_velocity == - ball_x_velocity_from_class and abs(ball_x_velocity) > 0: # if x vecloity from class is minus that of ball_x_velocity, then we have hit a block
        ball_x_velocity = ball_x_velocity_from_class # so rename ball_x_velocity with this new negative velovity
        ballx += ball_x_velocity # and update
        level_number.get_completed_status(level_number.block_colour_change_x, level_number.block_colour_change_y)


                    
                    
    
    # if ball hits left or right sides, then reverse x velocity
    # NOTE shape co-ordinates (e.g. ballx, bally) are always for top-left corner
    if ballx + 2*ball_radius >= screen_pixel_width or ballx < 0:
        ball_x_velocity *= -1
        ballx += ball_x_velocity
    
    # if ball hits top of screen, reverse its y velocity    
    if bally < 0:
        ball_y_velocity *= -1
        bally += ball_y_velocity
        
        
        
    
    # if top of ball hits bar below the top of the bar, reverse x velocity (solves bug)
    if  ball_x_velocity > 0 and bally >= bary and ballx + 2*ball_radius + abs(ball_x_velocity) >= barx and ballx - abs(ball_x_velocity) <= barx + bar_length:
        #ballx = barx - 2*ball_radius - 2        
        ball_x_velocity *= -1
        ball_y_velocity = 5
        
    elif  ball_x_velocity < 0 and bally >= bary and ballx + 2*ball_radius + abs(ball_x_velocity) >= barx and ballx - abs(ball_x_velocity) <= barx + bar_length:
        #ballx = barx + bar_length + 2        
        ball_x_velocity *= -1
        ball_y_velocity = 5
        
    # if ball hits bar, then reverse its y velocity and change its x-velocity depending where it hits on the bar
        
    elif ballx + 2*ball_radius > barx and ballx < barx + bar_length and bally + 2*ball_radius >= bary:
        ball_y_velocity *= -1
        bally += ball_y_velocity
        
        #x_velocity_change = [0.1*i**2 for i in range(int(-bar_length/2), int(1+bar_length/2))]
        #print (x_velocity_change)
        
        # if going right and ball is within 1/6 of bar length, then reverse x velocity
        if ballx + ball_radius <= barx + bar_length/6 and ball_x_velocity > 0:
            if ball_x_velocity < 8: # if x velocity magnitude small, then increase its magnitude and reverse its direction
                ball_x_velocity = -ball_x_velocity*1.5
            else:
                ball_x_velocity *= -1 # if x velocity magnitude large, then just reverse its direction

        # if going left and ball is more than 1/6 of bar length along, then reverse x velocity
        elif ballx + ball_radius >= barx + 5*bar_length/6 and ball_x_velocity < 0:
            if ball_x_velocity > -8:
                ball_x_velocity = -ball_x_velocity*1.5
            else:
                ball_x_velocity *= -1

        
        
        # if going right and ball is between 1/6 and 2.5/6 of bar length, then half reverse x velocity
        elif ballx + ball_radius > barx + bar_length/6 and ballx + ball_radius < barx + 2.5*bar_length/6 and ball_x_velocity > 0:
            ball_x_velocity = -0.5*ball_x_velocity
            
        # if going left and ball is between 3.5/6 and 5/6 of bar length, then half reverse x velocity
        elif ballx + ball_radius > barx + 3.5*bar_length/6 and ballx + ball_radius < barx + 5*bar_length/6 and ball_x_velocity < 0:
            ball_x_velocity = -0.5*ball_x_velocity
        
        
        
        # if in middle 1/6, then bounce ball straigtht back up
        elif ballx + ball_radius >= barx + 2.5*bar_length/6 and ballx + ball_radius <= barx + 3.5*bar_length/6 and abs(ball_x_velocity) > 0:
            ball_x_velocity = 0
        
        
        # these ensure that if it bounces straight up, then on the next bounce it can angle off again        
        elif abs(ball_x_velocity) < 2: 
            
            if ballx + ball_radius <= barx + bar_length/6:
                ball_x_velocity = -6
            
            elif ballx + ball_radius >= barx + 5*bar_length/6:
                ball_x_velocity = 6
            
            elif ballx + ball_radius > barx + bar_length/6 and ballx + ball_radius < barx + 2.5*bar_length/6:
                ball_x_velocity = -3
                
            elif ballx + ball_radius > barx + 3.5*bar_length/6 and ballx + ball_radius < barx + 5*bar_length/6:
                ball_x_velocity = 3
        
            
    # if ball sinks below bar, end game       
    if bally >= bary + bar_width:
        level_fail()
        

  
    # Now let's look for events the user does in the game (e.g. key presses)   
    for event in pygame.event.get():
        
        # if user presses a key:
        if event.type == pygame.KEYDOWN:

            # if user presses left key, move bar left only if it won't go outside the screen
            if event.key == pygame.K_LEFT and barx - bar_length/2 >= 0: # remember barx refers to LHS of bar, not centre
                barx -= 50
            
            # if user presses right key, move bar right only if it won't go outside the screen            
            if event.key == pygame.K_RIGHT and barx + bar_length < screen_pixel_width:
                barx += 50
            
            # if user presses up key, increase ball_y_velocity up to a certain limit     
            if event.key == pygame.K_UP and abs(ball_y_velocity) < 10:
                ball_y_velocity *= 1.5
                ball_x_velocity *= 1.1
             
            # if user presses down key, decrease ball_y_velocity down to a certain limit 
            if event.key == pygame.K_DOWN and abs(ball_y_velocity) > 2:
                ball_y_velocity *= 0.5
                ball_x_velocity *= 0.7
            
            # if user presses q key, then quit game  
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
                
                
                
        # if statment for ending game        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    # Copy the bocks, ball and bar to the screen
    DISPLAYSURF.blit(bar, (barx, bary)) # copies bar to DISPLAYSURF
    DISPLAYSURF.blit(ball, (ballx, bally)) # copies ball to DISPLAYSURF
    DISPLAYSURF.blit(textSurfaceObj2, textRectObj2) # copies quit instruction to DISPLAYSURF
    for i in range (0, len(level_number.blockx)):
        DISPLAYSURF.blit(level_number.block[i], (level_number.blockx[i], level_number.blocky[i])) # copies blocks to DISPLAYSURF
        DISPLAYSURF.blit(level_number.sub_block[i], (level_number.blockx[i]+1, level_number.blocky[i]+1)) # copies sub-blocks to DISPLAYSURF # copies sub-blocks to DISPLAYSURF
   
    pygame.display.update() # makes display surfaces actually appear on monitor
    fpsClock.tick(FPS) # wait FPS number of frames before drawing the next frame
    
   



