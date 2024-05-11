import pygame


class MusicManager:
  def __init__(self):
    self.__last_music = ""

  def play(self, name: str):
    if self.__last_music == name:
      return
    self.__last_music = name
    pygame.mixer.music.load(f"assets/music/{name}.ogg")
    pygame.mixer.music.play(-1)

  def play_once(self, name: str):
    if self.__last_music == name:
      return
    self.__last_music = name
    pygame.mixer.music.load(f"assets/music/{name}.ogg")
    pygame.mixer.music.play(0)

Music = MusicManager()