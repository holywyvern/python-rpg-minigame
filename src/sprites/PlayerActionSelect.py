import pygame

from .Sprite import Sprite
from .Icon import Icon
from .TextSprite import TextSprite

class PlayerActionSelect(pygame.sprite.Group):
  def __init__(self):
    from ..managers import Game, Cache
    self.accept = lambda x: None
    self.player = Game.player
    self.__index = 0
    self.__active = False
    self.arrow_down = Sprite()
    self.arrow_down.image = Cache.image("assets/system/arrow-down.png")
    self.arrow_up = Sprite()
    self.arrow_up.image = Cache.image("assets/system/arrow-up.png")
    self.__actions: list[Icon] = []
    for skill in self.player.skills:
      icon = Icon(skill.icon_index)
      self.__actions.append(icon)
    self.text1 = TextSprite("Your turn", Game.small_font)
    self.action_name = TextSprite("", Game.small_font)
    super().__init__(
      self.arrow_down, self.arrow_up, *self.__actions,
      self.text1, self.action_name
    )
    self.rect = pygame.Rect(64 * 4, 32 * 12, 0, 0)
    self.update()

  @property
  def active(self):
    return self.__active
  
  @active.setter
  def active(self, value: bool):
    self.__active = value
    skills = self.player.skills
    for i in range(0, len(skills)):
      skill = skills[i]
      icon = self.__actions[i]
      if self.player.mp < skill.mp_cost:
        icon.alpha = 128
      else:
        icon.alpha = 255

  def update(self, *args, **kwargs):
    super().update(*args, **kwargs)
    if self.active:
      self.__update_cursor()
    self.__update_positions()

  def __update_cursor(self):
    from ..managers import Input, Sound
    if Input.is_reppeated("left"):
      Sound.play("cursor")
      self.__index -= 1
    elif Input.is_reppeated("right"):
      Sound.play("cursor")
      self.__index += 1
    elif Input.is_triggered("accept"):
      skill = self.player.skills[self.__index]
      if self.player.mp < skill.mp_cost:
        Sound.play("buzzer")
      else:
        self.active = False
        Sound.play("accept")
        self.accept(skill)
    if self.__index < 0:
      self.__index = len(self.__actions) - 1
    if self.__index >= len(self.__actions):
      self.__index = 0

  def __update_positions(self):
    if self.active:
      self.text1.text = "Your Turn"
    else:
      self.text1.text = "Enemy Turn"
    self.text1.move(self.rect.x, self.rect.y)
    for i in range(0, len(self.__actions)):
      action = self.__actions[i]
      action.move(
        self.rect.x + i * (4 + action.width), self.rect.y + 12 + 24
      )
    action = self.__actions[0]
    x = self.rect.x + self.__index * (4 + action.width) + action.width / 2 - self.arrow_down.width / 2
    self.arrow_down.move(x, self.rect.y + 24)
    self.arrow_up.move(x, self.rect.y + action.height + 16 + 24)
    self.action_name.text = self.player.skills[self.__index].name
    self.action_name.move(self.rect.x + len(self.__actions) * (4 + action.width) + 8, self.rect.y + action.height / 2 + 24)
