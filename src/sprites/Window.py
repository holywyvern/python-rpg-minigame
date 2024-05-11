from typing import Any
import pygame

from .Sprite import Sprite
from .TextSprite import TextSprite

class Window(pygame.sprite.Group):
  def __init__(self, rect: pygame.Rect = None, title: str = ""):
    from ..managers import Game
    self.__bg = Sprite()
    self.__bg.rect = rect
    self.image = pygame.Surface((1, 1)).convert_alpha()
    self.image.fill((0, 0, 0, 0))
    self.__title = TextSprite(title, Game.small_font)
    self.__draw_background()
    super().__init__(self.__bg, self.__title)
    self.move(self.x, self.y)

  @property
  def x(self):
    return self.rect.x
  
  @property
  def y(self):
    return self.rect.y

  @property
  def font(self):
    return self.__title.font

  @property
  def title(self):
    return self.__title.text

  @title.setter
  def title(self, value: str):
    self.__title.text = value
    self.__draw_background()

  @property
  def rect(self):
    return self.__bg.rect
  
  @rect.setter
  def rect(self, value):
    self.__bg.rect = value
    self.__draw_background()

  def __draw_background(self):
    img = pygame.Surface(self.rect.size).convert_alpha()
    img.fill("black")
    pygame.draw.rect(img, "white", ( 4, 10, self.rect.w - 8, self.rect.h - 14), 4)
    pygame.draw.rect(img, "black", ((self.rect.width - self.__title.width - 16) / 2, 0, self.__title.width + 8, 16))
    self.__bg.image = img

  def move(self, x: int, y: int):
    self.rect.x = x
    self.rect.y = y
    self.__title.move(x + (self.rect.width - self.__title.width - 16) / 2 + 2, y)

  

