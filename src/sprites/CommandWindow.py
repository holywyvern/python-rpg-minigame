from copy import copy
from typing import Any
import pygame

from .Window import Window
from .TextSprite import TextSprite
from .Sprite import Sprite
from .Colors import Colors

class CommandWindow(Window):
  def __init__(self, commands: list[str], title: str = ""):
    from ..managers import Cache, Game
    self.__handles = {}
    w = max(0, Game.small_font.measure_text(title), *map(Game.small_font.measure_text, commands)) + 40
    h = 16 * (len(commands) + 2) + len(commands) * 4 
    self.active = False
    self.__index = -1
    self.__commands: list[TextSprite] = []
    self.__cursor = Sprite()
    self.__texts = copy(commands)
    self.__enabled = [True] * len(commands)
    super().__init__(pygame.Rect(0, 0, w, h), title)
    for text in commands:
      command = TextSprite(f" {text}", self.font)
      self.add(command)
      self.__commands.append(command)    
    self.__cursor.image = Cache.image("assets/system/arrow-right.png").copy()
    self.move(self.x, self.y)
    self.add(self.__cursor)
    self.update()

  def enable_command(self, index: int):
    self.__enabled[index] = True
  
  def disable_command(self, index: int):
    self.__enabled[index] = False

  def enable(self):
    self.__index = 0
    self.active = True

  def update(self, *args: Any, **kwargs: Any):
    self.__update_selection()
    self.__update_cursor()
    self.__update_commands()
    super().update(*args, **kwargs)

  def __update_selection(self):
    if not self.active:
      return
    from ..managers import Input
    if Input.is_reppeated("down"):
      self.__select(self.__index + 1)
    elif Input.is_reppeated("up"):
      self.__select(self.__index - 1)
    elif Input.is_triggered("accept"):
      if self.__enabled[self.__index]:
        self.__accept()
      else:
        self.__buzzer()

  def select(self, index: int):
    self.__index = index
    size = len(self.__commands)
    while self.__index < 0:
      self.__index += size
    while self.__index >= size:
      self.__index -= size

  def __select(self, index: int):
    from ..managers import Sound
    Sound.play("cursor")
    self.select(index)

  def __buzzer(self):
    from ..managers import Sound
    Sound.play("buzzer")

  def bind(self, command: str, handle):
    self.__handles[command] = handle

  def __accept(self):
    from ..managers import Sound
    Sound.play("accept")
    command = self.__texts[self.__index]
    if command in self.__handles:
      self.__handles[command]()


  def __update_cursor(self):
    if self.__cursor.image:
      if self.__index >= 0:
        self.__cursor.image.set_alpha(255)
      else:
        self.__cursor.image.set_alpha(0)
    self.__cursor.move(self.rect.x + 18, self.rect.y + 2 + 20 * (self.__index + 1))

  def move(self, x: int, y: int):
    super().move(x, y)
    for i in range(0, len(self.__commands)):
      command = self.__commands[i]
      command.move(x + 16, y + 20 * (i + 1))
    self.__update_cursor()

  def __update_commands(self):
    for i in range(0, len(self.__commands)):
      command = self.__commands[i]
      command.color = Colors.DEFAULT if self.__enabled[i] else Colors.DISABLED