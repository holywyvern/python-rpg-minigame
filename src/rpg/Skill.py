from dataclasses import dataclass

@dataclass
class Skill:
  id: int
  name: str
  icon_index: int
  motion: str
  animation_id: int
  animation_wait: int
  type: str
  mp_cost: int
  formula: str
  variance: int
  animation_loops: int = 0

  def eval(self, user, target):
    try:
      return max(1, int(eval(self.formula)))
    except Exception as e:
      return 1
