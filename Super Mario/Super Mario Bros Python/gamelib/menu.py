#! /usr/bin/env python

import os, pygame, sys, time
from pygame.locals import *

from game import *
from ezmenu import *
from data import *
from cutscenes import *

def RunGame(screen):
    Game(screen)
    play_music("title.ogg", 0.75)
    
def ContinueGame(screen):
    Game(screen, True)
    play_music("title.ogg", 0.75)

def Fullscreen(screen):
    screen = pygame.display.set_mode((640, 480), FULLSCREEN)

def Normalscreen(screen):
    screen = pygame.display.set_mode((640, 480))
    
def Help(screen):
    cutscene(screen, ["CONTROLS:",
    "",
    "Move: Arrow Keys",
    "Jump: Z key",
    "Return: Escape key (ESC)",                 
    "Music off: = S key",
    "Music on: = P key",
    "Advice: Jump on enemies to kill them!",
    "Hold the Z key to extend your air time",
    "when killing an enemy"])                  
      
class MenuO(object): 
    def __init__(self, screen):
        self.screen = screen
        self.menuO = EzMenu(["FULLSCREEN", lambda: Fullscreen(screen)], ["WINDOWED MODE", lambda: Normalscreen(screen)], ["RETURN", lambda: Menu(screen)])
        self.menuO.set_highlight_color((255, 0, 0))
        self.menuO.set_normal_color((255, 255, 255))
        self.menuO.center_at(300, 400)
        self.menuO.set_font(pygame.font.Font(filepath("fonts/font.ttf"), 16))
        self.bg = load_image("menu.png")
        self.font = pygame.font.Font(filepath("fonts/font.ttf"), 16)
        self.font2 = pygame.font.Font(filepath("fonts/super-mario-64.ttf"), 45)
        events = pygame.event.get()
        self.clock = pygame.time.Clock()
        self.menuO.update(events)
        self.main_loop()

    def main_loop(self):
        while 1:
            self.clock.tick(30)
            events = pygame.event.get()
            self.menuO.update(events)
            for e in events:
                if e.type == QUIT:
                    pygame.quit()
                    return
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    pygame.quit()
                    return

            self.screen.blit(self.bg, (0, 0))

            ren = self.font2.render("Super Mario", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 180))

            ren = self.font2.render("Python", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 235))

            ren = self.font2.render("Game by HJ", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 80))
            
            self.menuO.draw(self.screen) 
            pygame.display.flip()
 
class Menu(object):

    def __init__(self, screen):
        play_music("title.ogg", 0.75)
        self.screen = screen
        self.menu = EzMenu(["NEW GAME", lambda: RunGame(screen)], ["CONTINUE", lambda: ContinueGame(screen)], ["OPTIONS", lambda: MenuO(screen)], ["CONTROLS", lambda: Help(screen)], ["QUIT GAME", sys.exit])
        self.menu.set_highlight_color((255, 0, 0))
        self.menu.set_normal_color((255, 255, 255))
        self.menu.center_at(300, 400)
        self.menu.set_font(pygame.font.Font(filepath("fonts/font.ttf"), 16))
        self.bg = load_image("menu.png")
        self.font = pygame.font.Font(filepath("fonts/font.ttf"), 16)
        self.font2 = pygame.font.Font(filepath("fonts/super-mario-64.ttf"), 45)
        self.clock = pygame.time.Clock()
        events = pygame.event.get()
        self.menu.update(events)
        self.menu.draw(self.screen)
        self.main_loop()    
  
    def main_loop(self):
        while 1:
            self.clock.tick(30)
            events = pygame.event.get()
            self.menu.update(events)
            for e in events:
                if e.type == QUIT:
                    pygame.quit()
                    return
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    pygame.quit()
                    return
          
            self.screen.blit(self.bg, (0, 0))

            ren = self.font2.render("Super Mario", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 180))

            ren = self.font2.render("Python", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 235))

            ren = self.font2.render("Game by HJ", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 80))

            self.menu.draw(self.screen)
            pygame.display.flip()
