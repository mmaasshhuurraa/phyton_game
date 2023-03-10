from typing import Tuple
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT
import random
from os import listdir

WIDTH, HEIGHT = 1800, 1000
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)

class Ball:
  def __init__(self):
    self.rect = pygame.Rect(0, 0, 10, 10)
    self.speed = [1, 1]

  def move(self, speed: list):
    self.rect = self.rect.move(speed)

class EnemyBall(Ball):
  def __init__(self):
    super().__init__()

    if not hasattr(EnemyBall, 'surface'):
      self.surface = pygame.image.load('images/enemy.png').convert_alpha()
    
    self.rect = pygame.Rect(0, 0, *self.surface.get_size())
    self.speed = [random.randint(2, 5), 0]
  
  def draw(self, canvas: pygame.Surface):
    canvas.blit(self.surface, self.rect)

class BonusBall(Ball):
  def __init__(self):
    super().__init__()

    if not hasattr(BonusBall, 'surface'):
      self.surface = pygame.image.load('images/bonus.png').convert_alpha()
      
    self.rect = pygame.Rect(0, 0, *self.surface.get_size())
    self.speed = [0, random.randint(2, 5)]
  
  def draw(self, canvas: pygame.Surface):
    canvas.blit(self.surface, self.rect)

class HeroBall(Ball):
  def __init__(self, pos: Tuple[int, int]):
    super().__init__()

    GOOSE_ANIM_PATH = 'images/goose'
    self.surfaces = [pygame.image.load(
      GOOSE_ANIM_PATH + '/' + file).convert_alpha() 
        for file in listdir(GOOSE_ANIM_PATH)]

    self.anim_index = 0
    self.surface = self.surfaces[self.anim_index]
    self.rect = pygame.Rect(pos[0], pos[1], *self.surface.get_size())
    self.speed = [5, 5]

  def doAnim(self):
    self.anim_index += 1
    self.anim_index %= len(self.surfaces)
    self.surface = self.surfaces[self.anim_index]

  def draw(self, canvas: pygame.Surface):
    canvas.blit(self.surface, self.rect)

  def handlePressedKeys(self, pressed_keys, width, height):
    if pressed_keys[K_DOWN] and self.rect.bottom < height:
      self.move((0, self.speed[1]))

    if pressed_keys[K_UP] and self.rect.top > 0:
      self.move((0, -self.speed[1]))

    if pressed_keys[K_RIGHT] and self.rect.right < width:
      self.move((self.speed[0], 0))

    if pressed_keys[K_LEFT] and self.rect.left > 0:
      self.move((-self.speed[0], 0))

class BackGround:
  def __init__(self, width, height):
    self.surface = pygame.transform.scale(
      pygame.image.load('images/background.png').convert(),
      (width, height))

    self.rect1 = pygame.Rect(0, 0, width, height)
    self.rect2 = pygame.Rect(width, 0, width, height)
    self.speed = 3

  def frame(self):
    self.rect1 = self.rect1.move((-self.speed, 0))
    self.rect2 = self.rect2.move((-self.speed, 0))

    if self.rect1.right < 0:
      self.rect1.left = self.rect1.width

    if self.rect2.right < 0:
      self.rect2.left = self.rect2.width

  def draw(self, canvas: pygame.Surface):
    canvas.blit(self.surface, self.rect1)
    canvas.blit(self.surface, self.rect2)

class TextField:
  def __init__(self, fontName, fontSize, rect, color, text):
    self.scoreFont = pygame.font.SysFont(fontName, fontSize)
    self.rect = rect
    self.color = color
    self.text = text

  def setText(self, text):
    self.text = text

  def draw(self, canvas: pygame.Surface):
    canvas.blit(
      self.scoreFont.render(self.text, True, self.color), 
      self.rect )

class MyGame:
  def __init__(self, width, height):
    pygame.init()
    
    self.is_game_over = False

    self.width = width
    self.height = height

    self.surface = pygame.display.set_mode((width, height))

    self.CREATE_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(self.CREATE_ENEMY, 1500)
    self.CREATE_BONUS = pygame.USEREVENT + 2
    pygame.time.set_timer(self.CREATE_BONUS, 3000)
    self.DO_ANIM = pygame.USEREVENT + 3
    pygame.time.set_timer(self.DO_ANIM, 125)

    self.FPS = pygame.time.Clock()

    self.background = BackGround(width, height)

    self.hero = HeroBall((100, height / 2))
    
    self.enemies = []
    self.bonuses = []

    self.scores = 0
    self.scoresTextField = TextField(
      'Verdana', 20, 
      pygame.Rect(self.width - 120, 10, 120, 20), 
      BLACK, f'scores: {self.scores}')

  def frame(self):
    self.background.frame()

    for enemy in self.enemies:
      enemy.move((-enemy.speed[0], 0))

      if enemy.rect.right < 0:
        self.enemies.pop(self.enemies.index(enemy))
        continue;

      if self.hero.rect.colliderect(enemy.rect):
        self.is_game_over = True
        break
        
    for bonus in self.bonuses:
      bonus.move((0, bonus.speed[1]))

      if self.hero.rect.colliderect(bonus.rect):
        self.bonuses.pop(self.bonuses.index(bonus))
        self.scores += 1
        self.scoresTextField.setText(f'scores: {self.scores}')
        continue

      if bonus.rect.top > self.height:
        self.bonuses.pop(self.bonuses.index(bonus))
        
  def draw(self):
    self.background.draw(self.surface)
    self.hero.draw(self.surface)

    for enemy in self.enemies:
      enemy.draw(self.surface)

    for bonus in self.bonuses:
      bonus.draw(self.surface)
    
    self.scoresTextField.draw(self.surface)

  def createEmemyHandler(self):
      enemy = EnemyBall()
      enemy.rect.move_ip(
        self.width, 
        random.randint(0, self.height - enemy.rect.height))
      self.enemies.append(enemy)

  def createBonusHandler(self):
      bonus = BonusBall()
      bonus.rect.move_ip(
        random.randint(0, self.width / 2), 
        -bonus.rect.height)
      self.bonuses.append(bonus)

  def doAnimHandler(self):
      self.hero.doAnim()

  def loop(self):
    while not self.is_game_over:
        self.FPS.tick(60)

        for e in pygame.event.get():
          if QUIT == e.type:
            self.is_game_over = True
            
          elif self.CREATE_ENEMY == e.type:
            self.createEmemyHandler()

          elif self.CREATE_BONUS == e.type:
            self.createBonusHandler()

          elif self.DO_ANIM == e.type:
            self.doAnimHandler()

        self.hero.handlePressedKeys(
          pygame.key.get_pressed(), 
          self.width, self.height)
                
        self.frame()
        self.draw()

        pygame.display.flip()

game = MyGame(WIDTH, HEIGHT)
game.loop()
