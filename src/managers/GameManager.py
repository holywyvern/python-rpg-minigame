import pygame
import asyncio

from .CacheManager import Cache

class GameClass:

  def play(self):
    from ..game import Player
    self.player: Player = None
    from .DataManager import Database
    Database.load_database()
    self.__setup()

  def __setup(self):
    from .ScreenManager import Screen
    from .EventManager import Events
    from .InputManager import Input
    from .SceneManager import Scenes
    Input.setup()
    self.delta_time = 0
    self.small_font = self.__load_font(16, 2)
    self.big_font = self.__load_font(20, 6)
    self.__clock = pygame.time.Clock()
    Events.on(pygame.QUIT, self.__close_window)    
    Scenes.setup()    

  def __load_font(self, size: int, kerning: int):
    from ..sprites import Font
    image = Cache.image(f"assets/fonts/{size}.png")
    return Font(image, size, kerning)

  def __close_window(self, event):
    pygame.quit()

  async def loop(self):
    while True:
      self.update()
      await asyncio.sleep(0)  # This line is critical; ensure you keep the sleep time at 0

  def update(self):
    from .ScreenManager import Screen
    from .EventManager import Events
    from .SceneManager import Scenes
    from .InputManager import Input
    Events.update()
    Screen.fill("black")

    Scenes.update()
    Scenes.draw()

    Screen.update()
    Input.update()
    self.delta_time = self.__clock.tick(60) / 1000
  
Game = GameClass()
