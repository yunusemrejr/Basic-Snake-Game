import sys, random, pygame
from time import time, sleep
pygame.display.set_caption('Snake Game')
icon = pygame.image.load('gameico.png')
pygame.display.set_icon(icon)

class Player():
    def __init__(this):
        this.length = 1
        this.positions=[( (screen_width/2), (screen_height/2))]
        this.direction= random.choice( [up,down,right,left] )
        this.color=(51,0,102)
        this.score=0
    
    def get_head_position(this):
        return this.positions[0]
    
    def turn(this, point):
        if this.length > 1 and (point[0]*-1, point[1]*-1)==this.direction:
            return
        else:
            this.direction= point

    def move(this):
        headPosition = this.get_head_position()
        x,y=this.direction
        newP = (((headPosition[0]+(x*gridsize))%screen_width), (headPosition[1]+(y*gridsize))%screen_height)
        if len(this.positions) > 2 and newP in this.positions[2:]:
            this.reset()
        else:
            this.positions.insert(0,newP)
            if len(this.positions)>this.length:
                this.positions.pop()
    
    def reset(this):
        this.length=1
        this.positions=[((screen_width/2),(screen_height/2))]
        this.direction=random.choice([up,down,left,right])
        this.score=0

    def draw(this,surface):
        for i in this.positions:
            r = pygame.Rect((i[0],i[1]),(gridsize,gridsize))
            pygame.draw.rect(surface, this.color,r)
            pygame.draw.rect(surface,this.color, r, 1)

    def handle_keys(this):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    this.turn(up)

            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_DOWN:
                    this.turn(down)
            
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    this.turn(left)

            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT:
                    this.turn(right)

            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_f:
                    this.turn(boost)


class Food():
    def __init__(this):
        this.position = (0,0)
        this.color = (255,0,0)
        this.randomize_position()

    def randomize_position(this):
        this.position = (random.randint(0, grid_width-1)*gridsize, random.randint(0, grid_height-1)*gridsize)

    def draw(this,surface):
        r = pygame.Rect((this.position[0],this.position[1]),(gridsize,gridsize))
        pygame.draw.rect(surface,this.color,r)
        pygame.draw.rect(surface,(74,167,237),r,1)

def drawGrid(surface):
        for y in range(0, int(grid_height)):
            for x in range(0, int(grid_width)):
                if(x+y)%2==0:
                    r= pygame.Rect((x*gridsize,y*gridsize),(gridsize,gridsize))
                    pygame.draw.rect(surface,(74,167,237),r)
                else:
                    rr=pygame.Rect((x*gridsize,y*gridsize),(gridsize,gridsize))
                    pygame.draw.rect(surface,(55,167,178),rr)

screen_width=680
screen_height=480
gridsize=20
grid_width=screen_width/gridsize
grid_height=screen_height/gridsize

up=(0,-1)
down=(0,1)
right=(1,0)
left=(-1,0)
boost=(3,0)

def first3Seconds():
    pygame.init()
    clock=pygame.time.Clock()
    screen=pygame.display.set_mode((screen_width, screen_height))
    surface=pygame.Surface(screen.get_size())
    surface=surface.convert()
    drawGrid(surface)
    snake=Player()
    food=Food()
    myfont = pygame.font.SysFont("times",54)

    while(1):
        clock.tick(20)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        screen.blit(surface,(0,0))
        text=myfont.render("WELCOME",1,(0,255,255))
        screen.blit(text,(66,155))
        pygame.display.update()
        sleep(3)
        main()

def main():
    pygame.init()
    clock=pygame.time.Clock()
    screen=pygame.display.set_mode((screen_width, screen_height))
    surface=pygame.Surface(screen.get_size())
    surface=surface.convert()
    drawGrid(surface)
    snake=Player()
    food=Food()
    myfont=pygame.font.SysFont("arial",13)

    while(1):
        clock.tick(20)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        if snake.get_head_position()==food.position:
            snake.length+=1
            snake.score +=1
            food.randomize_position()
            snake.draw(surface)
            snake.draw(surface)
            screen.blit(surface,(0,0))
            text=myfont.render("your score is: {0}".format(snake.score),1,(255,0,0))
            screen.blit(text,(15,10))
            pygame.display.update()

first3Seconds()  
            
