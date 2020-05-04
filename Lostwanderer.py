import random
import pygame
import math
from Buttons import Button
import matplotlib

#initializing
pygame.init()
clock = pygame.time.Clock()
screenSize = 700
screen = pygame.display.set_mode((screenSize,screenSize))
pygame.display.set_caption("Lostwanderer 1.0")
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (127,127,127)



class wanderer:
    """define the start position x,y,velocity, and canvas to draw the images on"""
    def __init__(self,x,y,vel,canvas = screen):
        self.x = x
        self.y = y
        self.vel = vel
        self.xstart = x
        self.ystart = y
        self.canvas = canvas
        # record furtherst distance from centre, used for radius of circle
        self.distance_max = 0
        # record step count since start of run
        self.stepCount = 0
        # record all the positions, draw them in every frame
        self.positionSet = set()

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

    def update_position_and_distance_and_stepCount(self):
        # Add more position to position set
        self.positionSet.add((self.x,self.y))
        #update max distance
        if self.distance_from_start() > self.distance_max:
            self.distance_max = self.distance_from_start()
        self.stepCount += 1

    def display(self):
        """shows all the position that the lost wanderer has been to and the furthest distance"""
        for n in self.positionSet:
            pygame.draw.rect(self.canvas, (255, 255, 255), (n[0], n[1], 1, 1))
        pygame.draw.circle(self.canvas, (0, 255, 0), (int(self.xstart), int(self.ystart)), int(self.distance_max), 1)
        #arbitrary rectangle to mark the beginning point
        pygame.draw.rect(screen, (255, 0, 0), (Jerry.xstart - 2, Jerry.ystart - 2, 5, 5))

    def clearData(self):
        """clear all data in the current instance, (for new run)"""
        self.positionSet = set()
        self.distance_max = 0
        self.x = self.xstart
        self.y = self.ystart
        self.stepCount = 0

Jerry = wanderer(screenSize/2,screenSize/2,2)

def showWord(text,position,colour = WHITE, size = 20):
    myFont = pygame.font.SysFont("Times New Roman", size)
    myText = myFont.render(text,True,colour)
    screen.blit(myText,position)

def isIn(coordinates, area):
    """used to determine whether a coordinates has both its x and y values within the range of area that we want,boundary inclusive
    area should be tuple of tuple((xmin,xmax),(ymin,ymax))"""
    return coordinates[0]>= area[0][0] and coordinates[0] <= area[0][1] and coordinates[1]>= area[1][0] and coordinates[1] <= area[1][1]

#runPage
def stepChange():
    Jerry.randommove()
    Jerry.update_position_and_distance_and_stepCount()

def update():
    screen.fill((0,0,0))
    Jerry.display()
    showWord("A lost wanderer is moving two pixels per step.", (20, 50), size = 18)
    showWord("The green circle indicates the furthest distance", (20, 70), size = 18)
    showWord("from the initial position.", (20, 90), size = 18)
    showWord("Steps:" + "    " + str(Jerry.stepCount), (screenSize - 200, 50))
    showWord("Max Distance:" + str(round(Jerry.distance_max,2)), (screenSize - 200, 80))
    for button in runButtons:
        button.show()
    pygame.display.update()

button1 = Button(screen,screenSize - 100, screenSize - 50, 60, 30, WHITE, GREY, BLUE, textcolour = BLACK, textcolour2 = BLACK, TEXT = "Return")
button5 = Button(screen,screenSize - 100, screenSize - 100, 60, 30, WHITE, GREY, BLUE, textcolour = BLACK, textcolour2 = BLACK, TEXT = "Pause")
runButtons = [button1,button5]

#startPage
def startUpdate():
    screen.fill((0,0,0))
    for button in startButtons:
        button.show()
    pygame.display.update()

button2 = Button(screen,screenSize/2, screenSize/2 - 50, 150, 40, WHITE, GREY, BLUE, textcolour = BLACK, textcolour2 = BLACK, TEXT = "Start")
button3 = Button(screen,screenSize/2, screenSize/2, 150, 40, WHITE, GREY, BLUE, textcolour = BLACK, textcolour2 = BLACK, TEXT = "Settings")
button4 = Button(screen,screenSize/2, screenSize/2 + 50, 150, 40, WHITE, GREY, BLUE, textcolour = BLACK, textcolour2 = BLACK, TEXT = "Quit")
startButtons = [button2,button3,button4]

#pausePage
def pauseContent():
    pygame.draw.rect(screen, GREY, (0, screenSize - 120, screenSize, 120))
    showWord("Paused", (screenSize / 2 - 25, screenSize - 80), WHITE)
    showWord("Click anywhere to resume", (screenSize / 2 - 100, screenSize - 40), WHITE)
    pygame.display.update()
    pygame.time.delay(500)

startPage = True
runPage = False
settingsPage = False
pausePage = False
fps = 20

run = True
while run:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if runPage:
        stepChange()
        update()
        if button1.leftClicked():
            fps = 20
            runPage = False
            startPage = True
            Jerry.clearData()
        if button5.leftClicked():
            #pause button, content updated only once
            fps = 20
            runPage = False
            pausePage = True
            pauseContent()

    elif startPage:
        startUpdate()
        if button2.leftClicked():
            runPage = True
            startPage = False
            fps = 100
        if button3.leftClicked():
            pass
        if button4.leftClicked():
            run = False

    elif settingsPage:
        pass

    elif pausePage:
        if pygame.mouse.get_pressed()[0] and isIn(pygame.mouse.get_pos(),((0,screenSize),(0,screenSize))):
            pausePage = False
            runPage = True
            fps = 100


