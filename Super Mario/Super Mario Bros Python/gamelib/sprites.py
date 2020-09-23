#! /usr/bin/env python

import pygame, random, math
from pygame.locals import *

from data import *
import math

TOP_SIDE    = 0
BOTTOM_SIDE = 2
LEFT_SIDE   = 3
RIGHT_SIDE  = 1

def speed_to_side(dx,dy):
    if abs(dx) > abs(dy):
        dy = 0
    else:
        dx = 0
    if dy < 0:
        return 0
    elif dx > 0:
        return 1
    elif dy > 0:
        return 2
    elif dx < 0:
        return 3
    else:
        return 0, 0
    
class Collidable(pygame.sprite.Sprite):

    def __init__(self, *groups):
        pygame.sprite.Sprite.__init__(self, groups)
        self.collision_groups = []
        self.xoffset = 0
        self.yoffset = 1

    def collide(self, group):
        if group not in self.collision_groups:
            self.collision_groups.append(group)

    def move(self, dx, dy, collide=True):
        if collide:
            if dx!=0:
                dx, dummy = self.__move(dx,0)
            if dy!=0:
                dummy, dy = self.__move(0,dy)
        
        self.rect.move_ip(dx, dy)

    def clamp_off(self, sprite, side):
        if side == TOP_SIDE:
            self.rect.top = sprite.rect.bottom
        if side == RIGHT_SIDE:
            self.rect.right = sprite.rect.left
        if side == BOTTOM_SIDE:
            self.rect.bottom = sprite.rect.top
        if side == LEFT_SIDE:
            self.rect.left = sprite.rect.right

    def __move(self,dx,dy):
        oldr = self.rect
        self.rect.move_ip(dx, dy)
        side = speed_to_side(dx, dy)

        for group in self.collision_groups:
            for spr in group:
                if spr.rect.colliderect(self.rect):
                    self.on_collision(side, spr, group)

        return self.rect.left-oldr.left,self.rect.top-oldr.top

    def on_collision(self, side, sprite, group):
        self.clamp_off(sprite, side)

    def draw(self, surf):
        surf.blit(self.image, (self.rect[0]+self.xoffset, self.rect[0]+self.yoffset))

class Player(Collidable):

    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.left_images = []
        for i in self.right_images:
            self.left_images.append(pygame.transform.flip(i, 1, 0))
        self.image = self.right_images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.jump_speed = 0
        self.jump_accel = 0.3
        self.jumping = False
        self.frame = 0
        self.facing = 1
        self.angle = 0
        self.dying = False        
        self.shooting = False
        self.shoot_timer = 0
        self.still_timer = 5
        self.hp = 1
        self.hit_timer = 3
        self.jump_sound = load_sound("jump.ogg")
        self.hit_sound = load_sound("stomp.ogg")
        self.spring_sound = load_sound("jump2.ogg")
        self.springing = False

    def kill(self):
        #pygame.mixer.music.stop()
        pygame.sprite.Sprite.kill(self)
        PlayerDie(self.rect.center, self.facing)
        

    def on_collision(self, side, sprite, group):
        self.clamp_off(sprite, side)
        if side == TOP_SIDE:
            self.jump_speed = 0
        if side == BOTTOM_SIDE:
            if isinstance(sprite, Spikes):
                self.kill()
            self.jump_speed = 0
            self.jumping = False
            self.springing = False
            if isinstance(sprite, Spring):
                self.jump_speed = -15
                sprite.spring_time = 5
                self.jumping = True
                self.springing = True
                self.spring_sound.play()            
    def hit(self):
        if self.hit_timer <= 0:
            self.hit_timer = 20
            self.hp -= 1
            if self.hp <= 0:
                self.kill()
            else:
                self.hit_sound.play()
            
    def jump(self):
        if not self.jumping and not self.shooting and self.still_timer <= 0:
            self.jump_speed = -9.4
            self.jumping = True
            self.jump_sound.play()
            self.move(0, -4)
            
    def shoot(self):
        if not self.shooting and not self.jumping and self.still_timer <= 0:
            self.shooting = True
            self.shoot_timer = 6
            
    def stop_attacking(self):
        self.shooting = False

    def update(self):
        self.frame += 1
        self.still_timer -= 1
        self.hit_timer -= 1
        dx = 0
        key = pygame.key.get_pressed()

        if key[K_z] and not self.springing:
            self.jump_accel = 0.3
        else:
            self.jump_accel = 0.6

        if self.jump_speed < 8:
            self.jump_speed += self.jump_accel
        if self.jump_speed > 3:
            if MovingPlatform:
                False
            if MovingPlatformtwo:
                False
            if Underground:
                False
            else:
                self.jumping = True
            
        if self.shooting:
            self.shoot_timer -= 1
            id = self.shoot_timer/5
            if self.shoot_timer % 5 == 0 and id != 0:
                self.string = Stringer(self.rect.center, self.facing, id, self)
            if self.shoot_timer <= 0:
                self.shooting = False
        else:
            if self.still_timer <= 0:
                if key[K_LEFT]:
                    dx = -1
                    self.facing = dx
                if key[K_RIGHT]:
                    dx = 1
                    self.facing = dx

        if self.facing > 0:
            self.image = self.right_images[0]
        if self.facing < 0:
            self.image = self.left_images[0]
        if dx > 0:
            self.image = self.right_images[self.frame/6%4]
        if dx < 0:
            self.image = self.left_images[self.frame/6%4]
        if self.facing > 0 and self.jumping:
            self.image = self.right_images[4]
        if self.facing < 0 and self.jumping:
            self.image = self.left_images[4]    
        if self.hit_timer > 0:
            if not self.frame % 2:
                if self.facing > 0:
                    self.image = self.right_images[2]
                if self.facing < 0:
                    self.image = self.left_images[2]
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top >= 475:
            pygame.sprite.Sprite.kill(self)
                    
        self.move(3*dx, self.jump_speed)
        
