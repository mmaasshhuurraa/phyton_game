import pygame
from pygame.constants import QUIT
import random
#import time

BALLS_NUM = 20
BALL_SIZE_MAX = 200
WIDTH, HEIGHT = 800, 600

class RandomBall(pygame.Surface):
  def __init__(self, rect):
    super().__init__(rect)
    self.fill(self.randomColor())
    self.rect = self.get_rect()
    self.rect.x = random.randint(0,WIDTH-self.rect.width)
    self.rect.y = random.randint(0,HEIGHT-self.rect.height)
    self.speed = [
      random.choice([-2, -1, 1, 2]),
      random.choice([-2, -1, 1, 2])]

  def randomColor(self):
    return (
      random.randint(1, 255), 
      random.randint(1, 255), 
      random.randint(1, 255))
  
  def move(self, speed: list):
    self.rect = self.rect.move(speed)
  
  def reflectFromScreenBorders(self, width, heigth):
    if self.rect.bottom >= heigth or self.rect.top <= 0:
      self.speed[1]=-self.speed[1]
      self.fill(self.randomColor())

    if self.rect.right >= width or self.rect.left <= 0:
      self.speed[0]=-self.speed[0]
      self.fill(self.randomColor())

pygame.init()

surface = pygame.display.set_mode((WIDTH, HEIGHT))

balls = []
for i in range(0, BALLS_NUM):
  balls.append(
    RandomBall((
      random.randint(1, BALL_SIZE_MAX),
      random.randint(1, BALL_SIZE_MAX))))

is_working = True
while is_working:
    for e in pygame.event.get():
      if QUIT == e.type:
        is_working = False

    surface.fill((0,0,0))

    for ball in balls:
      ball.move(ball.speed)
      ball.reflectFromScreenBorders(WIDTH, HEIGHT)
      surface.blit(ball, ball.rect)

    pygame.display.flip()
    #time.sleep(0.1)

pygame.quit()
