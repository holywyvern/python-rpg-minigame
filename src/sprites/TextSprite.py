import pygame

from .Sprite import Sprite
from .Font import Font

class TextSprite(Sprite):
  def __init__(self, text: str, font: Font):
    super().__init__()
    self.__text = text
    self.__font = font
    self.__color = (255, 255, 255, 255)
    self.__refresh_image()
  
  @property
  def text(self):
    return self.__text
  
  @text.setter
  def text(self, value):
    if self.__text == value:
      return
    self.__text = value
    self.__refresh_image()

  @property
  def font(self):
    return self.__font

  @property
  def color(self):
    return self.__color
  
  @color.setter
  def color(self, value):
    self.__color = value
    self.__refresh_image()

  @font.setter
  def font(self, value):
    self.__font = value
    self.__refresh_image()

  def __refresh_image(self):
    self.rect = pygame.rect.Rect(
      self.rect.x,
      self.rect.y,
      self.__font.measure_text(self.__text),
      self.__font.size
    )
    self.image = pygame.Surface((self.rect.w, self.rect.h)).convert_alpha()
    self.image.fill((0, 0, 0, 0))
    images = self.__font.get_text(self.__text)
    for i in range(0, len(images)):
      x = i * self.__font.size - (i - 1) * self.__font.kerning
      self.image.blit(images[i], (x, 0))
    color_img = pygame.Surface(self.image.get_size()).convert_alpha()
    color_img.fill(self.__color)
    self.image.blit(color_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