class Platform(Collidable):
    def __init__(self, pos, tile, l, r):
        Collidable.__init__(self, self.groups)
        self.image = self.images["platform-%s.png" % tile]
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = l
        self.on_right = r

class Platformblue(Collidable):
    def __init__(self, pos, tile, l, r):
        Collidable.__init__(self, self.groups)
        self.image = self.images["platform-blue%s.png" % tile]
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = l
        self.on_right = r        

class Grass(Collidable):
    def __init__(self, pos, tile, l, r):
        Collidable.__init__(self, self.groups)
        self.image = self.images["grass-%s.png" % tile]
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = l
        self.on_right = r

class Brick(Collidable):
    def __init__(self, pos, tile, l, r):
        Collidable.__init__(self, self.groups)
        self.image = self.images["brick%s.png" % tile]
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = l
        self.on_right = r

class Brickblue(Collidable):
    def __init__(self, pos, tile, l, r):
        Collidable.__init__(self, self.groups)
        self.image = self.images["brickblue%s.png" % tile]
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = l
        self.on_right = r        

class Gray(Collidable):
    def __init__(self, pos, tile, l, r):
        Collidable.__init__(self, self.groups)
        self.image = self.images["gray%s.png" % tile]
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = l
        self.on_right = r

class Mountain(Collidable):
    def __init__(self, pos, tile, l, r):
        Collidable.__init__(self, self.groups)
        self.image = self.images["mountains%s.png" % tile]
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = l
        self.on_right = r
    
