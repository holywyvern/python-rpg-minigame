from typing import Any
import pygame

from .TextSprite import TextSprite

from .Colors import Colors

class CharacterBag(pygame.sprite.Group):
  def __init__(self):
    from ..managers import Game
    self.rect = pygame.rect.Rect((32, 375, 0, 0))
    self.player = Game.player    
    self.lvl = TextSprite("Level", Game.small_font)
    self.lvl.color = Colors.SYSTEM
    self.lvl_value = TextSprite(f"{self.player.level:3d}", Game.small_font)
    self.gold = TextSprite("G", Game.small_font)
    self.gold.color = self.lvl.color
    self.gold_value = TextSprite(f"{self.player.gold}", Game.small_font)
    self.update()
    super().__init__(
      self.lvl, self.lvl_value,
      self.gold, self.gold_value
    )


  def update(self, *args: Any, **kwargs: Any):
    from ..managers import Screen
    x = self.rect.x
    y = self.rect.y
    self.lvl_value.text = f"{self.player.level:3d}"
    self.lvl_value.move(Screen.width - self.lvl_value.width - 16, y)
    self.lvl.move(Screen.width - self.lvl.width - 32 - self.lvl_value.width, y)
    self.gold.move(Screen.width - self.gold.width - 16, y + 20)
    self.gold_value.text = f"{self.player.gold}"
    self.gold_value.move(Screen.width - self.gold_value.width - self.gold.width - 20, y + 20)