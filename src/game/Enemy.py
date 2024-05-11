from copy import copy
from random import randint

from .Battler import Battler

class Enemy(Battler):
  def __init__(self):
    super().__init__()
    self.shiny = False
    self.level = 1
    self.__race_id = 0

  @property
  def name(self):
    return self.race.name

  @property
  def race(self):
    from ..managers import Database
    return Database.enemies[self.__race_id]

  @property
  def gold(self):
    from ..managers import Game
    growth =  self.level * self.race.gold_growth
    value = self.race.base_gold + growth + randint(0, growth) + Game.player.location_changes * randint(1, growth)
    if self.shiny:
      value *= 5
    return value

  @property
  def experience(self):
    from ..managers import Game
    growth =  self.level * self.race.exp_growth
    value = self.race.base_exp + growth + randint(0, growth) + Game.player.location_changes * (3 + randint(0, growth))
    if self.shiny:
      value *= 5
    return value

  def battler_name(self):
    if self.shiny:
      return f"assets/enemies/{self.race.sprite_name}-shiny.png"
    return f"assets/enemies/{self.race.sprite_name}.png"

  def sprite_cols(self):
    return self.race.sprite_cols

  def sprite_rows(self):
    return self.race.sprite_rows

  def motions(self):
    return self.race.motions

  def find_skill_ids(self):
    return self.race.skill_ids

  def setup(self, race_id: int, level: int):
    self.__race_id = race_id
    self.__stats = copy(self.race.bases)
    self.level = level
    self.shiny = randint(0, 100) == 69
    for i in range(1, level):
      self.__level_up()
    self.full_heal()
    if self.shiny:
      self.animation_id = 9

  def stat(self, index):
    return self.__stats[index]

  def __level_up(self):
    for i in range(0, 7):
      self.__stats[i] += self.race.growth[i] * randint(1, 1 + self.level // 3)

