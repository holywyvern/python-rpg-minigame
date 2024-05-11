from .Battler import Battler

class Action:
  def __init__(self, user: Battler, target: Battler, skill_id: int):
    self.user = user
    self.target = target
    self.__skill_id = skill_id

  @property
  def skill(self):
    from ..managers import Database
    return Database.skills[self.__skill_id]

  @property
  def enabled(self):
    return self.user.mp >= self.skill.mp_cost
  
  def perform(self):
    skill = self.skill
    self.user.mp -= self.skill.mp_cost
    if skill.type == 'heal':
      return self.__perform_heal()
    if skill.type == 'damage':
      return self.__perform_damage()
    return self.__perform_escape()

  def __perform_heal(self):
    skill = self.skill
    recover = skill.eval(self.user, self.user)
    self.user.hp += recover
    return -recover

  def __perform_damage(self):
    skill = self.skill
    damage = skill.eval(self.user, self.target)
    self.target.hp -= damage
    return damage

  def __perform_escape(self):
    from ..managers import Scenes, Game
    from ..scenes import FieldScene
    Game.player.score -= 1000
    if Game.player.score < 0:
      Game.player.score = 0
    Scenes.goto(FieldScene())
    return 0
