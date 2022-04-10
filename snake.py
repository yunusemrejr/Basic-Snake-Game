#we import necessary libraries pygame, sys, random. (pip install pygame)
#pygame is our gaming library which will make everything easier to build
#sys is our important module that makes it possible to manipulate Python runtime enviroment.
#random is our module to generate random numbers, it is a built-in python module.
import pygame,sys,random
from time import time, sleep #importing time for sleeping etc.
#setting window title for our game
pygame.display.set_caption('Basic Snake Game With Pygame - Yunus E.V.')
#setting window icon for our game
img = pygame.image.load('gameico.png')
pygame.display.set_icon(img)
#Player class is the class spesificly for our character/snake/player.
class Player():
    
    #def ----> defining a function
    #_init_ acts as a constructor here. 
    
    def __init__(this):
        
    #'this' has to be passed everytime here in order to make non-static methods.
        this.length = 1 #initial snake length is 1 (1 box only)
        this.positions = [((screen_width/2), (screen_height/2))]
        #direction definitions
        this.direction = random.choice([up,down,right,left])
        
        #color of player/snake ---> dark purple / #330066 / CSS : hsl(270, 100%, 20%)
        this.color = (51, 0, 102)
      
      #initial score / score count starting point
        this.score = 0 #stars from zero

    #method that gets position of snake's head
    def get_head_position(this):
        return this.positions[0]

    #changes rotation on command else continues on a straight line
    def turn(this, point):
        if this.length > 1 and (point[0]*-1, point[1]*-1) == this.direction:
            return
        else:
            this.direction = point
    
    #movement defimitions
    def move(this):
        headPosition = this.get_head_position()
        x,y = this.direction
        #updates head position on key stroke
        newP = (((headPosition[0]+(x*gridsize))%screen_width), (headPosition[1]+(y*gridsize))%screen_height)
        #determines when to call the reset module
        if len(this.positions) > 2 and newP in this.positions[7:]:
            this.reset()
        else:
            this.positions.insert(0,newP)
            if len(this.positions) > this.length:
                this.positions.pop()
                
#resets snake length to initial length
    def reset(this):
        this.length = 1
        this.positions = [((screen_width/2), (screen_height/2))]
        this.direction = random.choice([up, down, left, right])
        this.score = 0
#draws the background/surface
    def draw(this,surface):
        for p in this.positions:
            r = pygame.Rect((p[0], p[1]), (gridsize,gridsize))
            pygame.draw.rect(surface, this.color, r)
            pygame.draw.rect(surface, this.color, r, 1)
#defines keys and their actions
    def handle_keys(this):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
                #takes correct action on button pushes
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    this.turn(up)
                elif event.key == pygame.K_DOWN:
                    this.turn(down)
                elif event.key == pygame.K_LEFT:
                    this.turn(left)
                elif event.key == pygame.K_RIGHT:
                    this.turn(right)
                    #pressing the 'F' on keyboard will trigger a special linear boost effect for your snake. 
                elif event.key == pygame.K_f:
                    this.turn(boost)

#food class has modules that adjust the food
class Food():
    def __init__(this):
        this.position = (0,0)
        this.color = (255, 0, 0)
        this.randomize_position()

    def randomize_position(this):
        this.position = (random.randint(0, grid_width-1)*gridsize, random.randint(0, grid_height-1)*gridsize)
#draws the food on the surface
    def draw(this, surface):
        r = pygame.Rect((this.position[0], this.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, this.color, r)
        pygame.draw.rect(surface, (74, 167, 237), r, 1)

def drawGrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x+y)%2 == 0:
                r = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface,(74, 167, 237), r)
            else:
                rr = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface, (55, 167, 178), rr)
#screen width and height
screen_width = 680
screen_height = 480
#gridsize determines the grid's size and kind of makes a zoom-in out style. if set high, zooms in, if low, zooms out.
gridsize = 20
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)
boost = (3,0) #special linear boost effect. Makes the snake go crazy

def first3Seconds():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height))

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Player()
    food = Food()

    myfont = pygame.font.SysFont("times",54)  

    while (True):  
        clock.tick(20)  
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        screen.blit(surface, (0,0))
        text = myfont.render("WELCOME TO SNAKE", 1, (0,225,225)) #lightblue
        screen.blit(text, (66,155)) 
        pygame.display.update()
        sleep(3)
        main()

#END OF INTRO FUNCTION

#BEGINNING OF GAME / MAIN

def main(): #starts all the functions , main function
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height))

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Player()
    food = Food()

    myfont = pygame.font.SysFont("arial",14) #score label display style

    while (True): #while loop makes it possible to make game run continuesly until an action is taken by the user
        clock.tick(20) #how fast our snake is
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        #if snake and food go on the same location, add snake a new box/ increase our length
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            #calls the randomize position module to randomly put the new foot on our screen
            food.randomize_position()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0,0))
        #score display text, starts from 0
        text = myfont.render("Your Score is : {0}".format(snake.score), 1, (255,0,0))
        screen.blit(text, (15,10)) #places the socre label on top left corner
        pygame.display.update()

first3Seconds() #CALLING THE INTRO FUNCTION ON CODE EXECUTION



#Yunus Emre Vurgun 2022

#Special thanks to Kite's YT channel and tutorial.