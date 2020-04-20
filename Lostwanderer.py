import random
import pygame
import math
from miscellaneous.Buttons import Button

#initializing
pygame.init()
clock = pygame.time.Clock()
screenSize = 800
screen = pygame.display.set_mode((screenSize,screenSize))
pygame.display.set_caption("Lostwanderer 1.0")
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (127,127,127)

stepCount = 0


class people:
    """define the start position x,y,velocity, and canvas to draw the images on"""
    def __init__(self,x,y,vel,canvas = screen):
        self.x = x
        self.y = y
        self.vel = vel
        self.xstart = x
        self.ystart = y
        self.canvas = canvas

    def moveright(self):
        self.x += self.vel
    def moveleft(self):
        self.x -= self.vel
    def moveup(self):
        self.y -= self.vel
    def movedown(self):
        self.y += self.vel

    def randommove(self):
        n = random.randint(0,3)
        if n == 0:
            self.moveright()
        elif n == 1:
            self.moveleft()
        elif n == 2:
            self.moveup()
        else:
            self.movedown()

    #Use Pythagoras to return distance from centre
    def distance_from_start(self):
        return math.sqrt((self.x - self.ystart)**2 + (self.y - self.ystart)**2)

    # record furtherst distance from centre, used for radius of circle
    distance_max = 0
    # record all the positions, draw them in every frame
    positionSet = set()

    def update_position_and_distance(self):
        self.positionSet.add((self.x,self.y))
        if self.distance_from_start() > self.distance_max:
            self.distance_max = self.distance_from_start()

    def display(self):
        """shows all the position that the lost wanderer has been to and the furthest distance"""
        for n in self.positionSet:
            pygame.draw.rect(self.canvas, (255, 255, 255), (n[0], n[1], 1, 1))
        pygame.draw.circle(self.canvas, (0, 255, 0), (int(self.xstart), int(self.ystart)), int(self.distance_max), 1)

Jerry = people(screenSize/2,screenSize/2,2)

def showWord(text,position,colour = WHITE, size = 20):
    myFont = pygame.font.SysFont("Times New Roman", size)
    myText = myFont.render(text,True,colour)
    screen.blit(myText,position)

def stepChange():
    Jerry.randommove()
    Jerry.update_position_and_distance()
    global stepCount
    stepCount += 1
def update():
    screen.fill((0,0,0))
    Jerry.display()
    pygame.draw.rect(screen,(255,0,0),(Jerry.xstart - 2,Jerry.ystart - 2,5,5))
    showWord("A lost wanderer is moving two pixels per step.", (20, 50), size = 18)
    showWord("The green circle indicates the furthest distance from the initial position.", (20, 70), size = 18)
    showWord("Steps:" + "    " + str(stepCount), (screenSize - 200, 50))
    showWord("Max Distance:" + str(round(Jerry.distance_max,2)), (screenSize - 200, 80))
    button1.show()
    pygame.display.update()
    if button1.leftClicked():
        global runPage
        global startPage
        runPage = False
        startPage = True
button1 = Button(screen,screenSize - 100, screenSize - 50, 60, 30, WHITE, GREY, BLUE, textcolour = BLACK, textcolour2 = BLACK, TEXT = "Return")
startButton = []

def startPage():
    screen.fill((0,0,0))
    button2.show()
    button3.show()
    button4.show()
    pygame.display.update()
    if button2.leftClicked():
        global runPage
        global startPage
        runPage = True
        startPage = False
    if button3.leftClicked():
        pass
    if button4.leftClicked():
        global run
        run = Fasle


button2 = Button(screen,screenSize/2, screenSize/2 - 50, 150, 40, WHITE, GREY, BLUE, textcolour = BLACK, textcolour2 = BLACK, TEXT = "Start")
button3 = Button(screen,screenSize/2, screenSize/2, 150, 40, WHITE, GREY, BLUE, textcolour = BLACK, textcolour2 = BLACK, TEXT = "Instructions")
button4 = Button(screen,screenSize/2, screenSize/2 + 50, 150, 40, WHITE, GREY, BLUE, textcolour = BLACK, textcolour2 = BLACK, TEXT = "Quit")

startPage = True
runPage = False
settingPage = False

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if runPage:
        clock.tick(100)
        stepChange()
        update()

    elif startPage:
        clock.tick(50)
        screen.fill((0, 0, 0))
        button2.show()
        button3.show()
        button4.show()
        pygame.display.update()
        if button2.leftClicked():
            runPage = True
            startPage = False
        if button3.leftClicked():
            pass
        if button4.leftClicked():
            run = False

    elif infoPage:
        pass
