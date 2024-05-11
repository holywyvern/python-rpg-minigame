from dataclasses import dataclass

@dataclass
class Location:
  id: int
  name: str
  background_name: str
  enemy_ids: list[int] 
  music_name: str = "field"
