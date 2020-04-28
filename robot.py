import math
import pygame as pg
from pygame.locals import *
import random

import Constants


# Normalizes a given angle to Euler angles
def normalize_angle(angle: float):
    while angle >= math.pi:
        angle -= math.pi * 2
    while angle < -math.pi:
        angle += math.pi * 2
    return angle


class Robot:
    def __init__(self):
        self.width = 18
        self.enc_di = 1

        self.x = 0
        self.y = 0
        self.a = 0

        self.line_buffer = 1000

        self.vel_x = 0
        self.vel_y = 0
        self.vel_a = 0

        self.enc_l = 0
        self.enc_r = 0
        self.enc_c = 0

        self.paths = []

        self.odo_x = 0
        self.odo_y = 0
        self.odo_a = 0

    def update(self, keys):

        # Check all keys for robot motion
        if keys[K_w]:
            self.vel_x += math.cos(self.a) / 2
            self.vel_y += math.sin(self.a) / 2
        if keys[K_s]:
            self.vel_x += math.cos(self.a + math.pi) / 2
            self.vel_y += math.sin(self.a + math.pi) / 2
        if keys[K_a]:
            self.vel_x += math.cos(self.a - (math.pi / 2)) / 2
            self.vel_y += math.sin(self.a - (math.pi / 2)) / 2
        if keys[K_d]:
            self.vel_x += math.cos(self.a + (math.pi / 2)) / 2
            self.vel_y += math.sin(self.a + (math.pi / 2)) / 2

        # Check for robot rotation
        if keys[K_LEFT]:
            self.vel_a -= 0.05 / 2
        if keys[K_RIGHT]:
            self.vel_a += 0.05 / 2

        # Check to change the size of the line buffer length
        if keys[K_PAGEUP]:
            self.line_buffer = 1000
        elif keys[K_PAGEDOWN]:
            self.line_buffer = 700

        # Normalize the rotational velocity with the velo vector
        self.vel_a += (random.randint(-100, 100) / 1000000 * math.sqrt(self.vel_x ** 2 + self.vel_y ** 2))
        self.a += self.vel_a / 2

        # Simulate the encoder inputs (assuming three wheels, two y and one x)
        # Rotate our vector
        self.enc_c -= (self.vel_x * math.sin(self.a)) - (self.vel_y * math.cos(self.a))
        self.enc_l += (self.vel_x * math.cos(self.a)) + (self.vel_y * math.sin(self.a)) + (
                    (self.vel_a / (2 * math.pi)) * (self.width * math.pi))
        self.enc_r += (self.vel_x * math.cos(self.a)) + (self.vel_y * math.sin(self.a)) - (
                    (self.vel_a / (2 * math.pi)) * (self.width * math.pi))

        # Translate our position
        self.x += self.vel_x
        self.y += self.vel_y
        self.a += self.vel_a / 2
        # print(self.enc_c, self.enc_l, self.enc_r)

        # We don't want to become the Flash, so let's slow down a bit
        self.vel_x *= Constants.DAMPENING
        self.vel_y *= Constants.DAMPENING
        self.vel_a *= Constants.DAMPENING_A

        # Start trimming the path list if it gets too big
        if len(self.paths) >= self.line_buffer:
            del self.paths[0]

    # This method actually uses odometry to estimate our position
    def path(self):
        """
        Two points make a line, and we need to get both. The first point is our original position.
        The second is our position after we find it with the new encoder values.

        """

        # Store our old pose before finding a new one
        old = (self.odo_x, self.odo_y, self.odo_a)

        # Find the average y encoder value
        dc = ((self.enc_r + self.enc_l) / 2)
        # Find our "phi" (heading change) by finding the difference of the y encoders and dividing by the width
        ph = (self.enc_l - self.enc_r) / self.width

        # Next we can find our new position by adding where we are by how much we have moved.
        # We know how much we have gone relative to the robot, but we need relative to the field
        # To do this, we can apply a rotation vector

        self.odo_x += dc * math.cos(self.odo_a + (ph / 2)) - self.enc_c * math.sin(self.odo_a + (ph / 2))
        self.odo_y += dc * math.sin(self.odo_a + (ph / 2)) + self.enc_c * math.cos(self.odo_a + (ph / 2))
        self.odo_a += ph

        # Make our new position
        new = (self.odo_x, self.odo_y, self.odo_a)

        # To avoid using up unnecessary operations, don't update the path if the robot isn't moving
        if not (abs(self.vel_x) <= 0.01 and abs(self.vel_y) <= 0.01):
            # Add a new line to the path.
            self.paths.append([old, new])

        # Reset our encoders for the next iteration
        self.enc_c = 0
        self.enc_l = 0
        self.enc_r = 0

    # Draws the robot and it's path
    def draw(self, surf: pg.Surface):
        # Find the global position of the robot as it's used multiple times
        position_on_board = (int(self.x * Constants.PIX_PER_INCH) + 360, int(self.y * Constants.PIX_PER_INCH) + 360)

        # Draw the circle as the robot body
        pg.draw.circle(surf, Constants.ROBOT_COLOR, position_on_board, int(self.width / 2 * Constants.PIX_PER_INCH), 2)

        # Then draw the line that signifies the heading
        pg.draw.line(surf, Constants.HEADING_COLOR, position_on_board, (
        int((self.x + (math.cos(self.a) * 14)) * Constants.PIX_PER_INCH) + 360, int((self.y + (math.sin(self.a) * 14)) *
                                                                                Constants.PIX_PER_INCH) + 360), 2)

        # Next draw the paths found by the odometry algorithm
        for path in self.paths:
            pg.draw.line(surf, Constants.LINE_COLOR, (int(path[0][0] * Constants.PIX_PER_INCH) + 360,
                                                      int(path[0][1] * Constants.PIX_PER_INCH) + 360),
                         (int(path[1][0] * Constants.PIX_PER_INCH) + 360, int(path[1][1] * Constants.PIX_PER_INCH) + 360), 2)

