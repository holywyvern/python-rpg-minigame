from pygame import Rect

from .Window import Window
from .Colors import Colors

from .TextSprite import TextSprite

class VictoryWindow(Window):
  def __init__(self, exp: int, gold: int):
    from ..managers import Game, Screen
    w = 64 * 4
    h = 24 * 3 + 16 
    super().__init__(Rect((Screen.width - w) / 2, (Screen.height - h) / 2, w, h), "Victory spoils!")
    exp_label = TextSprite("Experience", Game.small_font)
    exp_label.color = Colors.SYSTEM 
    self.add(exp_label)
    exp_value = TextSprite(str(exp), Game.small_font)
    self.add(exp_value)
    gold_label = TextSprite("G", Game.small_font)
    gold_label.color = Colors.SYSTEM
    self.add(gold_label)
    gold_value = TextSprite(str(gold), Game.small_font)
    self.add(gold_value)
    exp_label.move(self.x + 16, self.y + 24)
    exp_value.move(self.x + w - 16 - exp_value.width, exp_label.y)
    gold_label.move(self.x + w - 16 - gold_label.width, exp_label.y + 24)
    gold_value.move(gold_label.x - gold_value.width - 4, gold_label.y)
