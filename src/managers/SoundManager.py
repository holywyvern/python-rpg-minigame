import pygame

from .CacheManager import Cache

class SoundManager:
  def play(self, name):
    pygame.mixer.Sound.play(Cache.sfx(f"assets/sound/{name}.ogg"))

Sound = SoundManager()
