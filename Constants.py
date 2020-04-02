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


backgroundFileName = "Images/stars.jpg"
iconFileName = "Images/icon.jpg"

backgroundFileOriginal = pg.image.load(backgroundFileName)
iconFileOriginal = pg.image.load(iconFileName)

backgroundImage = pg.transform.scale(backgroundFileOriginal, (720, 720))
iconImage = pg.transform.scale(iconFileOriginal, (32, 32))

