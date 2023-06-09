import pygame
from pygame.locals import *
import math
P = 30
pp = 30
class CarSprite(pygame.sprite.Sprite):
    def __init__(self, car_image, x, y, rotations=360):
        pygame.sprite.Sprite.__init__(self)
        self.rot_img = []
        self.min_angle = (360 / rotations)
        for i in range(rotations):
            rotated_image = pygame.transform.rotozoom(car_image, 360 - 90 - (i * self.min_angle), 1)
            self.rot_img.append(rotated_image)
        self.min_angle = math.radians(self.min_angle)
        self.image = self.rot_img[0]
        self.rect = pygame.rect.Rect(self.image.get_rect())
        self.rect.center = (x, y)
        self.heading = 0
        self.reversing = False
        self.speed = 0
        self.velocity = pygame.math.Vector2(0, 0)
        self.position = pygame.math.Vector2(x, y)
    def accelerate(self, amount):
        if not self.reversing:
            self.speed += amount
        else:
            self.speed -= amount
    def brake(self):
        self.speed /= 2
        if abs(self.speed) < 0.1:
            self.speed = 0
    def reverse(self):
        self.speed = 0
        self.reversing = not self.reversing
    def turn(self, angle_degrees):
        self.heading += math.radians(angle_degrees)
        image_index = int(self.heading / self.min_angle) % len(self.rot_img)
        if self.image != self.rot_img[image_index]:
            x, y = self.rect.center
            self.image = self.rot_img[image_index]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
    def update(self):
        self.velocity.from_polar((self.speed, math.degrees(self.heading)))
        self.position+=self.velocity
        self.rect.center = (round(self.position[0]),round(self.position[1]))
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 900
pygame.init()
C = 0
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),pygame.RESIZABLE)
cactus_cordinate =(WINDOW_WIDTH , WINDOW_HEIGHT - 10)
pygame.display.set_caption('avto')
clock = pygame.time.Clock()
running = True
road_image = pygame.image.load('road_texture.png')
background = pygame.transform.smoothscale(road_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
car_image = pygame.image.load('car_128.png').convert_alpha()
black_car = CarSprite(car_image, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
car_sprites = pygame.sprite.Group()
car_sprites.add(black_car)
pygame.mixer.music.load("Dschinghis_Khan_-_Moskau_48138405.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)
r = pygame.mixer.Sound('long_crash_type_tire_skid.mp3')
rr = pygame.mixer.Sound('car-turn-signals_m1s1lseo.mp3')
rrrr = pygame.mixer.Sound('sports-car-muffler_z1mdjme_.mp3')
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == VIDEORESIZE:
            WINDOW_WIDTH = event.w
            WINDOW_HEIGHT = event.h
            screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
            background = pygame.transform.smoothscale(road_image,(WINDOW_WIDTH,WINDOW_HEIGHT))
        elif event.type == KEYUP:
            if event.key == K_b:
                print('beep-beep')
            elif event.key == K_r:
                print('aaaaaaa')
                black_car.reverse()
            elif event.key == K_UP:
                print('gus')
                rrrr.play()
                black_car.accelerate(0.5)
            elif event.key == K_DOWN:
                print("fffff")
                black_car.brake()
                r.play()
             elif event.type == KEYUP and event.key == K_ESCAPE:
                road_image = pygame.image.load('ASF.jpg')
                background = pygame.transform.smoothscale(road_image, (WINDOW_WIDTH, WINDOW_HEIGHT)) 



    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        black_car.turn(-1.8)
        rr.play()
    if keys[K_RIGHT]:
        black_car.turn(1.8)
        rr.play()
    if keys[K_LEFT] or keys[K_RIGHT] and keys[K_UP]:
        rr.play()
        rrrr.play()

    car_sprites.update()
    screen.blit(background, (0, 0))
    car_sprites.draw(screen)
    filter = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    filter.fill(pygame.color.Color('Gray'))
    screen.blit(filter, (0, 0), special_flags=pygame.BLEND_RGB_SUB)
    pygame.display.flip()
    clock.tick_busy_loop(60)
pygame.quit()
