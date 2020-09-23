import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import random
import pygame, os,sys,math
from pygame.locals import *
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
            self.image = self.right_images[self.frame//6%4]
        if dx < 0:
            self.image = self.left_images[self.frame//6%4]
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
        self.image = self.images[self.frame//39%3]

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
        self.image = self.images[self.frame//8%2]    
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
        self.image = self.images[self.frame//4%2]
      
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
        self.image = self.images[self.frame//8%2]
              
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
        self.image = self.images[self.frame//8%2]
              
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
        self.image = self.images[self.frame//8%2]
              
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
        self.image = self.images[self.frame//8%2]
        
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
        self.image = self.images[self.frame//8%2]
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
        self.image = self.images[self.frame//8%2]
        if self.type == "bkshell":
            self.image = self.images[self.frame//12%2]
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
        self.image = self.images[self.frame//2%2]
        if self.type == "cannon":
            self.image = self.images[self.frame//12%2]
        elif self.type == "cannonbig":
            self.image = self.images[self.frame//12%2]
        elif self.type == "smallcannon":
            self.image = self.images[self.frame//12%2]
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
        self.image = self.images[self.frame//8%2]


        
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
            self.image = self.images[self.timer//4%2]
        elif self.timer < 36:
            self.image = self.images[self.timer//4%2]
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
        self.angle = int(270.0 - (angle * 180) //math.pi)
    def update(self):
        self.rect.center = (self.x, self.y)
        speed = 3
        self.x += math.sin(math.radians(self.angle))*speed
        self.y += math.cos(math.radians(self.angle))*speed
        self.frame += 1
        self.image = self.images[self.frame//8%2]
                                      
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
            self.image = self.images[self.timer//4%3]
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
            self.image = self.images[self.timer//4%3]
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
        self.image = self.images[self.frame//6%4]

class CoinDie(Collidable):
    def __init__(self, pos):
        Collidable.__init__(self, self.groups) 
        self.image = self.images[0]
        self.rect = self.image.get_rect(center = pos)
        self.timer = 0
   
    def update(self):
        self.timer += 1
        if self.timer < 12:
            self.image = self.images[self.timer//4%3]
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
            self.image = self.images[self.timer//4%3]
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
            self.image = self.images[self.frame//50%4]
            if self.hit_timer > 0:
                self.image = self.images[self.frame//50%4 + 1]
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

class Level:

    def __init__(self, lvl=1):
        self.level = pygame.image.load(filepath(("levels/lvl%d.png" % lvl))).convert()
        self.x = 0
        self.y = 0
        for y in range(self.level.get_height()):
            self.y = y
            for x in range(self.level.get_width()):
                self.x = x
                color = self.level.get_at((self.x, self.y))
                if color == (0, 0, 0, 255):
                    l=r=False
                    tile = "middle"
                    if self.get_at(0, -1) != (0, 0, 0, 255):
                        tile = "top"
                    if self.get_at(-1, 0) != (0, 0, 0, 255):
                        l=True
                    if self.get_at(1, 0) != (0, 0, 0, 255):
                        r=True
                    Platform((self.x*32, self.y*32), tile, l, r)
                    
                if color == (0, 19, 127, 255):
                    l=r=False
                    tile = "1"
                    if self.get_at(0, -1) != (0, 19, 127, 255):
                        tile = "middle"
                    if self.get_at(-1, 0) != (0, 19, 127, 255):
                        l=True
                    if self.get_at(1, 0) != (0, 19, 127, 255):
                        r=True
                        
                    Grass((self.x*32, self.y*32), tile, l, r)    


                if color == (109, 127, 63, 255):
                    l=r=False
                    tile = "1"
                    if self.get_at(0, -1) != (109, 127, 63, 255):
                        tile = "2"
                    if self.get_at(-1, 0) != (109, 127, 63, 255):
                        l=True
                    if self.get_at(1, 0) != (109, 127, 63, 255):
                        r=True

                    Brick((self.x*32, self.y*32), tile, l, r)

                if color == (127, 255, 255, 255):
                    l=r=False
                    tile = "1"
                    if self.get_at(0, -1) != (127, 255, 255, 255):
                        tile = "2"
                    if self.get_at(-1, 0) != (127, 255, 255, 255):
                        l=True
                    if self.get_at(1, 0) != (127, 255, 255, 255):
                        r=True

                    Brickblue((self.x*32, self.y*32), tile, l, r)    

                if color == (160, 160, 160, 255):
                    l=r=False
                    tile = "1"
                    if self.get_at(0, -1) != (160, 160, 160, 255):
                        tile = "2"
                    if self.get_at(-1, 0) != (160, 160, 160, 255):
                        l=True
                    if self.get_at(1, 0) != (160, 160, 160, 255):
                        r=True

                    Gray((self.x*32, self.y*32), tile, l, r)

                if color == (127, 89, 63, 255):
                    l=r=False
                    tile = "1"
                    if self.get_at(0, -1) != (127, 89, 63, 255):
                        tile = "2"
                    if self.get_at(-1, 0) != (127, 89, 63, 255):
                        l=True
                    if self.get_at(1, 0) != (127, 89, 63, 255):
                        r =True

                    Bridge((self.x*32, self.y*32), tile, l, r)

                if color == (102, 124, 255, 255):
                    l=r=False
                    tile = "1"
                    if self.get_at(0, -1) != (102, 124, 255, 255):
                        tile = "2"
                    if self.get_at(-1, 0) != (102, 124, 255, 255):
                        l=True
                    if self.get_at(1, 0) != (102, 124, 255, 255):
                        r =True

                    Platformblue((self.x*32, self.y*32), tile, l, r)

                if color == (0, 255, 104, 255):
                    l=r=False
                    tile = "1"
                    if self.get_at(0, -1) != (0, 255, 104, 255):
                        tile = "2"
                    if self.get_at(-1, 0) != (0, 255, 104, 255):
                        l=True
                    if self.get_at(1, 0) != (0, 255, 104, 255):
                        r =True

                    Mountain((self.x*32, self.y*32), tile, l, r)    

                if color == (255, 200, 0, 255):
                    AirPlatform((self.x*32, self.y*32))
                if color == (192, 192, 192, 255):
                    AirPlatformblue((self.x*32, self.y*32))
                if color == (127, 51, 0, 255):
                    PlatformQ((self.x*32, self.y*32))
                if color == (0, 74, 127, 255):
                    Platform_Brick((self.x*32, self.y*32))
                if color == (128, 128, 128, 255):
                    Flag((self.x*31.9, self.y*10))
                if color == (91, 127, 0, 255):
                    Pipe((self.x*32, self.y*28))
                if color == (255, 192, 109, 255):
                    PipeEnd((self.x*32, self.y*24))
                if color == (63, 127, 98, 255):
                    Firebowser((self.x*32, self.y*32))
                if color == (87, 0, 127, 255):
                    Cloud((self.x*32, self.y*32))
                if color == (127, 0, 55, 255):
                    Bush((self.x*32, self.y*32))
                if color == (127, 255, 142, 255):
                    Bush2((self.x*32, self.y*32))
                if color == (127, 201, 255, 255):
                    Bush3((self.x*32, self.y*32))
                if color == (80, 63, 127, 255):
                    Castle((self.x*32, self.y*22))
                if color == (255, 233, 127, 255):
                    Hill((self.x*32, self.y*29))
                if color == (218, 255, 127, 255):
                    Hill2((self.x*32, self.y*31.5))
                if color == (0, 0, 255, 255):
                    Baddie((self.x*32 + 2, self.y*32 + 4), "monster")
                if color == (0, 255, 255, 255):
                    Baddie((self.x*32 + 1, self.y*32 + 2), "slub")
                if color == (255, 217, 78, 255):
                    Baddie((self.x*32 + 1, self.y*32 + 2), "blue")
                if color == (255, 177, 104, 255):
                    Baddie((self.x*32 + 2, self.y*32 + 4), "black")
                if color == (255, 0, 255, 255):
                    Baddie((self.x*32 + 1, self.y*32 + 2), "squidge")
                if color == (76, 255, 0, 255):
                    Cannon((self.x*32 + 1, self.y*29.3 + 4), "cannon") # 1
                if color == (63, 73, 127, 255):
                    Cannon((self.x*32 + 1, self.y*26.5 + 4), "cannonbig") # 1
                if color == (255, 127, 182, 255):
                    Cannon((self.x*32 + 1, self.y*32 + 2), "smallcannon") # 1
                if color == (127, 0, 110, 255):
                    Flower((self.x*32.5, self.y*28.8 + 2), "flower")
                if color == (255, 217, 101, 255):
                    Flowertwo((self.x*32.1, self.y*31.5), "flowertwo")
                if color == (252, 255, 89, 255):
                    Flowerthree((self.x*32.07, self.y*30.2), "flowerthree")
                if color == (175, 10, 35, 255):
                    Flowerblue((self.x*32.1, self.y*31.5), "flowerblue")
                if color == (233, 255, 112, 255):
                    Spiker((self.x*32, self.y*32), "spiker")
                if color == (255, 255, 142, 255):
                    Sky((self.x*32, self.y*32), "sky")
                if color == (255, 0, 0, 255):
                    MovingPlatform((self.x*32, self.y*32))
                if color == (82, 127, 63, 255):
                    MovingPlatformtwo((self.x*32, self.y*32))
                if color == (174, 0, 255, 255):
                    Underground((self.x*32, self.y*32))
                if color == (255, 255, 0, 255):
                    Coin((self.x*32 + 4, self.y*32 + 4))
                if color == (0, 255, 0, 255):
                    Bomb((self.x*31.9, self.y*10))
                if color == (0, 200, 0, 255):
                    Spring((self.x*32, self.y*32))
                if color == (200, 0, 0, 255):
                    Boss((self.x*32, self.y*32 + 4))
                if color == (0, 127, 70, 255):
                    MushroomGreen((self.x*32, self.y*32))
                if color == (255, 127, 237, 255):
                    Axe((self.x*32, self.y*32))
                if color == (178, 0, 255, 255):
                    PipeBig((self.x*32, self.y*25))
                if color == (64, 64, 64, 255):
                    Fence((self.x*32, self.y*32))
                if color == (182, 255, 0, 255):
                    Tree1((self.x*32, self.y*27))
                if color == (255, 0, 220, 255):
                    Cloud2((self.x*32, self.y*32))
                if color == (72, 0, 255, 255):
                    Rose((self.x*32.23, self.y*27.8 + 2), "flower2")
                if color ==(255, 106, 0, 255):
                    Baddie((self.x*32 + 2, self.y*32 + 4), "monsterred")
                if color ==(0, 255, 59, 255):
                    Baddie((self.x*32 + 2, self.y*32 + 4), "monsterblue")
                if color ==((38, 127, 0, 255)):
                    Tree2((self.x*32, self.y*29.7))
                if color ==((0, 127, 127, 255)):
                    Grasstexture((self.x*32, self.y*32))
                if color ==((255, 0, 110, 255)):
                    Grass1((self.x*32, self.y*32))
                if color ==((165, 255, 127, 255)):
                    Grass2((self.x*32, self.y*32))
                if color ==((255, 127, 127, 255)):
                    GrassSprite((self.x*32, self.y*32))
                if color ==((127, 255, 197, 255)):
                    Wall((self.x*32, self.y*19))
                if color == ((214, 127, 255, 255)):
                    Castlebig((self.x*32, self.y* 6))
                if color == ((234, 106, 68, 255)):
                    Lava((self.x*32, self.y*32))
                if color == ((127, 116, 63, 255)):
                    Chain((self.x*32, self.y*32))
                if color == ((217, 106, 0, 255)):
                    Toad((self.x*32, self.y*30.6))
                if color == ((127, 63, 118, 255)):
                    Invisiblewall((self.x*32, self.y*32))
                if color == ((147, 167, 61, 255)):
                    PipeDown((self.x*32, self.y*32))
                if color == ((150, 82, 0, 255)):
                    PipeGreen((self.x*32, self.y*27))
                if color == ((255, 81, 87, 255)):
                    PipeGreenBig((self.x*32, self.y*24))
                if color == ((255, 182, 0, 255)):
                    PipeGreenEnd((self.x*32.1, self.y*7))
                if color == ((255, 252, 122, 255)):
                    Flag2((self.x*31, self.y*7.5))
                if color == ((196, 255, 48, 255)):
                    Railing((self.x*32, self.y*33.5))
                                              
    def get_at(self, dx, dy):
        try:
            return self.level.get_at((self.x+dx, self.y+dy))
        except:
            pass
            
    def get_size(self):
        return [self.level.get_size()[0]*32, self.level.get_size()[1]*32]

def cutscene(screen, text):
    font = pygame.font.Font(filepath("fonts/font.ttf"), 16)
    black = pygame.Surface((640, 480))
    black.fill((0, 0, 0))
    alpha = 255
    intro = True
    outro = False
    height = len(text)*(font.get_height()+3)
    image = pygame.Surface((640, height))
    y = 0
    for line in text:
        ren = font.render(line, 1, (255, 255, 255))
        image.blit(ren, (320-ren.get_width()//2, y*(font.get_height()+3)))
        y += 1
    while 1:
        pygame.time.wait(10)
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()
            if e.type == K_c:
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    return
                if e.key in (K_SPACE, K_RETURN):
                    intro = False
                    outro = True
        if intro:
            if alpha > 0:
                alpha -= 5
        if outro:
            if alpha < 255:
                alpha += 5
            else:
                return
        black.set_alpha(alpha)
        screen.fill((0, 0, 0))
        screen.blit(image, (0, 240-image.get_height()//2))
        screen.blit(black, (0, 0))
        ren = font.render("Press Enter to continue", 1, (255, 255, 255))
        screen.blit(ren, (320-ren.get_width()//2, 460))
        pygame.display.flip()

def RelRect(actor, camera):
    return Rect(actor.rect.x-camera.rect.x, actor.rect.y-camera.rect.y, actor.rect.w, actor.rect.h)

class Camera(object):
    def __init__(self, player, width):
        self.player = player
        self.rect = pygame.display.get_surface().get_rect()
        self.world = Rect(0, 0, width, 480)
        self.rect.center = self.player.rect.center
        
    def update(self):
        if self.player.rect.centerx > self.rect.centerx+1:
            self.rect.centerx = self.player.rect.centerx-64
            
        self.rect.clamp_ip(self.world)
    def draw_sprites(self, surf, sprites):
        for s in sprites:
            if s.rect.colliderect(self.rect):
                surf.blit(s.image, RelRect(s, self))

def save_level(lvl):
    open(filepath("saves/prog.sav"), "w").write(str(lvl))
    
def get_saved_level():
    try:
        return int(open(filepath("saves/prog.sav")).read())
    except:
        open(filepath("saves/prog.sav"),  "w").write(str(1))
        return 1

def save_coin(coin):
    open(filepath("saves/coin.sav"), "w").write(str(coin))
    
def get_saved_coin():
    try:
        return int(open(filepath("saves/coin.sav")).read())
    except:
        open(filepath("saves/coin.sav"),  "w").write(str(1))
        return 1

def save_score(score):
    open(filepath("saves/score.sav"), "w").write(str(score))

def get_saved_score():
    try:
        return int(open(filepath("saves/score.sav")).read())
    except:
        open(filepath("saves/score.sav"),  "w").write(str(1))
        return 1

def save_lives(lives):
    open(filepath("saves/lives.sav"), "w").write(str(lives))

def get_saved_lives():
    try:
        return int(open(filepath("saves/lives.sav")).read())
    except:
        open(filepath("saves/lives.sav"),  "w").write(str(1))
        return 1

class Game(object):

    def __init__(self, screen, continuing=False):

        self.screen = screen
        self.sprites = pygame.sprite.OrderedUpdates()
        self.players = pygame.sprite.OrderedUpdates()
        self.platforms = pygame.sprite.OrderedUpdates()
        self.platformblues = pygame.sprite.OrderedUpdates() 
        self.grasss = pygame.sprite.OrderedUpdates()
        self.grays = pygame.sprite.OrderedUpdates()
        self.bricks = pygame.sprite.OrderedUpdates()
        self.brickblues = pygame.sprite.OrderedUpdates()
        self.movingplatforms = pygame.sprite.OrderedUpdates()
        self.movingplatformtwos = pygame.sprite.OrderedUpdates()
        self.undergrounds = pygame.sprite.OrderedUpdates()
        self.baddies = pygame.sprite.OrderedUpdates()
        self.cannons = pygame.sprite.OrderedUpdates()
        self.flowers = pygame.sprite.OrderedUpdates()
        self.flowertwos = pygame.sprite.OrderedUpdates()
        self.flowerthrees = pygame.sprite.OrderedUpdates()
        self.firebowsers = pygame.sprite.OrderedUpdates()
        self.spikeshots = pygame.sprite.OrderedUpdates()
        self.roses = pygame.sprite.OrderedUpdates()
        self.nomoveplatforms = pygame.sprite.OrderedUpdates()
        self.coins = pygame.sprite.OrderedUpdates()
        self.playerdying = pygame.sprite.OrderedUpdates()
        self.bombs = pygame.sprite.OrderedUpdates()
        self.shots = pygame.sprite.OrderedUpdates()
        self.springs = pygame.sprite.OrderedUpdates()
        self.bosses = pygame.sprite.OrderedUpdates()
        self.platformqs = pygame.sprite.OrderedUpdates()
        self.mushroomgreens = pygame.sprite.OrderedUpdates()
        self.axes = pygame.sprite.OrderedUpdates()
        self.bridges = pygame.sprite.OrderedUpdates()
        self.toads = pygame.sprite.OrderedUpdates()
        self.spikers = pygame.sprite.OrderedUpdates()
        self.skys = pygame.sprite.OrderedUpdates()
        self.pipegreenends = pygame.sprite.OrderedUpdates()
        self.flag2s = pygame.sprite.OrderedUpdates()
        self.pipeends = pygame.sprite.OrderedUpdates()
        self.flowerblues = pygame.sprite.OrderedUpdates()
        self.mountains = pygame.sprite.OrderedUpdates()
        self.hill2 = pygame.sprite.OrderedUpdates()
        self.bush2 = pygame.sprite.OrderedUpdates()
        self.bush3 = pygame.sprite.OrderedUpdates()
        
        Player.right_images = [load_image("mario1.png"), load_image("mario2.png"), load_image("mario3.png"), load_image("mario4.png"), load_image("mario5.png")]
        Platform.images = {"platform-top.png": load_image("platform-top.png"), "platform-middle.png": load_image("platform-top.png")}
        Platformblue.images = {"platform-blue1.png": load_image("platform-blue1.png"), "platform-blue2.png": load_image("platform-blue1.png")}
        Grass.images = {"grass-1.png": load_image("grass-1.png"), "grass-middle.png": load_image("grass-middle.png")}
        Mountain.images = {"mountains1.png": load_image("mountains1.png"), "mountains2.png": load_image("mountains2.png")}
        Gray.images = {"gray1.png": load_image("gray1.png"), "gray2.png": load_image("gray2.png")}
        Brick.images = {"brick1.png": load_image("brick1.png"), "brick2.png": load_image("brick2.png")}
        Brickblue.images = {"brickblue1.png": load_image("brickblue1.png"), "brickblue2.png": load_image("brickblue2.png")}
        Bridge.images = {"bridge.png": load_image("bridge.png"), "bridge2.png": load_image("bridge2.png")}
        MovingPlatform.image = load_image("moving-platform.png")
        Firebowser.images = [load_image("bowser-fireball%s.png" % i) for i in range(1, 3)]
        MovingPlatformtwo.image = load_image("moving-platformlong.png")
        Underground.image = load_image("moving-platformlong.png")
        Baddie.left_images1 = [load_image("monster%d.png" % i) for i in range(1, 3)]
        Baddie.left_images2 = [load_image("slub%d.png" % i) for i in range(1, 3)]
        Baddie.left_images3 = [load_image("squidge%d.png" % i) for i in range(1, 3)]
        Baddie.left_images4 = [load_image("monster-red%d.png" % i) for i in range(1, 3)]
        Baddie.left_images5 = [load_image("slubblue%d.png" % i) for i in range(1, 3)]
        Baddie.left_images6 = [load_image("bluemonster%d.png" % i) for i in range(1, 3)]
        Baddie.left_images7 = [load_image("black%d.png" % i) for i in range(1, 3)]
        Cannon.left_images1 = [load_image("cannon%d.png" % i) for i in range(1, 3)]
        Cannon.left_images2 = [load_image("cannonbig%d.png" % i) for i in range(1, 3)]
        Cannon.left_images4 = [load_image("smallcannon%d.png" % i) for i in range(1, 3)]
        Spiker.left_images1 = [load_image("spiker%d.png" % i) for i in range(1, 3)]
        Sky.left_images1 = [load_image("sky%d.png" % i) for i in range(1, 2)]
        BaddieBoom.left_images1 = [load_image("monster2.png"), load_image("monster3.png"), load_image("exp1.png"), load_image("exp2.png"), load_image("exp3.png")]
        BaddieBoom.left_images2 = [load_image("slub2.png"), load_image("slub3.png"), load_image("exp1.png"), load_image("exp2.png"), load_image("exp3.png")]
        BaddieBoom.left_images3 = [load_image("squidge2.png"), load_image("squidge3.png"), load_image("exp1.png"), load_image("exp2.png"), load_image("exp3.png")]
        BaddieBoom.left_images4 = [load_image("monster-red2.png"), load_image("monster-red3.png"), load_image("exp1.png"), load_image("exp2.png"), load_image("exp3.png")]
        BaddieBoom.left_images5 = [load_image("slubblue2.png"), load_image("slubblue3.png"), load_image("exp1.png"), load_image("exp2.png"), load_image("exp3.png")]
        BaddieBoom.left_images6 = [load_image("bluemonster2.png"), load_image("bluemonster3.png"), load_image("exp1.png"), load_image("exp2.png"), load_image("exp3.png")]
        BaddieBoom.left_images7 = [load_image("black2.png"), load_image("black3.png"), load_image("exp1.png"), load_image("exp2.png"), load_image("exp3.png")]
        Coin.images = [load_image("coin%s.png" % i) for i in range(1, 5)]
        CoinDie.images = [load_image("exp2-%d.png" % i) for i in range(1, 4)]
        PlayerDie.right_images = [load_image("mariodie.png"), load_image("exp2-1.png"), load_image("exp2-2.png"), load_image("exp2-3.png")]
        Bomb.image = load_image("flagpole.png")
        Flag2.image = load_image("flagpole.png")
        Toad.image = load_image("toad.png")
        BaddieShot.image = load_image("shot.png")
        SpikeShot.images = [load_image("spikeshot%s.png" % i) for i in range(1, 3)]
        Fireball.images = [load_image("bowser-fireball%s.png" % i) for i in range(1, 3)]
        CannonShot.image = load_image("cannonbullet1.png")
        CannonShotbig.image = load_image("cannonbullet1.png")
        CannonShotsmall.image = load_image("cannonbullet1.png")
        Spring.images = [load_image("spring1.png"), load_image("spring2.png")]
        AirPlatform.image = load_image("platform-air.png")
        AirPlatformblue.image = load_image("platform-blue3.png")
        PlatformQ.images = [load_image("platform-q%s.png" % i) for i in range (1, 4)]
        Pipe.image = load_image("pipe.png")
        Flag.image = load_image("flagpole.png")
        Castle.image = load_image("castle.png")
        Castlebig.image = load_image("castle-big.png")
        Hill.image = load_image("hill.png")
        Bush.image = load_image("bush-1.png")
        Bush2.image = load_image("bush-2.png")
        Bush3.image = load_image ("bush-3.png")
        Cloud.image = load_image("cloud.png")
        Cloud2.image = load_image("dobbelclouds.png")
        Platform_Brick.image = load_image("platform-brick.png")
        Boss.left_images = [load_image("bowser1.png"), load_image("bowser2.png"), load_image("bowser3.png"), load_image("bowser4.png")]
        Flower.left_images1 = [load_image("flower%d.png" % i) for i in range(1, 2)]
        Flowertwo.left_images1 = [load_image("flower%d.png" % i) for i in range(1, 2)]
        Flowerthree.left_images1 = [load_image("flower%d.png" % i) for i in range(1, 2)]
        Flowerblue.left_images1 = [load_image("blueflower%d.png" % i) for i in range(1, 2)]
        MushroomGreen.image = load_image("mushroom-green.png")
        MushroomGreendie.images = [load_image("exp2-%d.png" % i) for i in range(1, 4)]
        Axe.image = load_image("trigger.png")
        AxeDie.images = [load_image("exp2-%d.png" % i) for i in range(1, 4)]
        PipeBig.image = load_image("pipe-big.png")
        Fence.image = load_image("fence.png")
        Tree1.image = load_image("tree-1.png")
        Tree2.image = load_image("tree-2.png")
        Rose.image = load_image ("rose2.png")
        Grasstexture.image = load_image("grass-texture.png")
        Grass1.image = load_image("grass-1.png")
        Grass2.image = load_image("grass-2.png")
        GrassSprite.image = load_image("grass-texturesprite.png") 
        Wall.image = load_image("wall-1.png")
        Lava.image = load_image("lava.png")
        Chain.image = load_image("chain.png")
        Invisiblewall.image = load_image("invisible_wall.png")
        PipeEnd.image = load_image("pipe-end.png")
        PipeDown.image = load_image("pipe_down.png")
        PipeGreen.image = load_image("pipe_green.png")
        PipeGreenBig.image = load_image("pipe_greenbig.png")
        PipeGreenEnd.image = load_image("pipe_greenend.png")
        Railing.image = load_image("railing.png")
        Hill2.image = load_image("hill2.png")

        Player.groups = self.sprites, self.players
        Platform.groups = self.sprites, self.platforms, self.nomoveplatforms
        Platformblue.groups = self.sprites, self.platformblues, self.nomoveplatforms
        Grass.groups = self.sprites, self.grasss, self.nomoveplatforms
        Brick.groups = self.sprites, self.bricks, self.nomoveplatforms
        Brickblue.groups = self.sprites, self.brickblues, self.nomoveplatforms
        Gray.groups = self.sprites, self.grays, self.nomoveplatforms
        MovingPlatform.groups = self.sprites, self.platforms, self.movingplatforms
        MovingPlatformtwo.groups = self.sprites, self.platforms, self.movingplatformtwos
        Underground.groups = self.sprites, self.platforms, self.undergrounds
        Baddie.groups = self.sprites, self.baddies
        Cannon.groups = self.sprites, self.cannons, self.platforms
        BaddieBoom.groups = self.sprites
        Coin.groups = self.sprites, self.coins
        CoinDie.groups = self.sprites
        MushroomGreen.groups = self.sprites, self.mushroomgreens
        MushroomGreendie.groups = self.sprites
        Axe.groups = self.sprites, self.axes
        AxeDie.groups = self.sprites
        PlayerDie.groups = self.sprites, self.playerdying
        Bomb.groups = self.sprites, self.bombs
        Toad.groups = self.sprites, self.toads
        BaddieShot.groups = self.sprites, self.shots
        SpikeShot.groups = self.sprites, self.shots, self.spikeshots
        Fireball.groups = self.sprites, self.shots
        CannonShot.groups = self.sprites, self.shots
        CannonShotbig.groups = self.sprites, self.shots
        CannonShotsmall.groups = self.sprites, self.shots
        Spring.groups = self.sprites, self.springs
        AirPlatform.groups = self.sprites, self.platforms, self.nomoveplatforms
        AirPlatformblue.groups = self.sprites, self.platforms, self.nomoveplatforms
        Pipe.groups = self.sprites, self.platforms, self.nomoveplatforms
        PlatformQ.groups = self.sprites, self.platformqs, self.platforms
        Platform_Brick.groups = self.sprites, self.platforms, self.nomoveplatforms
        Flag.groups = self.sprites
        Flag2.groups = self.sprites, self.flag2s
        Castle.groups = self.sprites
        Castlebig.groups = self.sprites
        Cloud.groups = self.sprites
        Cloud2.groups = self.sprites
        Bush.groups = self.sprites
        Hill.groups = self.sprites
        Boss.groups = self.sprites, self.bosses
        Flower.groups = self.sprites, self.flowers
        Flowertwo.groups = self.sprites, self.flowertwos
        Flowerthree.groups = self.sprites, self.flowerthrees
        Flowerblue.groups = self.sprites, self.flowerblues
        PipeBig.groups = self.sprites, self.platforms, self.nomoveplatforms
        Firebowser.groups = self.sprites, self.firebowsers
        Fence.groups = self.sprites
        Tree1.groups = self.sprites
        Tree2.groups = self.sprites
        Rose.groups = self.sprites, self.roses
        Grasstexture.groups = self.sprites, self.platforms, self.nomoveplatforms
        Grass1.groups = self.sprites, self.platforms, self.nomoveplatforms
        Grass2.groups = self.sprites, self.platforms, self.nomoveplatforms
        GrassSprite.groups = self.sprites
        Wall.groups = self.sprites
        Lava.groups = self.sprites
        Bridge.groups = self.sprites, self.bridges, self.platforms, self.nomoveplatforms
        Chain.groups = self.sprites
        Invisiblewall.groups = self.sprites, self.platforms, self.nomoveplatforms
        Spiker.groups = self.sprites, self.spikers
        PipeEnd.groups = self.sprites, self.pipeends
        Sky.groups = self.sprites, self.skys
        PipeDown.groups = self.sprites
        PipeGreen.groups = self.sprites, self.platforms, self.nomoveplatforms
        PipeGreenBig.groups = self.sprites, self.platforms, self.nomoveplatforms
        PipeGreenEnd.groups = self.sprites, self.pipegreenends
        Mountain.groups = self.sprites, self.nomoveplatforms, self.mountains, self.platforms
        Railing.groups = self.sprites
        Hill2.groups = self.sprites
        Bush2.groups = self.sprites
        Bush3.groups = self.sprites
        
        self.score = 0
        self.coin = 0
        self.lives = 3
        self.lvl   = 1 #Edit what level to start at
        if continuing:
            self.lvl = get_saved_level()
            self.coin = get_saved_coin()
            self.score = get_saved_score()
            self.lives = get_saved_lives()  
        self.player = Player((0, 0))
        self.clock = pygame.time.Clock()
        self.bg = load_image("background-2.png")
        self.level = Level(self.lvl)
        self.camera = Camera(self.player, self.level.get_size()[0])
        self.font = pygame.font.Font(filepath("fonts/font.ttf"), 16)
        self.heart1 = load_image("mario1.png")
        self.heart2 = load_image("mario-life2.png")
        self.heroimg = load_image("mario5.png")
        self.heroimg2 = load_image("coin1.png")
        self.baddie_sound = load_sound("jump2.ogg")
        self.coin_sound = load_sound("coin.ogg")
        self.hurry_sound = load_sound("hurry-main.ogg", 0.05)
        self.win_sound = load_sound("miniboss.ogg", 0.05)
        self.up_sound = load_sound("1up.ogg")
        self.pipe_sound = load_sound("pipe.ogg")
        self.bonus_sound = load_sound("bonus.ogg")
        self.bowser_sound = load_sound("bowser.ogg", 0.08)
        self.time = 400
        self.running = 1
        self.booming = True
        self.boom_timer = 0
        self.music = "maintheme.ogg"
        if self.lvl == 1:
            self.intro_level() 
        if self.lvl == 2:
            self.intro_level()
        if self.lvl == 3:
            self.world1_2()
        if self.lvl == 4:
            self.world1_2()
        if self.lvl == 5:
            self.world1_3()
        if self.lvl == 6:
            self.world1_4()
            if continuing:
                self.music = "castle.ogg"
                self.bg = load_image("background-1.png")
        if self.lvl == 7:
            self.world2_1()
        if self.lvl == 8:
            self.world2_2()
        if self.lvl == 9:
            self.time = 250
            self.world2_3()        
        if self.lvl == 10:
            self.time = 250
            self.world2_4()
            if continuing:
                self.bg = load_image("background-1.png")
        if self.lvl == 11:
            self.time = 250
            self.world2_5()
            if continuing:
                self.bg = load_image("background-2.png")
           
        if not continuing:
            stop_music()

        self.main_loop()

    def end(self):
        self.running = 0
        
    def intro_level(self):
        stop_music()
        self.screen.fill((0, 0, 0))
        self.draw_stats()
        ren = self.font.render("World 1-%d" % self.lvl, 1, (255, 255, 255))
        self.screen.blit(ren, (320-ren.get_width()/2, 230))   
        ren = self.font.render("Lives x%d" % self.lives, 1, (255, 255, 255))
        self.screen.blit(ren, (320-ren.get_width()/2, 255))
        pygame.display.flip()
        pygame.time.wait(2500)
        play_music(self.music)

    def world1_2(self):
        stop_music()
        self.screen.fill((0, 0, 0))
        self.draw_stats()
        if self.lvl == 3: # (World 1-2)
            ren = self.font.render("World 1-2", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 230))
        if self.lvl == 4:
            ren = self.font.render("World 1-2", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 230))
        ren = self.font.render("Lives x%d" % self.lives, 1, (255, 255, 255))
        self.screen.blit(ren, (320-ren.get_width()/2, 255))
        pygame.display.flip()
        pygame.time.wait(2500)
        play_music(self.music)
        
    def world1_3(self):
        stop_music()
        self.screen.fill((0, 0, 0))
        self.draw_stats()
        if self.lvl == 5: # (World 1-3)
            ren = self.font.render("World 1-3", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 230))
        ren = self.font.render("Lives x%d" % self.lives, 1, (255, 255, 255))
        self.screen.blit(ren, (320-ren.get_width()/2, 255))
        pygame.display.flip()
        pygame.time.wait(2500)
        play_music(self.music)

        
    def world1_4(self):
        stop_music()
        self.screen.fill((0, 0, 0))
        self.draw_stats()
        if self.lvl == 6: # (World 1-4)
            ren = self.font.render("World 1-4", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 230))
        ren = self.font.render("Lives x%d" % self.lives, 1, (255, 255, 255))
        self.screen.blit(ren, (320-ren.get_width()/2, 255))
        pygame.display.flip()
        pygame.time.wait(2500)
        play_music(self.music)

    def world2_1(self):
        stop_music()
        self.screen.fill((0, 0, 0))
        self.draw_stats()
        if self.lvl == 7: # (World 2-1)
            ren = self.font.render("World 2-1", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 230))
        ren = self.font.render("Lives x%d" % self.lives, 1, (255, 255, 255))
        self.screen.blit(ren, (320-ren.get_width()/2, 255))
        pygame.display.flip()
        pygame.time.wait(2500)
        play_music(self.music)

    def world2_2(self):
        stop_music()
        self.screen.fill((0, 0, 0))
        self.draw_stats()
        if self.lvl == 8: # (World 2-2)
            ren = self.font.render("World 2-2", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 230))
        ren = self.font.render("Lives x%d" % self.lives, 1, (255, 255, 255))
        self.screen.blit(ren, (320-ren.get_width()/2, 255))
        pygame.display.flip()
        pygame.time.wait(2500)
        play_music(self.music)

    def world2_3(self):
        stop_music()
        self.screen.fill((0, 0, 0))
        self.draw_stats()
        if self.lvl == 9: # (World 2-3)
            ren = self.font.render("World 2-3", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 230))
        ren = self.font.render("Lives x%d" % self.lives, 1, (255, 255, 255))
        self.screen.blit(ren, (320-ren.get_width()/2, 255))
        pygame.display.flip()
        pygame.time.wait(2500)
        play_music(self.music)

    def world2_4(self):
        stop_music()
        self.screen.fill((0, 0, 0))
        self.draw_stats()
        if self.lvl == 10: # (World 2-4)
            ren = self.font.render("World 2-4", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 230))
        ren = self.font.render("Lives x%d" % self.lives, 1, (255, 255, 255))
        self.screen.blit(ren, (320-ren.get_width()/2, 255))
        pygame.display.flip()
        pygame.time.wait(2500)
        play_music(self.music)

    def world2_5(self):
        stop_music()
        self.screen.fill((0, 0, 0))
        self.draw_stats()
        if self.lvl == 11: # (World FINAL)
            ren = self.font.render("FINAL CHAPTER", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 230))
        ren = self.font.render("Lives x%d" % self.lives, 1, (255, 255, 255))
        self.screen.blit(ren, (320-ren.get_width()/2, 255))
        pygame.display.flip()
        pygame.time.wait(2500)
        play_music(self.music)
        
    def next_level(self):

        self.hurry_sound.stop()
        self.bowser_sound.stop()
        self.time = 400
        self.booming = True
        self.boom_timer = 0
        try:
            self.lvl += 1
            self.coin == self.coin
            self.score == self.score
            self.lives == self.lives
            
            if self.lvl == 1:
                self.intro_level()
            if self.lvl == 2:
                self.intro_level()
            if self.lvl == 4:
                self.music = "maintheme.ogg"
            if self.lvl == 5:
                self.world1_3()
                self.booming = False
            if self.lvl == 6:
                self.music = "castle.ogg"
                self.world1_4()
                self.booming = False
            if self.lvl == 7:
                self.music = "maintheme.ogg"
                self.world2_1()
                self.booming = False
            if self.lvl == 8:
                self.world2_2()
                self.booming = False
            if self.lvl == 9:
                self.time = 250
                self.world2_3()
                self.booming = False
            if self.lvl == 10:
                self.time = 250
                self.world2_4()
                self.booming = False
            if self.lvl == 11:
                self.time = 250
                self.world2_5()
                self.booming = False
                
            self.clear_sprites()
            self.level = Level(self.lvl)
            self.player = Player((0, 430))
            self.camera = Camera(self.player, self.level.get_size()[0])
            save_level(self.lvl)
            save_coin(self.coin)
            save_score(self.score)
            save_lives(self.lives)
        except:
            if self.lives == 0: # Fix
                self.lives += 3
            cutscene(self.screen,
            ["Thank you for playing!",
             "",
             "",
             "Check out the tutorial on how",
             "to create your own levels!",
             "Follow the guideline",
             "in the picture",
             "in the main folder.",
             "",
             "",
             "The end"])
            self.screen.fill((0, 0, 0))
            play_music("bonus.ogg")
            
            ren = self.font.render("Your Run:", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 180))
            ren = self.font.render("Score%06d" % self.score, 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 210))
            ren = self.font.render("Lives%d" % self.lives, 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 240))
            ren = self.font.render("Coins%02d" % self.coin, 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 270))
            self.screen.blit(self.heroimg2, (240, 260))
            pygame.display.flip()
            pygame.time.wait(6000)
            self.end()
                            
    def redo_level(self):
        self.booming = False
        self.boom_timer = 0
        self.time = 400
        if self.running:
            self.clear_sprites()
            self.level = Level(self.lvl)
            self.camera = Camera(self.player, self.level.get_size()[0]) 
            self.hurry_sound.stop()
            self.bowser_sound.stop()
            self.draw_stats()
            Chain.image = load_image("chain.png")
            play_music("maintheme.ogg")
            #play_music("maintheme.ogg")
            if self.lvl == 1:
                self.player = Player((0, 430)) # Makes Player spawn at ground not mid-air.
                self.camera = Camera(self.player, self.level.get_size()[0])
            if self.lvl == 2:
                self.player = Player((0, 430))
                self.camera = Camera(self.player, self.level.get_size()[0])
            if self.lvl == 3:
                play_music("underworld.ogg") 
                self.player = Player((0, 0)) # Fall through pipe
                self.camera = Camera(self.player, self.level.get_size()[0])
                self.pipe_sound.play()
            if self.lvl == 4:
                self.player = Player((0, 430))
                self.camera = Camera(self.player, self.level.get_size()[0])
                self.pipe_sound.play()
            if self.lvl == 5:
                self.player = Player((0, 430))
                self.camera = Camera(self.player, self.level.get_size()[0])
            if self.lvl == 6:
                play_music("castle.ogg")
                self.player = Player((0, 230))
                self.camera = Camera(self.player, self.level.get_size()[0])
            if self.lvl == 7:
                self.player = Player((0, 430))
                self.camera = Camera(self.player, self.level.get_size()[0])
            if self.lvl == 8:
                self.time = 250
                self.player = Player((0, 430))
                self.camera = Camera(self.player, self.level.get_size()[0])
            if self.lvl == 9:
                self.time = 250
                self.player = Player((0, 430))
                self.camera = Camera(self.player, self.level.get_size()[0])
            if self.lvl == 10:
                self.time = 250
                self.player = Player((0, 430))
                self.camera = Camera(self.player, self.level.get_size()[0])
            if self.lvl == 11:
                self.time = 250
                self.player = Player((0, 430))
                self.camera = Camera(self.player, self.level.get_size()[0])
             
    def show_death(self):
        self.hurry_sound.stop()
        self.bowser_sound.stop()
        ren = self.font.render("YOU DIED", 1, (255, 255, 255))
        self.screen.blit(ren, (320-ren.get_width()/2, 235))
        pygame.display.flip()
        pygame.time.wait(2500)

    def toad(self):
        ren = self.font.render("THE PRINCESS IS", 1, (255, 255, 255,))
        self.screen.blit(ren, (320-ren.get_width()/2, 235))
        ren = self.font.render("IN ANOTHER CASTLE!", 1, (255, 255, 255,))
        self.screen.blit(ren, (320-ren.get_width()/2, 255))
        pygame.display.flip()
        pygame.time.wait(5000)
        cutscene(self.screen,
             ["",    
             "Normal story over",
             "time for custom made maps",
             ""])
        
    def show_end(self):
        self.hurry_sound.stop()
        self.bowser_sound.stop()
        play_music("goal.ogg")
        pygame.time.wait(7500)
        pygame.display.flip()
        
    def gameover_screen(self):
        self.hurry_sound.stop()
        self.bowser_sound.stop()
        stop_music()
        play_music("gameover.ogg")
        cutscene(self.screen, ["Game Over"])
        self.end()  
      
    def clear_sprites(self):
        for s in self.sprites:
            pygame.sprite.Sprite.kill(s)

    # MAIN PART:
     
    def main_loop(self):
        while self.running:
            BaddieShot.player = self.player
            Fireball.player = self.player
            CannonShot.player = self.player
            CannonShotbig.player = self.player
            CannonShotsmall.player = self.player
            SpikeShot.player = self.player
            if not self.running:
                return

            self.boom_timer -= 1

            self.clock.tick(60)
            self.camera.update()
            for s in self.sprites:
                s.update()

            if self.lvl == 3:
                self.bg = load_image("background-1.png")
                self.music = "underworld.ogg"
            else:
                if self.lvl == 4:
                    self.bg = load_image("background-2.png")
                    self.music = "maintheme.ogg"
            
            if self.lvl == 5:
                self.bg = load_image("background-2.png")
                self.music = "maintheme.ogg"
            else:
                if self.lvl == 6:
                    self.bg = load_image("background-1.png")
                    self.music = "castle.ogg"

            if self.lvl == 7:
                    self.bg = load_image("background-2.png")
                    self.music = "maintheme.ogg"

            if self.lvl == 10:
                    self.bg = load_image("background-1.png")
            if self.lvl == 11:
                    self.bg = load_image("background-2.png")
            
            if self.player.rect.right > self.camera.world.w:
                if not self.toads and self.lvl < 30:
                    self.next_level()
                else:
                    self.player.rect.right = self.camera.world.w

            if self.player.rect.right > self.camera.world.w:
                self.next_level()        

            self.player.collide(self.platforms)
            self.player.collide(self.springs)

            # PROJECTILES:

            for f in self.firebowsers:
                if self.player.rect.colliderect(f.rect):
                    self.player.hit()

            for s in self.shots:
                if not s.rect.colliderect(self.camera.rect):
                    s.kill()
                if s.rect.colliderect(self.player.rect):
                    self.player.hit()
                    s.kill()
            if self.booming and self.boom_timer <= 0:
                self.redo_level()

            for s in self.skys:
                if s.rect.colliderect(self.camera.rect):
                    if s.type == "sky":
                        if not random.randrange(130):
                            SpikeShot(s.rect.center)
                
            for c in self.cannons:
                c.update()
                if c.rect.colliderect(self.camera.rect):
                    if c.type == "cannon":
                        if not random.randrange(135):
                            CannonShot(c.rect.center)
                    if c.type != "cannon":
                        c.collide(self.nomoveplatforms)
                        c.collide(self.springs)
                    if c.type == "cannonbig":
                        if not random.randrange(120):
                            CannonShotbig(c.rect.center)
                    if c.type != "cannonbig":
                        c.collide(self.nomoveplatforms)
                        c.collide(self.springs)
                        c.collide(self.cannons)
                    if c.type == "smallcannon":
                         if not random.randrange(145):
                            CannonShotsmall(c.rect.center)
                    if c.type != "smallcannon":
                        c.collide(self.nomoveplatforms)
                        c.collide(self.springs)
                        c.collide(self.cannons)

            # ENDING:
            
            for b in self.bombs:
                if self.player.rect.colliderect(b.rect):
                    self.show_end()
                    self.next_level()

            for f in self.flag2s:
                if self.player.rect.colliderect(f.rect):
                    self.show_end()
                    self.next_level()
                        
            for t in self.toads:
                if self.player.rect.colliderect(t.rect):
                    self.toad()
                    self.next_level()
                if self.booming and self.boom_timer <= 0:
                   self.redo_level()

            for p in self.pipegreenends:
                if self.player.rect.colliderect(p.rect):
                    self.next_level()
                    self.pipe_sound.play()
                if self.booming and self.boom_timer <= 0:
                   self.redo_level()

            for p in self.pipeends:
                if self.player.rect.colliderect(p.rect):
                    self.next_level()
                if self.booming and self.boom_timer <= 0:
                   self.redo_level()       

            # PLATFORMS:
          
            for p in self.platforms:
                self.player.collide(self.springs)
                self.player.collide(self.platforms)

            for m in self.mountains:
                self.player.collide(self.mountains)

            for p in self.platformblues:
                self.player.collide(self.platformblues)

            for b in self.brickblues:
                self.player.collide(self.brickblues)
        
            for g in self.grasss:
                self.player.collide(self.grasss)    
    
            for b in self.bricks:
                self.player.collide(self.bricks)    

            for l in self.grays:
                self.player.collide(self.grays)

            for p in self.movingplatformtwos:
                p.collide(self.players)
                for p2 in self.platforms:
                    if p != p2:
                        p.collide_with_platforms(p2)

            for p in self.movingplatforms:
                p.collide(self.players)
                for p2 in self.platforms:
                    if p != p2:
                        p.collide_with_platforms(p2)

            for u in self.undergrounds:
                u.collide(self.players)
                for u2 in self.platforms:
                    if u != u2:
                        u.collide_with_platforms(u2)        
        
            for m in self.mushroomgreens:
                if self.player.rect.colliderect(m.rect):
                    m.kill()
                    MushroomGreendie(m.rect.center)
                    self.score += 5000
                    self.lives += 1
                    self.up_sound.play()

            # WALK THROUGH:

            for a in self.axes:
                if self.player.rect.colliderect(a.rect):
                    self.bowser_sound.stop()
                    a.kill()
                    AxeDie(a.rect.center)
                for b in self.bosses:
                    b.collide(self.nomoveplatforms)
                    b.collide(self.platforms)
                    if self.player.rect.colliderect(a.rect):
                        Chain.image = load_image("trap.png")
                for b in self.bridges:
                    if self.player.rect.colliderect(a.rect):
                        b.kill()
                        stop_music()
                        self.win_sound.play()        
                                     
            for c in self.coins:
                if self.player.rect.colliderect(c.rect):
                    c.kill()
                    self.coin_sound.play()
                    CoinDie(c.rect.center)
                    self.coin += 1
                    self.score += 50
                if self.coin == 100:
                    self.coin -= self.coin
                    self.up_sound.play()
                    self.lives += 1

            # BADDIES:
          
            for b in self.baddies:
                b.collide(self.nomoveplatforms)
                b.collide(self.springs)
                b.collide(self.cannons)        

            for s in self.spikers:
                s.collide(self.platforms)
                s.collide(self.nomoveplatforms)
                if self.player.rect.colliderect(s.rect):
                    self.player.hit()
 
            for b in self.flowers:
                if self.player.rect.colliderect(b.rect):
                    self.player.hit()

            for b in self.flowertwos:
                if self.player.rect.colliderect(b.rect):
                    self.player.hit()

            for b in self.flowerthrees:
                if self.player.rect.colliderect(b.rect):
                    self.player.hit()

            for b in self.flowerblues:
                if self.player.rect.colliderect(b.rect):
                    self.player.hit()
        
            for b in self.flowers:
                if self.player.rect.colliderect(b.rect):
                    self.player.hit()
        
            for r in self.roses:
                if self.player.rect.colliderect(r.rect):
                    self.player.hit()
             
            for b in self.bosses:
                b.collide(self.nomoveplatforms)
                if b.rect.colliderect(self.camera.rect):
                    self.bowser_sound.play()
                    stop_music()
                if self.player.rect.colliderect(b.rect) and not b.dead:
                    self.player.hit()
                if b.die_time > 0:
                    for s in self.shots:
                        s.kill() 
                    for b2 in self.baddies:
                        b2.kill()
                        BaddieBoom(b2.rect.center, b2.speed, b2.type)
                if not random.randrange(75) and not b.dead:
                    Fireball(b.rect.center)

            for b in self.baddies:
                if self.player.rect.colliderect(b.rect):
                    if self.player.jump_speed > 0 and \
                       self.player.rect.bottom < b.rect.top+10 and \
                       b.alive():
                        b.kill()
                        self.player.jump_speed = -3
                        self.player.jump_speed = -5
                        self.player.rect.bottom = b.rect.top-1
                        self.score += 100
                        self.baddie_sound.play()
                        BaddieBoom(b.rect.center, b.speed, b.type)
                    else:
                        if b.alive():
                            self.player.hit()
                            
            # TIMER:
                    
            if self.player.alive():
                self.time -= 0.060
            if self.time <= 0:
                self.player.hit()
            if self.time <= 100:
                self.hurry_sound.play()
                stop_music()

            # EVENTS (KEYBINDINGS)
                                              
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.hurry_sound.stop()
                    self.bowser_sound.stop()
                    sys.exit()    
                if e.type == KEYDOWN:
                    if e.key == K_s:
                        stop_music()
                    if e.key == K_p:
                        play_music(self.music)
                    if e.key == K_ESCAPE:
                        self.hurry_sound.stop()
                        self.bowser_sound.stop()
                        self.end()    
                    if e.key == K_z:
                        self.player.jump()     
            if not self.running:
                return
            self.screen.blit(self.bg, ((-self.camera.rect.x/1)%640, 0))
            self.screen.blit(self.bg, ((-self.camera.rect.x/1)%640 + 640, 0))
            self.screen.blit(self.bg, ((-self.camera.rect.x/1)%640 - 640, 0))
            self.camera.draw_sprites(self.screen, self.sprites)
            self.draw_stats()
            if not self.player.alive() and not self.playerdying:
                if self.lives <= 0:
                    self.gameover_screen()
                else:
                    self.show_death()
                    self.lives -= 1
                    self.redo_level()
            pygame.display.flip()
            if not self.running:
                return

    def draw_stats(self):
        for i in range(1):
            self.screen.blit(self.heart2, (16 + i*34, 16))
        for i in range(self.player.hp):
            self.screen.blit(self.heart1, (16 + i*34, 16))
        self.screen.blit(self.heroimg, (313, 16))
        self.screen.blit(self.heroimg2, (235, 10))
        lives = self.lives
        if lives < 0:
            lives = 0
        ren = self.font.render("Mario", 1, (255, 255, 255))
        self.screen.blit(ren, (132-ren.get_width(), 16))
        ren = self.font.render("Score%06d" % self.score, 1, (255, 255, 255))
        self.screen.blit(ren, (228-ren.get_width(), 33))
        ren = self.font.render("x%d" % lives, 1, (255, 255, 255))
        self.screen.blit(ren, (315+34, 24))
        ren = self.font.render("x%02d" % self.coin, 1, (255, 255, 255))
        self.screen.blit(ren, (300-ren.get_width(), 16))
        ren = self.font.render("FPS    %d" % self.clock.get_fps(), 1, (255, 255, 255))
        self.screen.blit(ren, (451, 16))
        ren1 = self.font.render("Time: %d" % self.time, 1, (255, 255, 255))
        ren2 = self.font.render("Time: %d" % self.time, 1, Color("#ffffff"))
        self.screen.blit(ren1, (450, 35))
        self.screen.blit(ren2, (450, 35))
        if self.time <= 100:
            ren = self.font.render("GOTTA GO FAST", 1, (255, 255, 255))
            self.screen.blit(ren, (630-ren.get_width(), 60))

# end
            


class EzMenu:

    def __init__(self, *options):

        self.options = options
        self.x = 0
        self.y = 0
        self.font = pygame.font.Font(None, 32)
        self.option = 0
        self.width = 1
        self.color = [0, 0, 0]
        self.hcolor = [255, 0, 0]
        self.height = len(self.options)*self.font.get_height()
        for o in self.options:
            text = o[0]
            ren = self.font.render(text, 2, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()

    def draw(self, surface):
        i=0
        for o in self.options:
            if i==self.option:
                clr = self.hcolor
            else:
                clr = self.color
            text = o[0]
            ren = self.font.render(text, 2, clr)
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            surface.blit(ren, ((self.x+self.width/2) - ren.get_width()/2, self.y + i*(self.font.get_height()+4)))
            i+=1
            
    def update(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    self.option += 1
                if e.key == pygame.K_UP:
                    self.option -= 1
                if e.key == pygame.K_RETURN:    
                    self.options[self.option][1]()
        if self.option > len(self.options)-1:
            self.option = 0
        if self.option < 0:
            self.option = len(self.options)-1

    def set_pos(self, x, y):     
        self.x = x
        self.y = y
        
    def set_font(self, font):
        self.font = font
        
    def set_highlight_color(self, color):
        self.hcolor = color
        
    def set_normal_color(self, color):
        self.color = color
        
    def center_at(self, x, y):
        self.x = x-(self.width/2)
        self.y = y-(self.height/2)

data_py = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.normpath(os.path.join(data_py, '..', 'data'))

def filepath(filename):
    return os.path.join(data_dir, filename)

def load(filename, mode='rb'):

    return open(os.path.join(data_dir, filename), mode)

def load_image(filename):
	filename = filepath(filename)
	try:
		image = pygame.image.load(filename)
		image = pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))
	except pygame.error:
		raise SystemExit( "Unable to load: " + filename)
	return image.convert_alpha()

def load_sound(filename, volume=0.5):
    filename = filepath(filename)
    try:
        sound = pygame.mixer.Sound(filename)
        sound.set_volume(volume)
    except:
        raise SystemExit( "Unable to load: " + filename)
    return sound


def play_music(filename, volume=0.5, loop=-1):
    filename = filepath(filename)
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loop)
    except:
        raise SystemExit("Unable to load: " + filename)
   
def stop_music():
    pygame.mixer.music.stop()

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

            ren = self.font2.render("Game by Pranav", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 80))

            self.menu.draw(self.screen)
            pygame.display.flip()
def main():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    #pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    pygame.mouse.set_visible(0)
    pygame.display.set_icon(pygame.image.load(filepath("bowser1.gif")))
    pygame.display.set_caption("Super Mario Python")
    screen = pygame.display.set_mode((640, 480))
    Menu(screen)
main()
