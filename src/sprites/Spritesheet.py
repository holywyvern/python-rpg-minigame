from typing import Any
import pygame

from .Sprite import Sprite

class Spritesheet(Sprite):
  def __init__(self, image: pygame.Surface, cols: int, rows: int):
    super().__init__()
    self.__spritesheet = image
    self.__images = []
    w = image.get_width() / cols
    h = image.get_height() / rows
    self.rect = pygame.Rect(0, 0, w, h)
    for y in range(0, rows):
      for x in range(0, cols):
        self.__images.append(
          self.__image_at(x, y)
        )
    self.image = self.__images[0]
    self.__frame = 0

  def __image_at(self, x: int, y: int):
    image = pygame.Surface(self.rect.size).convert_alpha()
    image.fill((0, 0, 0, 0))
    rect = pygame.Rect(
      x * self.rect.width, y * self.rect.height, self.rect.width, self.rect.height
    )
    image.blit(self.__spritesheet, (0, 0), rect)
    return image

  @property
  def frame(self):
    return self.__frame
  
  @frame.setter
  def frame(self, value):
    self.__frame = min(len(self.__images) - 1, max(0, value))

  def update(self, *args: Any, **kwargs: Any):
    self.update_image()

  def update_image(self):
    self.image = self.__images[self.__frame]