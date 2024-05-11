from typing import Any
import pygame

from .Sprite import Sprite

class Bar(Sprite):
  def __init__(self, size, color):
    super().__init__()
    self.color = color
    self.ratio = 1
    self.image = pygame.Surface(size).convert_alpha()
    self.rect = pygame.Rect(0, 0, size[0], size[1])
  
  def update(self, *args: Any, **kwargs: Any):
    self.image.fill((0, 0, 0, 0))
    self.image.fill(self.color, (0, 0, self.ratio * self.rect.w, self.rect.h))
    return super().update(*args, **kwargs)