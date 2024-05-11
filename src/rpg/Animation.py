from dataclasses import dataclass

@dataclass
class Animation:
  id: int
  name: str
  frame_count: int
  image_name: str
  sfx_name: str