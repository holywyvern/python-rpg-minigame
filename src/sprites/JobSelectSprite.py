from typing import Any
import pygame

from .Spritesheet import Spritesheet
from ..managers import Game
from .. import rpg

class JobSelectSprite(Spritesheet):
  def __init__(self, job: rpg.Job):
    from ..managers import Cache
    self.motion_name = "idle"
    self.motion_index = 0
    self.motion_delay = 0
    self.active = False
    self.job = job
    img = Cache.image(f"assets/actors/{job.sprite_name}/character.png")
    super().__init__(img, job.sprite_cols, job.sprite_rows)

  @property
  def motion(self):
    return self.job.motions[self.motion_name]

  def update(self, *args: Any, **kwargs: Any):
    if self.active:
      self.update_animation()
    else:
      self.update_deactive_animation()
    self.update_frame()
    super().update()
  
  def update_animation(self):
    self.alpha = 255
    self.motion_delay += Game.delta_time
    while self.motion_delay > 0.2:
      self.motion_delay -= 0.2
      self.motion_index = (self.motion_index + 1) % len(self.motion)
    
  def update_deactive_animation(self):
    self.alpha = 128
    self.motion_index = 0
    self.motion_delay = 0
  
  def update_frame(self):
    self.frame = self.motion[self.motion_index]