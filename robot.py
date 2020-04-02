import math
import pygame as pg
from pygame.locals import *
import random

import Constants


class Robot:
    def __init__(self):
        self.width = 18
        self.enc_di = 1

        self.x = 0
        self.y = 0
        self.a = 0

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

        if keys[K_LEFT]:
            self.vel_a -= 0.05 / 2
        if keys[K_RIGHT]:
            self.vel_a += 0.05 / 2

        self.vel_a += (random.randint(-100, 100) / 1000000 * math.sqrt(self.vel_x ** 2 + self.vel_y ** 2))
        self.a += self.vel_a / 2

        self.enc_c -= (self.vel_x * math.sin(self.a)) - (self.vel_y * math.cos(self.a))
        self.enc_l += (self.vel_x * math.cos(self.a)) + (self.vel_y * math.sin(self.a)) + (
                    (self.vel_a / (2 * math.pi)) * (self.width * math.pi))
        self.enc_r += (self.vel_x * math.cos(self.a)) + (self.vel_y * math.sin(self.a)) - (
                    (self.vel_a / (2 * math.pi)) * (self.width * math.pi))

        self.x += self.vel_x
        self.y += self.vel_y
        self.a += self.vel_a / 2
        # print(self.enc_c, self.enc_l, self.enc_r)

        self.vel_x *= Constants.DAMPENING
        self.vel_y *= Constants.DAMPENING
        self.vel_a *= Constants.DAMPENING_A

        # Start trimming the path list if it gets too big
        if len(self.paths) >= 1000:
            del self.paths[0]

    def path(self):
        old = (self.odo_x, self.odo_y, self.odo_a)

        """
        self.odo_a += (self.enc_l-self.enc_r)/self.width
        p = (self.enc_r+self.enc_l)/2
        n = self.enc_c
        self.odo_y += ((p * math.sin(self.odo_a)) + (n * math.cos(self.odo_a)))
        self.odo_x += ((p * math.cos(self.odo_a)) - (n * math.sin(self.odo_a)))
        """
        """
        dc = ((self.enc_r + self.enc_l) / 2)
        ph = (self.enc_l - self.enc_r) / self.width
        self.odo_x += dc * math.cos(self.odo_a + (ph / 2))
        self.odo_y += dc * math.sin(self.odo_a + (ph / 2))
        self.odo_a += ph
        """

        dc = ((self.enc_r + self.enc_l) / 2)
        ph = (self.enc_l - self.enc_r) / self.width

        self.odo_x += dc * math.cos(self.odo_a + (ph / 2)) - self.enc_c * math.sin(self.odo_a + (ph / 2))
        self.odo_y += dc * math.sin(self.odo_a + (ph / 2)) + self.enc_c * math.cos(self.odo_a + (ph / 2))
        self.odo_a += ph

        """
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
        """

        """
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
        """
        """
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
        """
        """
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
        # print(self.enc_c, self.enc_l, self.enc_r)

        # print("ODO:", self.odo_x, self.odo_y, self.odo_a)

        # print((abs(self.vel_x)+abs(self.vel_y))*30/12/1.467)

        new = (self.odo_x, self.odo_y, self.odo_a)

        # To avoid using up unnecessary operations, don't update the path if the robot isn't moving
        if not (abs(self.vel_x) <= 0.01 and abs(self.vel_y) <= 0.01):
            self.paths.append([old, new])

        self.enc_c = 0
        self.enc_l = 0
        self.enc_r = 0

    def draw(self, surf):
        positionOnBoard = (int(self.x * Constants.PIX_PER_INCH), int(self.y * Constants.PIX_PER_INCH))

        pg.draw.circle(surf, Constants.ROBOT_COLOR, positionOnBoard, int(self.width / 2 * Constants.PIX_PER_INCH), 2)

        pg.draw.line(surf, Constants.HEADING_COLOR, positionOnBoard, (
        int((self.x + (math.cos(self.a) * 14)) * Constants.PIX_PER_INCH), int((self.y + (math.sin(self.a) * 14)) * Constants.PIX_PER_INCH)),
                     2)
        for path in self.paths:
            pg.draw.line(surf, Constants.LINE_COLOR, (int(path[0][0] * Constants.PIX_PER_INCH), int(path[0][1] * Constants.PIX_PER_INCH)),
                         (int(path[1][0] * Constants.PIX_PER_INCH), int(path[1][1] * Constants.PIX_PER_INCH)), 2)
