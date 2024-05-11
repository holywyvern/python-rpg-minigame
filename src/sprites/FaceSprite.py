import pygame

from .Sprite import Sprite

from .. import rpg

class FaceSprite(Sprite):
  def __init__(self):
    super().__init__()
    self.__job: rpg.Job = None
  
  @property
  def job(self):
    return self.__job
  
  @job.setter
  def job(self, value: rpg.Job):
    if self.__job != value:
      self.__job = value
      if value:
        from ..managers import Cache
        self.image = Cache.image(f"assets/actors/{value.sprite_name}/faceset.png")