import pygame
from .Sprite import Sprite

class BackgroundSprite(pygame.sprite.Group):
  def __init__(self, name: str):
    from ..managers import Cache
    bg = Sprite()
    bg.image = Cache.image(f"assets/backgrounds/{name}.png")
    fg = Sprite()
    fg.image = Cache.image("assets/system/strip.png")
    super().__init__(bg, fg)