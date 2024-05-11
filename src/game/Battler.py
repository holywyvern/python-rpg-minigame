from random import randint

class Battler:
  def __init__(self):
    self.__hp = 0
    self.__mp = 0
    self.motion_name = "idle"
    self.motion_loops = -1
    self.motion_index = 0
    self.motion_delay = 0  
    self.motion_count = 0  
    self.popup_value = 0
    self.popup_time = 0
    self.animation_id = 0
    self.animation_frame = 0
    self.animation_frame_count = 0
    self.animation_delay = 0
    self.animation_loops = 0

  def start_motion(self, name: str, loops: int = -1):
    self.motion_name = name
    self.motion_loops = loops
    self.motion_count = 0

  def popup(self, value: int):
    self.popup_value = value
    self.popup_time = 2

  @property
  def is_dead(self):
    return self.hp <= 0

  @property
  def stats(self):
    return list(map(self.stat, range(0, 7)))

  @property
  def is_in_animation(self):
    if self.motion_name != "idle" and self.motion_loops > 0:
      return True
    if self.animation_frame < self.animation_frame_count:
      return True
    return self.popup_time > 0

  @property
  def hp(self): return self.__hp

  @hp.setter
  def hp(self, value: int):
    self.__hp = int(min(self.max_hp, max(0, value)))

  @property
  def mp(self): return self.__mp

  @mp.setter
  def mp(self, value: int):
    self.__mp = int(min(self.max_mp, max(0, value)))

  @property
  def max_hp(self): return self.stat(0)

  @property
  def max_mp(self): return self.stat(1)

  @property
  def attack(self): return self.stat(2)

  @property
  def defense(self): return self.stat(3)

  @property
  def intelligence(self): return self.stat(4)

  @property
  def spirit(self): return self.stat(5)

  @property
  def agility(self): return self.stat(6)

  @property
  def speed(self): return randint(0, self.agility) + self.agility // 2

  @property
  def hp_ratio(self): return self.hp / self.max_hp

  @property
  def mp_ratio(self):
    if self.max_mp < 1:
      return 0
    return self.mp / self.max_mp

  def battler_name(self):
      return ""

  def sprite_cols(self):
    return 1

  def sprite_rows(self):
    return 1

  def motions(self) -> dict[str, list[int]]:
    return []

  def stat(self, index: int):
    return 0

  def actions(self, target: 'Battler'):
    from .Action import Action
    return list(map(lambda i: Action(self, target, i), self.find_skill_ids()))
  
  def find_skill_ids(self) -> list[int]:
    return []
  
  def full_heal(self):
    self.heal_hp()
    self.heal_mp()

  def heal_hp(self):
    self.hp = self.max_hp
  
  def heal_mp(self):
    self.mp = self.max_mp

