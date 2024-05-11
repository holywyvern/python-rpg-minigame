import pygame
from random import randint

from ..game import Battler

from .Sprite import Sprite

class AnimationPlayer(Sprite):
  def __init__(self, battler_sprite: Sprite):
    super().__init__()
    self.__empty = pygame.Surface((1, 1)).convert_alpha()
    self.__empty.fill((0, 0, 0, 0))
    self.image = self.__empty
    self.__animation = None
    self.battler_sprite = battler_sprite
    self.__offset = (0, 0)
    battler_sprite.animation = self
  
  @property
  def is_running(self):
    return self.__animation != None

  @property
  def battler(self) -> Battler:
    return self.battler_sprite.battler

  def update(self):
    self.__update_animation_id()
    self.__update_animation_frame()
    self.__update_position()
    return super().update()
  
  def __update_animation_id(self):
    if self.battler.animation_id != 0:
      self.__setup_animation(self.battler.animation_id)
      self.battler.animation_id = 0
  
  def __setup_animation(self, id: int):
    from ..managers import Database, Cache, Sound
    self.__animation = Database.animations[id]
    img = Cache.image(f"assets/fx/{self.__animation.image_name}.png")
    self.__animation_images = self.__generate_images(img, self.__animation.frame_count)
    self.battler.animation_frame = 0
    self.battler.animation_frame_count = self.__animation.frame_count
    self.battler.animation_delay = 0
    self.__offset = (0, 0)
    Sound.play(self.__animation.sfx_name)

  def __generate_images(self, img: pygame.Surface, frame_count: int):
    result: list[pygame.Surface] = []
    for i in range(0, frame_count):
      w = img.get_width() / frame_count
      rect = pygame.Rect(i * w, 0, w, img.get_height())
      frame = pygame.Surface((w, img.get_height())).convert_alpha()
      frame.fill((0, 0, 0, 0))
      frame.blit(img, (0, 0), rect)
      result.append(frame)
    return result

  def __update_animation_frame(self):
    from ..managers import Game, Sound
    if not self.__animation:
      return
    self.battler.animation_delay += Game.delta_time
    while self.battler.animation_delay > 0.1:
      self.battler.animation_delay -= 0.1
      self.battler.animation_frame += 1
    if self.battler.animation_frame >= self.battler.animation_frame_count:
      if self.battler.animation_loops > 0:
        self.battler.animation_loops -= 1
        self.battler.animation_frame = 0
        self.__offset = (randint(-4, 4), randint(-4, 4))
        Sound.play(self.__animation.sfx_name)
      else:
        self.__animation = None
        self.image = self.__empty
        return
    self.image = self.__animation_images[self.battler.animation_frame]
  
  def __update_position(self):
    x = self.battler_sprite.x + (self.battler_sprite.width - self.width) / 2 + self.__offset[0] * 8
    y = self.battler_sprite.y + self.battler_sprite.height - self.height + self.__offset[1] * 8
    self.move(x, y)