"""
This is storage for old odometry algorithms

        self.odo_a += (self.enc_l-self.enc_r)/self.width
        p = (self.enc_r+self.enc_l)/2
        n = self.enc_c
        self.odo_y += ((p * math.sin(self.odo_a)) + (n * math.cos(self.odo_a)))
        self.odo_x += ((p * math.cos(self.odo_a)) - (n * math.sin(self.odo_a)))
        
        =====
        
                dc = ((self.enc_r + self.enc_l) / 2)
        ph = (self.enc_l - self.enc_r) / self.width
        self.odo_x += dc * math.cos(self.odo_a + (ph / 2))
        self.odo_y += dc * math.sin(self.odo_a + (ph / 2))
        self.odo_a += ph
        
        =====
        
                self.odo_a = self.a #! getting angle by gyro
        xc = self.enc_c
        yc = (self.enc_l+self.enc_r)/2
        xe = [0,0]
        ye = [0,0]
        xe[0] = xc*math.sin(self.odo_a)
        ye[0] = yc*math.cos(self.odo_a)
        xe[1] = xc*math.cos(self.odo_a)
        ye[1] = yc*math.sin(self.odo_a)
        self.odo_x += xe[0] + ye[0]
        self.odo_y += xe[1] + ye[1]
        
        =====
        
                theta = (self.enc_l - self.enc_r) / self.width
        xi = self.enc_c
        yi = (self.enc_l + self.enc_r) / 2
        r = yi / theta
        r2 = xi / theta
        dx = r - math.cos(theta) * r + r2 * math.sin(theta)
        dy = r * math.sin(theta) + r2 - r2 * math.cos(theta)
        self.odo_x += math.cos(self.odo_a) * (dy + dx)
        self.odo_y += math.sin(self.odo_a) * (dy + dx)
        self.odo_a += theta
        
        =====
        
                theta = (self.enc_l - self.enc_r) / self.width
        xi = self.enc_c
        yi = (self.enc_l + self.enc_r) / 2
        dx = 0
        dy = 0
        if theta == 0:
            dx = xi
            dy = yi
        else:
            r = yi / theta
            r2 = xi / theta
            dx = r - math.cos(theta) * r + r2 * math.sin(theta)
            dy = r * math.sin(theta) + r2 - r2 * math.cos(theta)
        self.odo_x += math.cos(self.odo_a) * dy + math.sin(self.odo_a) * dx
        self.odo_y += math.sin(self.odo_a) * dy + math.cos(self.odo_a) * dx
        self.odo_a += theta
        
        =====
        
                xi = self.enc_c
        yi = (self.enc_l + self.enc_r) / 2
        theta = (self.enc_l - self.enc_r) / self.width
        sineTerm = math.sin(theta) / theta if theta else 1
        cosTerm = (1 - math.cos(theta)) / theta if theta else 0
        dx = xi * sineTerm - yi * cosTerm
        dy = xi * cosTerm + yi * sineTerm
        self.odo_y += dx * math.cos(self.odo_a) - dy * math.sin(self.odo_a)
        self.odo_x += dx * math.sin(self.odo_a) + dy * math.cos(self.odo_a)
        self.odo_a -= theta
        
"""