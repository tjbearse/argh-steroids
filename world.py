
import math
import random
import sys

import pygame

import util
import sprite
import particle
import text
import alien
import ship
import asteroid
import player

class World(object):
    SECOND_EVENT = pygame.USEREVENT + 1
    def __init__(self, surface, settings):
        self.surface = surface
        self.width = surface.get_width()
        self.height = surface.get_height()
        self.sprites = []
        self.particle = particle.Particle(surface)
        self.score = 0
        self.n_asteroids = 0
        self.text_y = 100
        self.settings = settings
        pygame.time.set_timer(self.SECOND_EVENT, 1000)

        # input state
        self.quit = False
        self.rotate_left = False
        self.rotate_right = False
        self.rotate_by = 0
        self.thrust = False
        self.info = False
        self.fire = False
        self.spawn = False
        self.show_particles = False
        self.enter = False
        self.next_level = False

        # the ship ... or none for no ship on screen
        self.player = None
        self.player_driver = None

        # countdown timer until next alien
        self.alien_time = random.randint(1000, 2000)

    def state(self):
        res = str(len(self.sprites))
        for sprite in self.sprites:
           res += "\n" + str(sprite)
        res += "\nstop"
        return res

    def n_objects(self):
        return len(self.sprites)

    def reset(self):
        self.sprites = []
        self.n_asteroids = 0
        self.particle.remove_all()
        self.text_y = 100
        self.score = 0
        self.player = None

    def remove_asteroids(self):
        self.sprites = [x for x in self.sprites 
                        if not isinstance(x, asteroid.Asteroid)]

    def add(self, sprite):
        self.sprites.append(sprite)

    def add_player(self, driver):
        if not self.player:
            self.player = ship.Ship(self)
            self.player_driver = driver

    def add_text(self, string, scale = 10):
        text.Character.string(self, string, 
                              [self.width / 2, self.text_y], scale)
        self.text_y += scale * 10

    def update(self):
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                self.quit = True 
            elif event.type == self.SECOND_EVENT:
                self.score = max(self.score - self.settings.time_cost, 0)
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.quit = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_s:
                    self.spawn = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_n:
                    self.next_level = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_p:
                    if event.type == pygame.KEYDOWN:
                        self.show_particles = not self.show_particles
                elif event.key == pygame.K_i:
                    self.info = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_RETURN:
                    self.enter = event.type == pygame.KEYDOWN
        self.rotate_left = False
        self.rotate_right = False
        self.thrust = False
        self.fire = False
        if(self.player_driver and self.player):
            state = self.state()
            self.player_driver.write(state)
            command = self.player_driver.read_timeout(1).split()
            if len(command) != 3:
                raise ValueError('All commands are not present')
            turn, thrust, fire = command
            # turn
            #if turn not in ['ccw', 'cw', 'off']:
                #raise ValueError("Turn has unexpected value")
            self.rotate_left = (turn == 'ccw')
            self.rotate_right = (turn == 'cw')
            # thrust
            #if thrust not in ['on', 'off']:
                #raise ValueError("Thrust has unexpected value")
            self.thrust = (thrust == 'on')
            # fire
            self.fire = (fire == 'on')

        self.particle.show(self.show_particles)

        if self.rotate_left:
            self.rotate_by = -3
        elif self.rotate_right:
            self.rotate_by = 3
        else:
            self.rotate_by = 0

        if self.player:
            if self.thrust:
                self.player.thrust();

            if self.fire:
                self.player.fire();

            self.player.rotate_by(self.rotate_by)

        for i in self.sprites:
            i.update()
        self.particle.update()

        self.alien_time -= 1
        if self.alien_time < 0:
            self.alien_time = random.randint(1000, 2000)
            alien.Alien(self)

        if self.player and self.player.kill:
            self.player = None

        self.sprites = [x for x in self.sprites if not x.kill]

        # split the world into a map of 100x100 squares, put a note in each
        # square of each sprite which intersects with that square ... then when
        # we test for collisions, we only need to test against the sprites in
        # that map square

        # 100 is the max size of the asteroids we make
        map_spacing = 100
        map_width = int(math.ceil(float(self.width+1) / map_spacing))
        map_height = int(math.ceil(float(self.height+1) / map_spacing))
        world_map = []
        for x in range(map_width):
            map_row = [[] for y in range(map_height)]
            world_map.append(map_row)

        for i in self.sprites:
            i.tested_collision = False
            x = int(i.position[0] / map_spacing)
            y = int(i.position[1] / map_spacing)
            for a in range(x - 1, x + 2):
                for b in range(y - 1, y + 2):
                    world_map[a % map_width][b % map_height].append(i)

        for i in self.sprites:
            x = int(i.position[0] / map_spacing)
            y = int(i.position[1] / map_spacing)
            i.test_collisions(world_map[x][y])

            # now we've tested i against everything it could possibly touch, 
            # we no longer need to test anything against i
            i.tested_collision = True

    def draw(self):
        self.particle.draw()
        for i in self.sprites:
            i.draw()
