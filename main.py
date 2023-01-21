import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT
import random

WIDTH, HEIGHT = 800, 600
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
class Ball:
  def __init__(self, rect: pygame.Rect):
    self.surface = pygame.Surface(rect.size)
    self.rect = rect
    self.speed = [1, 1]

  def move(self, speed: list):
    self.rect = self.rect.move(speed)

  def draw(self, canvas:pygame.Surface):
    canvas.blit(self.surface, self.rect)
class EnemyBall(Ball):
  def __init__(self, rect: pygame.Rect):
    super().__init__(rect)
    self.surface.fill(RED)
    self.speed = [random.randint(2, 5), 0]

class BonusBall(Ball):
  def __init__(self, rect: pygame.Rect):
    super().__init__(rect)
    self.surface.fill(GREEN)
    self.speed = [0, random.randint(2, 5)]

class HeroBall(Ball):
  def __init__(self, rect: pygame.Rect):
    super().__init__(rect)
    self.surface.fill(WHITE)
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
  def __init__(self, width, height):
    pygame.init()
    
    self.game_over = False

    self.width = width
    self.height = height

    self.surface = pygame.display.set_mode((width, height))

    self.CREATE_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(self.CREATE_ENEMY, 1500)
    self.CREATE_BONUS = pygame.USEREVENT + 2
    pygame.time.set_timer(self.CREATE_BONUS, 3000)

    self.FPS = pygame.time.Clock()

    self.hero = HeroBall(pygame.Rect(100, height / 2, 20, 20))
    self.enemies = []
    self.bonuses = []

  def stepEnemies(self):
    for enemy in self.enemies:
      enemy.move((-enemy.speed[0], 0))
      enemy.draw(self.surface)
        
      if enemy.rect.left < -20:
        self.enemies.pop(self.enemies.index(enemy))
        
      if self.hero.rect.colliderect(enemy.rect):
        self.game_over = True

  def stepBonuses(self):
    for bonus in self.bonuses:
      bonus.move((0, bonus.speed[1]))
      bonus.draw(self.surface)
        
      if bonus.rect.top > self.height:
        self.bonuses.pop(self.bonuses.index(bonus))
        
      if self.hero.rect.colliderect(bonus.rect):
        self.bonuses.pop(self.bonuses.index(bonus))

  def loop(self):
    while not self.game_over:
        self.FPS.tick(60)

        for e in pygame.event.get():
          if QUIT == e.type:
            is_working = False
          elif self.CREATE_ENEMY == e.type:
            self.enemies.append(
              EnemyBall(pygame.Rect(
                self.width, 
                random.randint(0, self.height - 20), 
                20, 20)))
          elif self.CREATE_BONUS == e.type:
            self.bonuses.append(
              BonusBall(pygame.Rect(
                random.randint(0, self.width / 2), 
                -20, 20, 20)))

        self.hero.handlePressedKeys(
          pygame.key.get_pressed())
        
        self.surface.fill(BLACK)
        self.hero.draw(self.surface)
        
        self.stepEnemies()
        self.stepBonuses()

        pygame.display.flip()

game = MyGame(WIDTH, HEIGHT)
game.loop()
