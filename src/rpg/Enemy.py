from dataclasses import dataclass

@dataclass
class Enemy:
  id: int
  name: str
  base_exp: int
  exp_growth: int
  base_gold: int
  gold_growth: int
  sprite_name: str
  sprite_rows: int
  sprite_cols: int
  bases: list[int]
  growth: list[int]
  motions: dict[str, list[int]]
  skill_ids: list[int]
  battle_name: str = "battle"