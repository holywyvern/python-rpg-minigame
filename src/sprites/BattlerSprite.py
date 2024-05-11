from typing import Any
import pygame

from .Spritesheet import Spritesheet
from .TextSprite import TextSprite
from ..managers import Game

from ..game import Battler

class BattlerSprite(Spritesheet):
  def __init__(self, battler: Battler, popup: TextSprite):
    from ..managers import Cache
    self.__motion_name = "idle"
    self.battler = battler
    self.battler.motion_index = 0
    self.battler.motion_delay = 0
    self.popup = popup
    self.animation = None
    img = Cache.image(battler.battler_name())
    super().__init__(img, battler.sprite_cols(), battler.sprite_rows())

  @property
  def motion_name(self):
    return self.__motion_name
  
  @motion_name.setter
  def motion_name(self, value: str):
    if self.__motion_name == value:
      return
    self.__motion_name = value
    self.battler.motion_index = 0
    self.battler.motion_delay = 0

  @property
  def motion(self):
    return self.battler.motions()[self.motion_name]

  def update(self, *args: Any, **kwargs: Any):
    self.update_collapse()
    self.update_popup()
    self.update_motion()
    self.update_frame()
    super().update()

  def update_collapse(self):
    from ..managers import Game
    if self.battler.hp <= 0 and self.alpha > 0:
      self.alpha = max(0, self.alpha - Game.delta_time * 255)

  def update_popup(self):
    if self.battler.popup_value != 0:
      self.popup.text = str(abs(self.battler.popup_value))
      self.popup.color = (255, 255, 255, 255) if self.battler.popup_value > 0 else (0, 255, 128, 255)
      self.battler.popup_value = 0
    if self.battler.popup_time > 0:
      self.battler.popup_time -= Game.delta_time
      if self.battler.popup_time <= 0:
        self.battler.popup_time = 0
        self.popup.text = ""
    self.popup.alpha = self.battler.popup_time * 255 / 2
    self.popup.move(self.x + self.width / 2 - self.popup.width / 2, self.y + self.battler.popup_time * 32)
  
  def update_motion(self):
    self.motion_name = self.battler.motion_name
    self.battler.motion_delay += Game.delta_time
    while self.battler.motion_delay > 0.1:
      self.battler.motion_delay -= 0.1
      self.battler.motion_index = self.battler.motion_index + 1
      self.battler.motion_count += 1
      total = len(self.motion)
      if self.battler.motion_index >= total and self.battler.motion_loops > 0:
        self.battler.motion_loops -= 1
        if self.battler.motion_loops == 0:
          self.battler.start_motion("idle", loops = -1)
          self.motion_name = "idle"
          return
      self.battler.motion_index %= total
  
  def update_frame(self):
    if self.battler.motion_index >= len(self.motion):
      return
    self.frame = self.motion[self.battler.motion_index]