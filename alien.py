
import pygame
import math
import random

import util
import sprite
import bullet
import ship

class Alien(sprite.Sprite):
    def __init__(self, world):
        super(Alien, self).__init__(world)

        self.points = [[1, 0], [-1, 0], [-0.7, 0],
                       [-0.5, 0.2], [0.5, 0.2],
                       [0.7, 0],
                       [0.5, -0.4], [-0.5, -0.4],
                       [-0.7, 0]]
        self.direction = random.randint(1, 2) * 2 - 3
        self.position = [world.width / 2 - self.direction * world.width / 2 + self.direction, 
                         random.randint(0, world.height)]
        self.angle = 0
        self.scale = 10
        self.direction_timer = random.randint(10, 50)
        self.random_velocity()

    def typename(self):
        return "alien"

    def random_velocity(self):
        self.velocity = [self.direction * (random.random() * 2 + 1), 
                         random.random() * 6 - 3]

    def update(self):
        self.direction_timer -= 1
        if self.direction_timer < 0:
            self.direction_timer = random.randint(10, 50)
            self.random_velocity()

        if self.angle > 0:
            self.angle -= 1
        elif self.angle < 0:
            self.angle += 1

        if self.direction == 1 and self.position[0] > self.world.width - 10:
            self.kill = True
        elif self.direction == -1 and self.position[0] < 10:
            self.kill = True

        super(Alien, self).update()

    def impact(self, other):
        self.angle = random.randint(-90, 90)
        return super(Alien, self).impact(other)
