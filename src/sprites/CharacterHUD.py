from typing import Any
import pygame

from .Sprite import Sprite
from .FaceSprite import FaceSprite
from .TextSprite import TextSprite
from .Bar import Bar

from .Colors import Colors

class CharacterHUD(pygame.sprite.Group):
  def __init__(self):
    from ..managers import Game, Cache
    self.rect = pygame.rect.Rect((32, 375, 0, 0))
    self.player = Game.player
    self.face = FaceSprite()
    self.name = TextSprite(self.player.name, Game.big_font)
    self.hp_text = TextSprite("HP", Game.small_font)
    self.mp_text = TextSprite("MP", Game.small_font)
    self.hp_value = TextSprite(f"{Game.player.hp:6d}", Game.small_font)
    self.hp_value.color = self.hp_color()
    self.mp_value = TextSprite(f"{Game.player.mp:6d}", Game.small_font)
    self.mp_value.color = Colors.MP_COLOR
    self.hp_bar_bg = Sprite()
    self.hp_bar_bg.image = Cache.image("assets/system/bar.png")
    self.mp_bar_bg = Sprite()
    self.mp_bar_bg.image = self.hp_bar_bg.image
    self.hp_bar = Bar((98, 7), self.hp_value.color)
    self.mp_bar = Bar((98, 7), self.mp_value.color)
    self.update()
    super().__init__(
      self.face, self.name, 
      self.hp_text, self.mp_text, self.hp_value, self.mp_value,
      self.hp_bar_bg, self.mp_bar_bg,
      self.hp_bar, self.mp_bar,
    )
  
  def hp_color(self):
    if self.player.hp / self.player.max_hp < 0.3:
      return Colors.CRISIS_COLOR
    return Colors.HP_COLOR

  def update(self, *args: Any, **kwargs: Any):
    from ..managers import Screen
    x = self.rect.x
    y = self.rect.y
    self.face.job = self.player.job
    self.face.move(x, y)
    self.name.move(x + 96, y)
    self.hp_text.move(x + 100, y + 20)
    self.hp_value.move(x + 116, y + 20)
    self.hp_value.text = f"{self.player.hp:6d}"
    self.mp_text.move(x + 100, y + 60)
    self.mp_value.move(x + 116, y + 60)
    self.mp_value.text = f"{self.player.mp:6d}"
    self.hp_bar_bg.move(x + 98, y + 38)
    self.mp_bar_bg.move(x + 98, y + 78)
    self.hp_bar.ratio = self.player.hp / self.player.max_hp
    self.hp_bar.move(x + 104, y + 38)
    self.mp_bar.ratio = self.player.mp / self.player.max_mp
    self.mp_bar.move(x + 104, y + 78)
    self.hp_value.color = self.hp_color()
    self.hp_bar.color = self.hp_value.color
    self.hp_bar.ratio = self.player.hp_ratio
    self.mp_bar.ratio = self.player.mp_ratio
    self.hp_bar.update()
    self.mp_bar.update()
