import pygame as pg

SCREENSIZE = 720
center = [SCREENSIZE / 2, SCREENSIZE / 2]

DAMPENING = 0.8
DAMPENING_A = 0.8
INCHES = 144

ROBOT_COLOR = [30, 250, 20]
LINE_COLOR = [23, 110, 230]
HEADING_COLOR = [255, 40, 40]

PIX_PER_INCH = SCREENSIZE // INCHES

# Store a constant for each field picture
FIELD = 0
STARS = 1

# The file names of the images
backgroundFileName = "Images/field-skystone-dark-fix.jpg"
iconFileName = "Images/icon.jpg"

# Get the original images
backgroundFileOriginal = pg.image.load(backgroundFileName)
iconFileOriginal = pg.image.load(iconFileName)

# We use a 720x720 screen, so scale the image to that
backgroundImage = pg.transform.scale(backgroundFileOriginal, (720, 720))
# The icon needs to be 32x32, so scale it as well
iconImage = pg.transform.scale(iconFileOriginal, (32, 32))


# Get the background image based on the selection
def get_background(index: int):
    if index == FIELD:
        return FIELD
    elif index == STARS:
        return STARS
