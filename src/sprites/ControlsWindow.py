from pygame import Rect
from .Window import Window

class ControlsWindow(Window):
  def __init__(self):
    from ..sprites import TextSprite
    from ..managers import Screen, Game
    super().__init__(Rect(0, 0, Screen.width, Screen.height), "Game Info")
    text = TextSprite("Game Controls", Game.big_font)
    texts = [
      ["Game Controls", Game.big_font],
      ["   Spacebar: Accept.", Game.small_font],
      ["   Arrow Keys: Move.", Game.small_font],
      ["   This game also accepts a gamepad.", Game.small_font],
      ["", Game.small_font],
      ["Game Tips", Game.big_font],
      ["   - Defeat higher level enemies", Game.small_font],
      ["     to earn more points.", Game.small_font],
      ["   - Changing locations raises enemy level.", Game.small_font],
      ["   - Training is important to keep with", Game.small_font],
      ["     enemy level up stats.", Game.small_font],
      ["", Game.small_font],
      ["", Game.small_font],
      ["Enjoy this minigame!", Game.big_font],
      ["Share your highest score!", Game.big_font],
    ]
    y = 24
    for text in texts:
      sprite = TextSprite(text[0], text[1])
      sprite.move(16, y)
      self.add(sprite)
      y += sprite.height
    sprite = TextSprite("- Press spacebar to continue -", text[1])
    sprite.move((Screen.width - sprite.width) / 2, Screen.height - sprite.height - 16)
    self.add(sprite)
    y += sprite.height