class Grass1(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class Grass2(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class GrassSprite(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False
        
                
class Spikes(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class AirPlatform(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class AirPlatformblue(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class Invisiblewall(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False        

class PlatformQ(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.frame = 0
    def update(self):
        self.frame += 1
        self.image = self.images[self.frame/39%3]

class Railing(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False        

class Pipe(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class PipeGreen(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class PipeGreenBig(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class PipeGreenEnd(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False        

class PipeBig(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class PipeEnd(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class PipeDown(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False        

class Fence(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class Tree1(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_rignt = False

class Tree2(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False
               
class Platform_Brick(Collidable):
     def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class Flag(Collidable):
     def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class Flag2(Collidable):
     def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False        

class Toad(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class Castle(Collidable):
     def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class Castlebig(Collidable):
     def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class Chain(Collidable):
     def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False


class Bush(Collidable):
     def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class Bush2(Collidable):
     def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False        

class Bush3(Collidable):
     def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False
    
class Bridge(Collidable):
    def __init__(self, pos, tile, l, r):
        Collidable.__init__(self, self.groups)
        self.image = self.images["bridge%s.png" % tile]
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = l
        self.on_right = r 

class Cloud(Collidable):
     def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.oldy = self.rect.centerx
        self.speed = -00.1
     def on_collision(self, side, sprite, group):
         if side == TOP_SIDE:
             sprite.rect.right = self.rect.left
             sprite.jump_speed = 1
         if side == BOTTOM_SIDE:
             sprite.rect.right = self.rect.left
     def update(self):
        if self.rect.centerx & self.oldy+64:
            self.speed = -self.speed
        if self.rect.centerx & self.oldy-64:
            self.speed = -self.speed
        self.move(-1, self.speed)        

class Cloud2(Collidable):
     def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.oldy = self.rect.centerx
        self.speed = -00.1
     def on_collision(self, side, sprite, group):
         if side == TOP_SIDE:
             sprite.rect.right = self.rect.left
             sprite.jump_speed = 1
         if side == BOTTOM_SIDE:
             sprite.rect.right = self.rect.left
     def update(self):
        if self.rect.centerx & self.oldy+64:
            self.speed = -self.speed
        if self.rect.centerx & self.oldy-64:
            self.speed = -self.speed
        self.move(-1, self.speed)              

class Firebowser(Collidable):
     def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.frame = 0
        self.oldy = self.rect.centerx
        self.speed = 0.5
     def on_collision(self, side, sprite, group):
         if side == TOP_SIDE:
             sprite.rect.right = self.rect.left
             sprite.jump_speed = 2
         if side == BOTTOM_SIDE:
             sprite.rect.right = self.rect.left
     def update(self):
        if self.rect.centerx & self.oldy+64:
            self.speed = -self.speed
        if self.rect.centerx & self.oldy-64:
            self.speed = -self.speed
        self.frame += 1
        self.image = self.images[self.frame/8%2]    
        self.move(-2.9, self.speed)
             
class MovingPlatform(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.oldy = self.rect.centery
        self.speed = 2
    def on_collision(self, side, sprite, group):
        if isinstance(sprite, Player):
            if side == TOP_SIDE:
                sprite.rect.bottom = self.rect.top
            if side == BOTTOM_SIDE:
                sprite.rect.top = self.rect.bottom
                if not sprite.jumping:
                    sprite.kill()
                    
    def update(self):
        if self.rect.centery > self.oldy+64:
            self.speed = -self.speed
        if self.rect.centery < self.oldy-64:
            self.speed = -self.speed
        self.move(0, self.speed)
    def collide_with_platforms(self, platform):
        if self.rect.colliderect(platform.rect):
            self.speed = -self.speed
            self.move(1, self.speed)

class MovingPlatformtwo(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.oldy = self.rect.centery
        self.speed = 2
    def on_collision(self, side, sprite, group):
        if isinstance(sprite, Player):
            if side == TOP_SIDE:
                sprite.rect.bottom = self.rect.top
            if side == BOTTOM_SIDE:
                sprite.rect.top = self.rect.bottom
                if not sprite.jumping:
                    sprite.kill()
                    
    def update(self):
        if self.rect.centery > self.oldy+64:
            self.speed = -self.speed
        if self.rect.centery < self.oldy-64:
            self.speed = -self.speed
        self.move(0, self.speed)
    def collide_with_platforms(self, platform):
        if self.rect.colliderect(platform.rect):
            self.speed = -self.speed
            self.move(1, self.speed)

class Underground(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.oldy = self.rect.centery
        self.speed = 2
    def on_collision(self, side, sprite, group):
        if isinstance(sprite, Player):
            if side == TOP_SIDE:
                sprite.rect.bottom = self.rect.top
                sprite.jump_speed = 1
            if side == BOTTOM_SIDE:
                sprite.rect.top = self.rect.bottom
                if not sprite.jumping:
                    sprite.kill()
                    
    def update(self):
        if self.rect.centery > self.oldy+230:
            self.speed = -self.speed
        if self.rect.centery < self.oldy-140:
            self.speed = -self.speed
        self.move(0, self.speed)
    def collide_with_platforms(self, platform):
        if self.rect.colliderect(platform.rect):
            self.speed = -self.speed
            self.move(1, self.speed)

class Hill(Collidable):
     def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class Hill2(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class Grasstexture(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class Wall(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class Lava(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False    

class Spring(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.spring_time = 0
        self.on_left = False
        self.on_right = False
    def update(self):
        self.image = self.images[0]
        self.spring_time -= 1
        if self.spring_time > 0:
            self.image = self.images[1]
                  
class Stringer(Collidable):
    def __init__(self, pos, dir, id, player):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(center = pos)
        self.move((28-id*12)*dir, 0)
        self.move(54*dir, 0)
        self.player = player
        self.dir = dir
        self.id = id
        if dir < 0:
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.life = 5*id
        self.shoot_sound = load_sound("fireball.ogg")
        self.shoot_sound.play()
    def update(self):
        self.rect.center = self.player.rect.center
        self.move((28-self.id*12)*self.dir, 0)
        self.move(54*self.dir, 0)
        self.life -= 1
        if not self.life % 5:
            self.image = pygame.transform.flip(self.image, 0, 0)
        if self.life <= 0:
            self.kill()


class Flower(Collidable):
    def __init__(self, pos, type="flower"):
        Collidable.__init__(self, self.groups)
        if type == "flower":
            self.left_images = self.left_images1
        self.right_images = []
        for i in self.left_images:
            self.right_images.append(pygame.transform.flip(i, 1, 0))
        self.images = self.right_images
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.frame = 0
        self.oldy = self.rect.centery
        self.speed = 1
        self.type = type

    def update(self):
        if self.speed > 0:
            self.images = self.right_images
        if self.speed < 0:
            self.images = self.left_images
        self.frame += 1
        self.image = self.images[self.frame/4%2]
      
# Flower up/down:

    def update(self):
        if self.rect.centery > self.oldy-1:
            self.speed = -self.speed
        if self.rect.centery < self.oldy+110:
            self.speed = -self.speed
        self.move(0, self.speed)
        
    def on_collision(self, side, sprite, group):
        self.clamp_off(sprite, side)
        if side == LEFT_SIDE:
            self.speed = 1
        if side == RIGHT_SIDE:
            self.speed = -1
        if side == BOTTOM_SIDE:
            if sprite.on_left:
                bottomleft = Rect(0, 1, 0, 1)
                bottomleft.topright = self.rect.bottomleft
                if bottomleft.left < sprite.rect.left:
                    self.speed = 1
            if sprite.on_right:
                bottomright = Rect(0, 1, 0, 1)
                bottomright.topleft = self.rect.bottomright
                if bottomright.right > sprite.rect.right:
                    self.speed = -1

class Flowertwo(Collidable):
    def __init__(self, pos, type="flowertwo"):
        Collidable.__init__(self, self.groups)
        if type == "flowertwo":
            self.left_images = self.left_images1
        self.right_images = []
        for i in self.left_images:
            self.right_images.append(pygame.transform.flip(i, 1, 0))
        self.images = self.right_images
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.frame = 1
        self.oldy = self.rect.centery
        self.speed = 1
        self.type = type

    def update(self):
        if self.speed > 0:
            self.images = self.right_images
        if self.speed < 0:
            self.images = self.left_images
        self.frame += 1
        self.image = self.images[self.frame/8%2]
              
# Flowertwo up/down:

    def update(self):
        if self.rect.centery > self.oldy-1:
            self.speed = -self.speed
        if self.rect.centery < self.oldy+110:
            self.speed = -self.speed
        self.move(0, self.speed)
        
    def on_collision(self, side, sprite, group):
        self.clamp_off(sprite, side)
        if side == LEFT_SIDE:
            self.speed = 1
        if side == RIGHT_SIDE:
            self.speed = -1
        if side == BOTTOM_SIDE:
            if sprite.on_left:
                bottomleft = Rect(0, 1, 0, 1)
                bottomleft.topright = self.rect.bottomleft
                if bottomleft.left < sprite.rect.left:
                    self.speed = 1
            if sprite.on_right:
                bottomright = Rect(0, 1, 0, 1)
                bottomright.topleft = self.rect.bottomright
                if bottomright.right > sprite.rect.right:
                    self.speed = -1

class Flowerthree(Collidable):
    def __init__(self, pos, type="flowerthree"):
        Collidable.__init__(self, self.groups)
        if type == "flowerthree":
            self.left_images = self.left_images1
        self.right_images = []
        for i in self.left_images:
            self.right_images.append(pygame.transform.flip(i, 1, 0))
        self.images = self.right_images
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.frame = 1
        self.oldy = self.rect.centery
        self.speed = 1
        self.type = type

    def update(self):
        if self.speed > 0:
            self.images = self.right_images
        if self.speed < 0:
            self.images = self.left_images
        self.frame += 1
        self.image = self.images[self.frame/8%2]
              
# Flowerthree up/down:

    def update(self):
        if self.rect.centery > self.oldy-5:
            self.speed = -self.speed
        if self.rect.centery < self.oldy+85:
            self.speed = -self.speed
        self.move(0, self.speed)
        
    def on_collision(self, side, sprite, group):
        self.clamp_off(sprite, side)
        if side == LEFT_SIDE:
            self.speed = 1
        if side == RIGHT_SIDE:
            self.speed = -1
        if side == BOTTOM_SIDE:
            if sprite.on_left:
                bottomleft = Rect(0, 1, 0, 1)
                bottomleft.topright = self.rect.bottomleft
                if bottomleft.left < sprite.rect.left:
                    self.speed = 1
            if sprite.on_right:
                bottomright = Rect(0, 1, 0, 1)
                bottomright.topleft = self.rect.bottomright
                if bottomright.right > sprite.rect.right:
                    self.speed = -1                    



class Flowerblue(Collidable):
    def __init__(self, pos, type="flowerblue"):
        Collidable.__init__(self, self.groups)
        if type == "flowerblue":
            self.left_images = self.left_images1
        self.right_images = []
        for i in self.left_images:
            self.right_images.append(pygame.transform.flip(i, 1, 0))
        self.images = self.right_images
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.frame = 1
        self.oldy = self.rect.centery
        self.speed = 1
        self.type = type

    def update(self):
        if self.speed > 0:
            self.images = self.right_images
        if self.speed < 0:
            self.images = self.left_images
        self.frame += 1
        self.image = self.images[self.frame/8%2]
              
# Flowerblue up/down:

    def update(self):
        if self.rect.centery > self.oldy-1:
            self.speed = -self.speed
        if self.rect.centery < self.oldy+110:
            self.speed = -self.speed
        self.move(0, self.speed)
        
    def on_collision(self, side, sprite, group):
        self.clamp_off(sprite, side)
        if side == LEFT_SIDE:
            self.speed = 1
        if side == RIGHT_SIDE:
            self.speed = -1
        if side == BOTTOM_SIDE:
            if sprite.on_left:
                bottomleft = Rect(0, 1, 0, 1)
                bottomleft.topright = self.rect.bottomleft
                if bottomleft.left < sprite.rect.left:
                    self.speed = 1
            if sprite.on_right:
                bottomright = Rect(0, 1, 0, 1)
                bottomright.topleft = self.rect.bottomright
                if bottomright.right > sprite.rect.right:
                    self.speed = -1
                    
# for big pipes
class Rose(Collidable):
    def __init__(self, pos, type="rose"):
        Collidable.__init__(self, self.groups)
        if type == "rose":
            self.left_images = self.left_images1
        self.right_images = []
        self.rect = self.image.get_rect(topleft = pos)
        self.frame = 1
        self.oldy = self.rect.centery
        self.speed = 1
        self.type = type

    def update(self):
        if self.speed > 0:
            self.images = self.right_images
        if self.speed < 0:
            self.images = self.left_images
        self.frame += 1
        self.image = self.images[self.frame/8%2]
        
    def update(self):
        if self.rect.centery > self.oldy-2:
            self.speed = -self.speed
        if self.rect.centery < self.oldy+150:
            self.speed = -self.speed
        self.move(0, self.speed)    

    def on_collision(self, side, sprite, group):
        self.clamp_off(sprite, side)
        if side == LEFT_SIDE:
            self.speed = 1
        if side == RIGHT_SIDE:
            self.speed = -1
        if side == BOTTOM_SIDE:
            if sprite.on_left:
                bottomleft = Rect(0, 1, 0, 1)
                bottomleft.topright = self.rect.bottomleft
                if bottomleft.left < sprite.rect.left:
                    self.speed = 1
            if sprite.on_right:
                bottomright = Rect(0, 1, 0, 1)
                bottomright.topleft = self.rect.bottomright
                if bottomright.right > sprite.rect.right:
                    self.speed = -1

                     
class Baddie(Collidable):
    def __init__(self, pos, type="monster"):
        Collidable.__init__(self, self.groups)
        if type == "monster":
            self.left_images = self.left_images1
        elif type == "slub":
            self.left_images = self.left_images2
        elif type == "monsterred":
            self.left_images = self.left_images4
        elif type == "blue":
            self.left_images = self.left_images5
        elif type == "monsterblue":
            self.left_images = self.left_images6
        elif type == "black":
            self.left_images = self.left_images7
        self.right_images = []
        for i in self.left_images:
            self.right_images.append(pygame.transform.flip(i, 1, 0))
        self.images = self.right_images
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.frame = 0
        self.speed = 2
        self.type = type
    
    def update(self):
        if self.speed > 0:
            self.images = self.right_images
        if self.speed < 0:
            self.images = self.left_images
        self.frame += 1
        self.image = self.images[self.frame/8%2]
        if self.type == "slub":
            self.move(self.speed, 1)
        self.move(self.speed, 1)    
    
    def on_collision(self, side, sprite, group):
        self.clamp_off(sprite, side)
        if side == LEFT_SIDE:
            self.speed = 1
        if side == RIGHT_SIDE:
            self.speed = -1
        if side == BOTTOM_SIDE:
            if sprite.on_left:
                bottomleft = Rect(0, 0, 1, 1)
                bottomleft.topright = self.rect.bottomleft
                if bottomleft.left < sprite.rect.left:
                    self.speed = 1
            if sprite.on_right:
                bottomright = Rect(0, 0, 1, 1)
                bottomright.topleft = self.rect.bottomright
                if bottomright.right > sprite.rect.right:
                    self.speed = -1

class Sky(Collidable):
    def __init__(self, pos, type="sky"):
        Collidable.__init__(self, self.groups)
        if type == "sky":
            self.left_images = self.left_images1
        self.right_images = []
        for i in self.left_images:
            self.right_images.append(pygame.transform.flip(i, 1, 0))
        self.images = self.right_images
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.oldy = self.rect.centerx
        self.speed = -00.01
        self.frame = 0
        self.type = type
    
    def update(self):
        if self.rect.centerx & self.oldy+64:
            self.speed = -self.speed
        if self.rect.centerx & self.oldy-64:
            self.speed = -self.speed    
        self.move(2.95, self.speed)
    
    def on_collision(self, side, sprite, group):
         if side == TOP_SIDE:
             sprite.rect.right = self.rect.left
             sprite.jump_speed = 1
         if side == BOTTOM_SIDE:
             sprite.rect.right = self.rect.left

class Spiker(Collidable):
    def __init__(self, pos, type="spiker"):
        Collidable.__init__(self, self.groups)
        if type == "spiker":
            self.left_images = self.left_images1
        elif type == "bkshell":
            self.left_images = self.left_images2
        self.right_images = []
        for i in self.left_images:
            self.right_images.append(pygame.transform.flip(i, 1, 0))
        self.images = self.right_images
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.frame = 0
        self.speed = 1
        self.type = type
    
    def update(self):
        if self.speed > 0:
            self.images = self.right_images
        if self.speed < 0:
            self.images = self.left_images
        self.frame += 1
        self.image = self.images[self.frame/8%2]
        if self.type == "bkshell":
            self.image = self.images[self.frame/12%2]
        else:
            self.move(self.speed, 2)
    
    def on_collision(self, side, sprite, group):
        self.clamp_off(sprite, side)
        if side == LEFT_SIDE:
            self.speed = 1
        if side == RIGHT_SIDE:
            self.speed = -1
        if side == BOTTOM_SIDE:
            if sprite.on_left:
                bottomleft = Rect(1, 1, 0, 0)
                bottomleft.topright = self.rect.bottomleft
                if bottomleft.right < sprite.rect.right:
                    self.speed = -1
            if sprite.on_right:
                bottomright = Rect(1, 1, 0, 0)
                bottomright.topleft = self.rect.bottomright
                if bottomright.left > sprite.rect.left:
                    self.speed = -1
                    
class Cannon(Collidable):
    def __init__(self, pos, type="cannon"):
        Collidable.__init__(self, self.groups)
        if type == "cannon":
            self.left_images = self.left_images1
        elif type == "cannonbig":
            self.left_images = self.left_images2
        elif type == "smallcannon":
            self.left_images = self.left_images4
        self.right_images = []
        for i in self.left_images:
            self.right_images.append(pygame.transform.flip(i, 1, 0))
        self.images = self.right_images
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.frame = 0
        self.speed = 1
        self.type = type

    def update(self):
        if self.speed > 0:
            self.images = self.right_images
        if self.speed < 0:
            self.images = self.left_images
        self.frame += 1
        self.image = self.images[self.frame/2%2]
        if self.type == "cannon":
            self.image = self.images[self.frame/12%2]
        elif self.type == "cannonbig":
            self.image = self.images[self.frame/12%2]
        elif self.type == "smallcannon":
            self.image = self.images[self.frame/12%2]
        else:
            self.move(self.speed, 1)

    def on_collision(self, side, sprite, group):
        self.clamp_off(sprite, side)
        if side == LEFT_SIDE:
            self.speed = 1
        if side == RIGHT_SIDE:
            self.speed = -1
        if side == BOTTOM_SIDE:
            if sprite.on_left:
                bottomleft = Rect(0, 0, 1, 1)
                bottomleft.topright = self.rect.bottomleft
                if bottomleft.left < sprite.rect.left:
                    self.speed = 1
            if sprite.on_right:
                bottomright = Rect(0, 0, 1, 1)
                bottomright.topleft = self.rect.bottomright
                if bottomright.right > sprite.rect.right:
                    self.speed = -1        

class CannonShot(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(bottomleft = pos)
        self.x,self.y=self.rect.topleft
        x = self.x - self.player.rect.centerx
        angle = math.atan(x)
        self.angle = int(265.0 - (angle * 30) / math.pi)
    def update(self):
        self.rect.center = (self.x, self.y)
        speed = 2.5
        self.x += math.sin(math.radians(self.angle))*speed

class CannonShotsmall(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(center = pos)
        self.x,self.y=self.rect.center
        x = self.x - self.player.rect.centerx
        angle = math.atan(x)
        self.angle = int(265.0 - (angle * 30) / math.pi)
    def update(self):
        self.rect.center = (self.x, self.y)
        speed = 2.5
        self.x += math.sin(math.radians(self.angle))*speed
       
class CannonShotbig(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(bottomleft = pos)
        self.x,self.y=self.rect.topleft
        x = self.x - self.player.rect.centerx
        angle = math.atan(x)
        self.angle = int(265.0 - (angle * 30) / math.pi)
    def update(self):
        self.rect.center = (self.x, self.y)
        speed = 2.5
        self.x += math.sin(math.radians(self.angle))*speed

class Fireball(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(bottomleft = pos)
        self.frame = 0
        self.x,self.y=self.rect.topleft
        x = self.x - self.player.rect.centerx
        angle = math.atan(x)
        self.angle = int(265.0 - (angle * 30) / math.pi)
    def update(self):
        self.rect.center = (self.x, self.y)
        speed = 2.5
        self.x += math.sin(math.radians(self.angle))*speed
        self.frame += 1
        self.image = self.images[self.frame/8%2]


        
class BaddieBoom(Collidable):        
    def __init__(self, pos, facing, type):
        Collidable.__init__(self, self.groups)
        if type == "monster":
            self.left_images = self.left_images1
        elif type == "slub":
            self.left_images = self.left_images2    
        elif type == "monsterred":
            self.left_images = self.left_images4
        elif type == "blue":
            self.left_images = self.left_images5
        elif type == "monsterblue":
            self.left_images = self.left_images6
        elif type == "black":
            self.left_images = self.left_images7
        self.right_images = []
        for i in self.left_images:
            self.right_images.append(pygame.transform.flip(i, 1, 0))
        self.images = self.right_images
        self.image = self.images[0]
        self.rect = self.image.get_rect(center = pos)
        self.facing = facing
        self.timer = 0

   
    def update(self):
        if self.facing > 0:
            self.images = self.right_images
        else:
            self.images = self.left_images
        self.timer += 1
        if self.timer <= 25:
            self.image = self.images[self.timer/4%2]
        elif self.timer < 36:
            self.image = self.images[self.timer/4%2]
        else:
            self.kill()
                                
class BaddieShot(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(center = pos)
        self.x,self.y=self.rect.center
        x = self.x - self.player.rect.centerx
        y = self.y - self.player.rect.centery
        angle = math.atan2(y, x)
        self.angle = int(270.0 - (angle * 180) / math.pi)
    def update(self):
        self.rect.center = (self.x, self.y)
        speed = 3
        self.x += math.sin(math.radians(self.angle))*speed
        self.y += math.cos(math.radians(self.angle))*speed

class SpikeShot(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(bottomleft = pos)
        self.frame = 0
        self.x,self.y=self.rect.center
        x = self.x - self.player.rect.centerx
        y = self.y - self.player.rect.centery
        angle = math.atan2(y, x)
        self.angle = int(270.0 - (angle * 180) / math.pi)
    def update(self):
        self.rect.center = (self.x, self.y)
        speed = 3
        self.x += math.sin(math.radians(self.angle))*speed
        self.y += math.cos(math.radians(self.angle))*speed
        self.frame += 1
        self.image = self.images[self.frame/8%2]
                                      
class MushroomGreen(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class MushroomGreendie(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups) 
        self.image = self.images[0]
        self.rect = self.image.get_rect(center = pos)
        self.timer = 0
   
    def update(self):
        self.timer += 1
        if self.timer < 12:
            self.image = self.images[self.timer/4%3]
        else:
            self.kill()

class Axe(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.on_left = False
        self.on_right = False

class AxeDie(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups) 
        self.image = self.images[0]
        self.rect = self.image.get_rect(center = pos)
        self.timer = 0
   
    def update(self):
        self.timer += 1
        if self.timer < 12:
            self.image = self.images[self.timer/4%3]
        else:
            self.kill()        
                                       
class Coin(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.frame = 0
    def update(self):
        self.frame += 1
        self.image = self.images[self.frame/6%4]

class CoinDie(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups) 
        self.image = self.images[0]
        self.rect = self.image.get_rect(center = pos)
        self.timer = 0
   
    def update(self):
        self.timer += 1
        if self.timer < 12:
            self.image = self.images[self.timer/4%3]
        else:
            self.kill()
            
class PlayerDie(Collidable):
    def __init__(self, pos, facing):
        Collidable.__init__(self, self.groups)
        self.left_images = []
        for i in self.right_images:
            self.left_images.append(pygame.transform.flip(i, 1, 0))
        self.images = self.right_images
        self.image = self.images[0]
        self.rect = self.image.get_rect(center = pos)
        self.facing = facing
        self.timer = 0
        self.sound1 = load_sound("death.ogg")
        self.sound1.play()
   
    def update(self):
        if self.facing > 0:
            self.images = self.right_images
        else:
            self.images = self.left_images
        self.timer += 1
        if self.timer <= 20:
            self.image = self.images[0]
        elif self.timer <= 45:
            self.image = self.images[1]
        elif self.timer <= 57:
            self.image = self.images[self.timer/4%3]
        else:
            self.kill()

class Bomb(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft = pos)
        self.explode_time = 2000
        self.on_left = False
        self.on_right = False
    def update(self):
        self.explode_time -= 0.5
                            
class Boss(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups)
        self.right_images = []
        for i in self.left_images:
            self.right_images.append(pygame.transform.flip(i, 1, 0))
        self.images = self.right_images
        self.image = self.images[0]
        self.rect = self.image.get_rect(bottomleft = pos)
        self.frame = 0
        self.facing = 1
        self.hit_timer = 0
        self.hp = 1
        self.die_time = 0
        self.dead = False
        self.oldy = self.rect.centery
        self.speed = 5
        self.type = type
        
    def kill(self):
        if self.die_time <= 0:
            self.image = pygame.Surface((1, 1))
            self.image.set_alpha(0)
            self.dead = True
            stop_music()
            self.die_time = 200         
        
    def hit(self):
        if self.hit_timer <= 0 and self.hp > 0:
            self.hit_timer = 50
            if self.hp <= 0:
                self.kill()            
    
    def update(self):
        self.die_time -= 1
        self.hit_timer -= 1
        dx = 0
        if not self.dead:
            if self.speed > 1:
                self.images = self.right_images
            if self.speed < 1:
                self.images = self.left_images
            self.frame += 1
            self.image = self.images[self.frame/50%4]
            if self.hit_timer > 0:
                self.image = self.images[self.frame/50%4 + 1]
            if not random.randrange(3):
                pos = [0, 0]
                pos[0] = random.randrange(self.rect.left, self.rect.right)
                pos[1] = random.randrange(self.rect.top, self.rect.bottom)
        self.move(self.speed, 1)
        
    def on_collision(self, side, sprite, group):
        self.clamp_off(sprite, side)
        if side == LEFT_SIDE:
            self.speed = 1
        if side == RIGHT_SIDE:
            self.speed = -1
        if side == BOTTOM_SIDE:
            if sprite.on_left:
                bottomleft = Rect(0, 0, 1, 1)
                bottomleft.topright = self.rect.bottomleft
                if bottomleft.left < sprite.rect.left:
                    self.speed = 4
            if sprite.on_right:
                bottomright = Rect(0, 0, 1, 1)
                bottomright.topleft = self.rect.bottomright
                if bottomright.right > sprite.rect.right:
                    self.speed = -4
