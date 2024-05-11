import pygame

class ScreenClass:
  def __init__(self):
    self.__fade_time = 0
    self.__fade_count = 0

  def setup(self):
    self.__display = pygame.display.set_mode((640, 480))
    self.__surface = pygame.Surface((640, 480)).convert_alpha()

  @property
  def display(self):
    return self.__display
  
  @property
  def width(self):
    return self.__display.get_width()
  
  @property
  def height(self):
    return self.__display.get_height()

  @property
  def is_fading(self):
    return self.__fade_count > 0

  def fill(self, color):
    self.__display.fill(color)

  def update(self):
    self.__update_fade()
    pygame.display.flip()
    pass

  def __update_fade(self):
    from .GameManager import Game
    self.__display.blit(self.__surface, (0, 0))
    if self.__fade_count > 0:
      self.__fade_count -= Game.delta_time
      if self.__fade_count < 0: self.__fade_count = 0
      ratio = self.__fade_count / self.__fade_time
      self.__surface.set_alpha(ratio * self.__target_alpha + (1 - ratio) * (255 - self.__target_alpha))

  def fadeout(self, time: float = 0.5):
    self.__fade_time = time
    self.__fade_count = time
    self.__target_alpha = 255

  def fadein(self, time: float = 0.5):
    self.__fade_time = time
    self.__fade_count = time
    self.__target_alpha = 0

Screen = ScreenClass()