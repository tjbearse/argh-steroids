#!/usr/bin/python

import random
import math

import sys
import argparse

import pygame

import util
import asteroid
import text
import world
import player


class Game(object):
    def __init__(self, surface, settings):
        self.surface = surface
        self.world = world.World(surface, settings)
        self.width = self.world.width
        self.height = self.world.height
        self.clock = pygame.time.Clock()
        self.level = 1
        self.player = player.Player(settings.driver)
        self.player.write("%i %i" % (self.width, self.height))

    def draw_hud(self):
        text.draw_string(self.surface, "SCORE %d" % self.world.score, 
                         util.WHITE, 10, [10, 20])
        text.draw_string(self.surface, "LEVEL %d" % self.level, 
                         util.WHITE, 10, [10, 40])

    def start_screen(self):
        self.world.add_text('ARGH ITS THE ASTEROIDS', scale = 20)
        self.world.add_text('PRESS ESC TO QUIT') 
        self.world.add_text('PRESS LEFT AND RIGHT TO ROTATE') 
        self.world.add_text('PRESS UP FOR THRUST')
        self.world.add_text('PRESS SPACE FOR FIRE')
        self.world.add_text('OR USE MOUSE CONTROLS') 
        self.world.add_text('WATCH OUT FOR ALLEN THE ALIEN')
        self.world.add_text('PRESS ENTER TO START', scale = 20)

        for i in range(4):
            asteroid.Asteroid(self.world, random.randint(50, 100), 1)
        self.world.particle.starfield()

        while not self.world.quit and not self.world.enter:
            self.world.update()
            self.surface.fill(util.BLACK)
            self.draw_info()
            self.world.draw()
            # set the limit very high, we can use the start screen as a 
            # benchmark
            self.clock.tick(200)
            pygame.display.flip()

    def draw_info(self):
        if self.world.info:
            text.draw_string(self.surface, 
                             "FPS %d" % self.clock.get_fps(),
                             util.WHITE, 10, [10, self.height - 20])
            text.draw_string(self.surface, 
                             "OBJECTS %d" % self.world.n_objects(), 
                             util.WHITE, 10, [10, self.height - 40])
            text.draw_string(self.surface, 
                             "PARTICLES %d" % self.world.particle.n_particles(),
                             util.WHITE, 10, [10, self.height - 60])

    def level_start(self):
        start_animation_frames = 100
        start_animation_time = start_animation_frames

        while not self.world.quit:
            if start_animation_time == 0:
                break

            self.world.update()
            if self.world.spawn:
                asteroid.Asteroid(self.world, 
                                  random.randint(75, 100), 
                                  self.level)

            self.surface.fill(util.BLACK)
            self.draw_hud()
            self.draw_info()
            start_animation_time -= 1
            t = float(start_animation_time) / start_animation_frames
            text.draw_string(self.surface, "LEVEL START", util.WHITE,
                             t * 150,
                             [self.width / 2, self.height / 2],
                             centre = True, 
                             angle = t * 200.0)
            self.world.draw()
            self.clock.tick(60)
            pygame.display.flip()

    def play_level(self):
        while not self.world.quit:
            if self.world.n_asteroids == 0:
                break
            if not self.world.player:
                break
            if self.world.next_level:
                self.world.remove_asteroids()
                break

            self.world.update()
            self.surface.fill(util.BLACK)
            self.draw_hud()
            self.draw_info()
            self.world.draw()
            self.clock.tick(60)
            pygame.display.flip()

    def game_over(self):
        end_animation_frames = 100
        end_animation_time = end_animation_frames

        while not self.world.quit:
            if end_animation_time == 0:
                break

            self.world.update()

            self.surface.fill(util.BLACK)
            self.draw_hud()
            self.draw_info()
            end_animation_time -= 1
            t = float(end_animation_time) / end_animation_frames
            text.draw_string(self.surface, "GAME OVER", util.WHITE,
                             math.log(t + 0.001) * 150,
                             [self.width / 2, self.height / 2],
                             centre = True,
                             angle = 180)
            self.world.draw()
            self.clock.tick(60)
            pygame.display.flip()

    def epilogue(self):
        while not self.world.quit:
            if self.world.enter:
                break

            self.world.update()

            self.surface.fill(util.BLACK)
            text.draw_string(self.surface, "PRESS ENTER TO PLAY AGAIN", 
                             util.WHITE,
                             20,
                             [self.width / 2, self.height / 2],
                             centre = True,
                             angle = 0)
            self.draw_hud()
            self.draw_info()
            self.world.draw()
            self.clock.tick(60)
            pygame.display.flip()

    def play_game(self):
        self.start_screen()

        while not self.world.quit:
            self.level = 1
            self.world.reset()
            self.world.particle.starfield()

            while not self.world.quit:
                self.level_start()

                self.world.add_player(self.player)
                for i in range(self.level * 2):
                    asteroid.Asteroid(self.world, 
                                      random.randint(75, 100), 
                                      0.5 + self.level / 4.0)

                self.play_level()

                if not self.world.player:
                    break

                self.level += 1

            self.game_over()
            self.epilogue()

def main():
    parser = argparse.ArgumentParser(description='Asteroids AI Client',
            fromfile_prefix_chars='@')
    parser.add_argument('-d', '--driver', dest='driver', metavar='driver', required=True)
    parser.add_argument('--no-shield-regen', dest='shield_regen', default=False, action='store_false')
    parser.add_argument('--shield-regen', dest='shield_regen', action='store_true')
    parser.add_argument('--bullet-cost', dest='bullet_cost', default=1, type=int)
    parser.add_argument('--time-cost', dest='time_cost', default=0, type=int)
    args = parser.parse_args()

    pygame.init()

    font = pygame.font.Font(None, 16)

    #surface = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
    surface = pygame.display.set_mode([1000, 1000])
    #pygame.mouse.set_visible(False)
    pygame.display.set_caption("Argh, it's the Asteroids!!")

    game = Game(surface, args)

    game.play_game()

    pygame.quit()

if __name__ == "__main__":
    main()
