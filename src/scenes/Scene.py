import pygame

class Scene(pygame.sprite.Group):
  def __init__(self):
    super().__init__()
    self.__iterating = False
    self.__children = set()
  
  def add(self, *items):
    for item in items:
      self.__children.add(item)
    super().add(*items)

  def remove(self, *items):
    for item in items:
      if item in self.__children:
        self.__children.remove(item)
    super().remove(*items)

  def update(self):
    for child in list(self.__children):
      child.update()

  def start(self): pass

  def end(self): pass

  

