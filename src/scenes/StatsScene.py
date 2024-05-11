import pygame

from .Scene import Scene
from .FieldScene import FieldScene

from ..sprites import Sprite, TextSprite, Colors

class StatsScene(FieldScene):
  STAT_NAMES = [
    "Max HP",
    "Max MP",
    "Attack",
    "Defense",
    "Intelligence",
    "Spirit",
    "Agility"
  ]

  def create_commands(self): pass

  def start(self):
    super().start()
    from ..managers import Game
    cover = Sprite()
    cover.image = pygame.Surface((400, 320)).convert_alpha()
    cover.move(0, 48)
    self.add(cover)
    player = Game.player
    exp = TextSprite("Experience", Game.small_font)
    exp.color = Colors.SYSTEM
    y = 64
    exp.move(16, y + 16)
    self.add(exp)
    next = TextSprite("To next level:", Game.small_font)
    next.color = Colors.SYSTEM
    next.move(16, y + 36)
    self.add(next)    
    exp_value = TextSprite(f"{player.experience:10d}", Game.small_font)
    exp_value.move(24 + next.width, y + 16)
    self.add(exp_value)
    next_value = TextSprite(f"{player.experience_to_level:10d}", Game.small_font)
    next_value.move(24 + next.width, y + 36)
    self.add(next_value)
    for stat in range(0, 7):
      label = TextSprite(StatsScene.STAT_NAMES[stat], Game.small_font)
      label.color = Colors.SYSTEM
      label.move(24, y + 86 + 20 * stat)
      self.add(label)
      stat_value = TextSprite(f"{player.stat(stat):10d}", Game.small_font)
      stat_value.move(exp_value.x, y + 86 + 20 * stat)
      self.add(stat_value)
    victories = TextSprite("Victories:", Game.small_font)
    victories.color = Colors.SYSTEM
    victories.move(24,  y + 86 + 20 * 8)
    self.add(victories)
    victory_count = TextSprite(f"{player.victories:14d}", Game.small_font)
    victory_count.move(victories.x + victories.width, victories.y)
    self.add(victory_count)
    score = TextSprite("Score:", Game.small_font)
    score.color = Colors.SYSTEM
    score.move(24,  y + 86 + 20 * 9)
    self.add(score)
    score_count = TextSprite(f"{player.score // 10:14,d}", Game.small_font)
    score_count.move(victories.x + victories.width, score.y)
    self.add(score_count)

  def update(self):
    from ..managers import Input, Sound, Scenes
    from .FieldScene import FieldScene
    super().update()
    if Input.is_triggered("accept"):
      Sound.play("cancel")
      Scenes.goto(FieldScene())

 