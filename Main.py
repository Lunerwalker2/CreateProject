import pygame as pg
from pygame.locals import *
import sys
import pygame.mouse as mouse
import Constants
import robot


# Set up the screen
screen = pg.display.set_mode((720, 720), HWACCEL | HWSURFACE | DOUBLEBUF)
pg.display.set_caption("Odometry Simulator v1.2")
pg.display.set_icon(Constants.iconImage)

mouse.set_pos(Constants.center)

mouseRel = mouse.get_pos()

# Define the black color
black = (0, 0, 0)

robotObject = robot.Robot()

clock = pg.time.Clock()

loopNums = 0


# Check to see if the window has been "x-ed" out
def checkForWindowExit(eventList):
    for event in eventList:
        if event.type == QUIT:
            sys.exit()


# Check to see if the escape key has been pressed
def checkForKeyExit(keylist):
    if keylist[K_ESCAPE]:
        sys.exit()


# If the user left clicks, send robot to the mouse
def checkForFollow():
    pressed = mouse.get_pressed()
    if pressed[0]:
        robotObject.x = 0
        robotObject.y = 0
        robotObject.a = 0
        robotObject.odo_a = 0
        robotObject.odo_x = 0
        robotObject.odo_y = 0


while 1:
    # Update events and keyboard events
    events = pg.event.get()
    keys = pg.key.get_pressed()

    # Check if we need to exit
    checkForWindowExit(events)
    checkForKeyExit(keys)

    checkForFollow()

    # Inform the robot of the keys
    robotObject.update(keys)

    # Find the mouse position
    mouseRel = mouse.get_pos()

    # Print the mouse position (DEBUG)
    print(str(mouseRel) + str((robotObject.x, robotObject.y)) + "Paths length: "+str(len(robotObject.paths)))

    if loopNums % 1 == 0:
        robotObject.path()

    # Fill the screen with black
    screen.fill(black)

    # Fill the screen with the image
    screen.blit(Constants.backgroundImage, (0, 0))

    # Tell the robot object to draw itself
    robotObject.draw(screen)

    # Update what the user sees
    pg.display.flip()

    clock.tick(60)
    loopNums += 1