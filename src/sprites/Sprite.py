import pygame


class Sprite(pygame.sprite.Sprite):
  def __init__(self) -> None:
    super().__init__()
    self.__alpha = 255
    self.__image: pygame.Surface = None
    self.rect = pygame.rect.Rect(0, 0, 0, 0)
  
  @property
  def image(self):
    return self.__image
  
  @image.setter
  def image(self, value: pygame.Surface):
    self.__image = value
    if value:
      value.set_alpha(self.__alpha)

  @property
  def alpha(self):
    return self.__alpha

  @alpha.setter
  def alpha(self, value):
    self.__alpha = value
    if self.image:
      self.image.set_alpha(value)

  @property
  def x(self):
    return self.rect.x
  
  @x.setter
  def x(self, value: float):
    self.rect.x = value

  @property
  def y(self):
    return self.rect.y
  
  @y.setter
  def y(self, value: float):
    self.rect.y = value

  @property
  def width(self):
    if not self.image:
      return 0
    return self.image.get_width()
  
  @property
  def height(self):
    if not self.image:
      return 0
    return self.image.get_height()
  
  def move(self, x: float, y: float):
    self.rect.x = x
    self.rect.y = y
