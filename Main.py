import pygame as pg
from pygame.locals import *
import sys
import pygame.mouse as mouse
import Constants
import robot
import pygame.font as font

# Set up the screen
screen = pg.display.set_mode((720, 720), HWACCEL | HWSURFACE | DOUBLEBUF)
# Set a caption and an icon
pg.display.set_caption("Odometry Simulator v1.2")
pg.display.set_icon(Constants.iconImage)

# Set up the font module
font.init()

# Get a font from the system
our_font = pg.font.SysFont("Arial", 13)

# Define the starting text position
starting_text_pos = (540, 15)
# This will be the (mutable) position of the next text to be drawn
text_pose = list(starting_text_pos)

# Make a new surface with the same dimensions as the screen
text_surface = pg.Surface((720, 720))

# Define the black color
black = (0, 0, 0)

# Make an object of the robot
robotObject = robot.Robot()

# Get a clock object
clock = pg.time.Clock()

# Store how many times we've looped
loopNums = 0

# Store the runtime
runtime = 0


# Check to see if the window has been "x-ed" out
def check_for_window_exit(event_list):
    for event in event_list:
        if event.type == QUIT:
            sys.exit()


# Check to see if the escape key has been pressed
def check_for_key_exit(key_list):
    if key_list[K_ESCAPE]:
        sys.exit()


# If the user left clicks, send robot to the starting position
def check_for_reset():
    pressed = mouse.get_pressed()
    if pressed[0]:  # Check for left click
        robotObject.x = 0  # Set the robot to the starting position
        robotObject.y = 0
        robotObject.a = 0
        robotObject.odo_a = 0
        robotObject.odo_x = 0
        robotObject.odo_y = 0


# Add the given text to the screen
def add_text(text: str):
    text = our_font.render(text, False, (20, 255, 20))
    screen.blit(text, text_pose)
    text_pose[1] += 15


# You can't have half a pixel, so positions need to be in integers
def round_position(pos):
    new_pos = list(pos)
    new_pos[0] = round(new_pos[0], 2)
    new_pos[1] = round(new_pos[1], 2)
    return new_pos


# Make a String representing the values in a list
def str_list(num_list):
    new_str = ""
    for num in num_list:
        new_str += str(num)
        if not num_list.index(num) == num_list[len(num_list) - 1]:
            new_str += ", "
    return new_str


# Run for 30 minutes
while 1 and not (runtime / 1000) >= 1800:
    # Update the runtime
    runtime = pg.time.get_ticks()

    # Update events and keyboard events
    events = pg.event.get()
    keys = pg.key.get_pressed()

    # Check if we need to exit
    check_for_window_exit(events)
    check_for_key_exit(keys)

    # Check if we need to reset the robot position
    check_for_reset()

    # Inform the robot of the keys
    robotObject.update(keys)

    # Find the mouse position
    mouseRel = mouse.get_pos()

    # Draw the robot's path
    robotObject.path()

    # Fill the screen with black to start
    screen.fill(black)

    # Fill the screen with the background image
    screen.blit(Constants.backgroundImage, (0, 0))

    # Add all our data
    add_text("Paths Length: "+str(len(robotObject.paths)))
    add_text("Robot Position: "+str_list(round_position((robotObject.x, robotObject.y))))
    add_text("Odometry Position: "+str_list(round_position((robotObject.odo_x, robotObject.odo_y))))
    add_text("Robot Heading: "+str(round(robot.normalize_angle(robotObject.a), 2)))
    add_text("Odometry Heading: "+str(round(robot.normalize_angle(robotObject.odo_a), 2)))
    add_text("Runtime (sec): "+str(runtime / 1000))
    add_text("FPS (target = 60): "+str(round(clock.get_fps(), 2)))

    # Tell the robot object to draw itself
    robotObject.draw(screen)

    # Update what the user sees
    pg.display.flip()

    # Reset where the text goes for next time
    text_pose = list(starting_text_pos)

    # Tell Pygame we want 60 fps
    clock.tick(60)

    # Increment our loop number
    loopNums += 1

screen.fill(black)
text_pose[0] = 100
text_pose[1] = 360
our_font = pg.font.SysFont("Arial", 20, True)
add_text("FOR THE LOVE OF GOD DO SOMETHING ELSE IN YOUR LIFE!")
pg.display.flip()

while 1:

    # Update events and keyboard events
    events = pg.event.get()
    keys = pg.key.get_pressed()

    # Check if we need to exit
    check_for_window_exit(events)
    check_for_key_exit(keys)
