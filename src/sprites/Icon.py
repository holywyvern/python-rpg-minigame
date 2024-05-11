from .Sprite import Sprite

class Icon(Sprite):
  def __init__(self, index):
    super().__init__()
    self.index = index
  

  @property
  def index(self):
    return self.__index
  
  @index.setter
  def index(self, value: int):
    from ..managers import Cache
    self.__index = value
    self.image = Cache.icon(value).copy()
