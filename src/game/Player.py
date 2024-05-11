from copy import copy
from random import randint

from .Battler import Battler
from .Enemy import Enemy

class Player(Battler):
  MAX_GOLD = 9_999_999
  MAX_LEVEL = 999

  def __init__(self):
    super().__init__()
    self.last_field_command = 0
    self.__level = 1
    self.__gold = 0
    self.__experience = 0
    self.__job_id = 0
    self.__location_id = 0
    self.location_changes = 0
    self.victories = 0
    self.score = 0
    self.__trainings = [0] * 7
    self.__stats = [0] * 7

  @property
  def gold(self):
    return self.__gold
  
  @gold.setter
  def gold(self, value):
    self.__gold = int(max(0, min(Player.MAX_GOLD, value)))

  @property
  def name(self):
    return self.job.name

  @property
  def job(self):
    from ..managers import Database
    return Database.jobs[self.__job_id]

  @property
  def location(self):
    from ..managers import Database
    return Database.locations[self.__location_id]

  @property
  def experience_to_level(self):
    if self.level >= Player.MAX_LEVEL:
      return 0
    return self.experience_for_level(self.level + 1) - self.experience

  @property
  def level(self):
    return self.__level
  
  @property
  def experience(self):
    return self.__experience
  
  @property
  def skills(self):
    from ..managers import Database
    return list(map(lambda i: Database.skills[i], self.find_skill_ids()))

  def battler_name(self):
    return f"assets/actors/{self.job.sprite_name}/character.png"

  def sprite_cols(self):
    return self.job.sprite_cols

  def sprite_rows(self):
    return self.job.sprite_rows

  def motions(self):
    return self.job.motions

  def find_skill_ids(self):
    return self.job.skill_ids

  def gain_experience(self, exp: int):
    self.__experience += exp
    self.score += 100 * exp
    while self.__experience >= self.experience_for_level(self.level + 1):
      self.level_up()

  def experience_for_level(self, level: int):
    return level * 10 + (level * level - 1) * 5 + max(0, level - 2) * level * 5

  def setup(self, job_id: int):
    self.__level = 0
    self.__experience = 0
    self.__job_id = job_id
    self.__location_id = 1
    self.gold = 100
    self.__stats = copy(self.job.bases)
    self.level_up()
  
  def level_up(self):
    if self.__level > 0:
      self.score += 1_000
    if self.level >= Player.MAX_LEVEL:
      return
    self.__level += 1
    for i in range(0, 7):
      self.__train(i)
    self.full_heal()

  def train_cost(self, stat: int):
    return 2 + self.__trainings[stat] * 3

  def can_train(self, stat: int):
    if self.stat(stat) >= self.__max_stat(stat):
      return False
    return self.gold >= self.train_cost(stat)

  def train(self, stat: int):
    self.__trainings[stat] += 1
    self.__train(stat)

  def __train(self, stat: int):
    growth = self.job.growth[stat]
    self.__stats[stat] += growth + randint(0, 1 + growth // 2 + self.level // 5)

  def stat(self, index: int):
    return min(self.__max_stat(index), self.__stats[index])
  
  def __max_stat(self, index: int):
    if index < 2:
      return 999_999
    return 9_999
  
  def change_location(self, location_id: int):
    self.__location_id = location_id
    self.location_changes += 1
