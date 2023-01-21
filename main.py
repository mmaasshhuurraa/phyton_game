import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT
import random

WIDTH, HEIGHT = 800, 600
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
class Ball(pygame.Surface):
  def __init__(self, rect: pygame.Rect):
    super().__init__(rect.size)
    self.fill(RED)
    self.rect = rect
    self.speed = [random.randint(2, 5), 0]

  def move(self, speed: list):
    self.rect = self.rect.move(speed)

class HeroBall(Ball):
  def __init__(self, rect: pygame.Rect):
    super().__init__(rect)
    self.fill(WHITE)
    self.speed = [5, 5]

  def handlePressedKeys(self, pressed_keys):
    if pressed_keys[K_DOWN] and self.rect.bottom < HEIGHT:
      self.move((0, self.speed[1]))

    if pressed_keys[K_UP] and self.rect.top > 0:
      self.move((0, -self.speed[1]))

    if pressed_keys[K_RIGHT] and self.rect.right < WIDTH:
      self.move((self.speed[0], 0))

    if pressed_keys[K_LEFT] and self.rect.left > 0:
      self.move((-self.speed[0], 0))

class MyGame:
  def __init__(self):
    pygame.init()

    self.surface = pygame.display.set_mode((WIDTH, HEIGHT))

    self.CREATE_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(self.CREATE_ENEMY, 1500)

    self.FPS = pygame.time.Clock()

    self.hero = HeroBall(pygame.Rect(100, HEIGHT / 2, 20, 20))
    self.enemies = []

  def loop(self):
    is_working = True

    while is_working:
        self.FPS.tick(60)

        for e in pygame.event.get():
          if QUIT == e.type:
            is_working = False
          elif self.CREATE_ENEMY == e.type:
            self.enemies.append(
              Ball(pygame.Rect(
                WIDTH, random.randint(0, HEIGHT - 20), 20, 20)))

        self.hero.handlePressedKeys(
          pygame.key.get_pressed())
        
        self.surface.fill(BLACK)
        self.surface.blit(self.hero, self.hero.rect)

        for enemy in self.enemies:
          enemy.move((-enemy.speed[0], 0))
          self.surface.blit(enemy, enemy.rect)

          if enemy.rect.left < -20:
            self.enemies.pop(self.enemies.index(enemy))
          
          if self.hero.rect.colliderect(enemy.rect):
            self.enemies.pop(self.enemies.index(enemy))

        pygame.display.flip()

game = MyGame()
game.loop()
