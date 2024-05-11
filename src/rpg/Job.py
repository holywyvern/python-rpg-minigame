from dataclasses import dataclass

@dataclass
class Job:
  id: int
  name: str
  description: list[str]
  sprite_name: str
  sprite_rows: int
  sprite_cols: int
  bases: list[int]
  growth: list[int]
  motions: dict[str, list[int]]
  skill_ids: list[int]
