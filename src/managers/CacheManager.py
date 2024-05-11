import pygame

class CacheManager:
  def __init__(self):
    self.__images: dict[str, pygame.Surface] = {}
    self.__sfx: dict[str, pygame.mixer.Sound] = {}
    self.__icons: dict[str, pygame.Surface] = {}

  def image(self, filename: str):
    if filename not in self.__images:
      self.__images[filename] = pygame.image.load(filename).convert_alpha()
    return self.__images[filename]
  
  def sfx(self, filename: str):
    if filename not in self.__sfx:
      self.__sfx[filename] = pygame.mixer.Sound(filename)
      self.__sfx[filename].set_volume(0.5)
    return self.__sfx[filename]
  
  def icon(self, index: int):
    if index not in self.__icons:
      iconset = self.image("assets/system/icon.png")
      w = iconset.get_width() / 10
      x = index % 10
      y = index // 10
      image = pygame.Surface((w, w)).convert_alpha()
      image.fill((0, 0, 0, 0))
      image.blit(iconset, (0, 0), (x * w, y * w, w, w))
      self.__icons[index] = image
    return self.__icons[index]
  
Cache = CacheManager()