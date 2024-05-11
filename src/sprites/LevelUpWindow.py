from pygame import Rect
from .Window import Window

from .TextSprite import TextSprite
from .Colors import Colors

class LevelUpWindow(Window):
  def __init__(self, old_level: int, old_stats: list[int]):
    from ..managers import Screen, Game
    player = Game.player
    font = Game.small_font
    size = font.measure_text("intelligence")
    w = 32 + size + font.measure_text(">>") + 24 + font.measure_text("000000") * 2
    h = 16 + 24 * 9
    labels = [
      "Max HP",
      "Map MP",
      "Attack",
      "Defense",
      "Intelligence",
      "Spirit",
      "Agility"
    ]
   
    super().__init__(Rect((Screen.width - w) / 2, (Screen.height - h) / 2, w, h), "Level up!")
    x = self.x + 16
    y = self.y + 24
    label = TextSprite("Level", font)
    label.color = Colors.SYSTEM
    label.move(x, y)
    self.add(label)
    level = TextSprite(f"{player.level:3d}", font)
    level.move(x + label.width + 8, y)
    self.add(level)
    for i in range(0, 7):
      x = self.x + 16
      y = self.y + (i + 2) * 24
      label = TextSprite(labels[i], font)
      label.move(x, y)
      label.color = Colors.SYSTEM
      self.add(label)
      old = TextSprite(f"{old_stats[i]:6d}", font)
      old.move(x + size + 8, y)
      self.add(old)
      arrow = TextSprite(">>", font)
      arrow.color = Colors.SYSTEM
      arrow.move(old.x + old.width + 8, y)
      self.add(arrow)
      current = TextSprite(f"{player.stat(i):6d}", font)
      current.move(arrow.x + arrow.width + 8, y)
      self.add(current)


