from .FieldScene import FieldScene

from ..sprites import BackgroundSprite, CommandWindow, TextSprite, Colors

class RestScene(FieldScene):
  def play_field_music(self):
    from ..managers import Music
    Music.play("rest")

  def create_background(self):
    from ..managers import Game
    self.background = BackgroundSprite(f"{Game.player.location.background_name}-night")
    self.add(self.background)

  def hp_cost(self):
    from ..managers import Game
    return Game.player.level * 5

  def mp_cost(self):
    from ..managers import Game
    return Game.player.level * 8

  def create_commands(self):
    from ..managers import Game
    hp = f"Recover HP - {self.hp_cost()}  "
    mp = f"Recover MP - {self.mp_cost()}  "
    self.commands = CommandWindow(
      [hp, mp, "Back to field"], title = "Should I rest?"
    )
    self.commands.move(20, 64)
    self.commands.enable()
    self.commands.select(0)
    if self.hp_cost() > Game.player.gold:
      self.commands.disable_command(0)
    if self.mp_cost() > Game.player.gold:
      self.commands.disable_command(1)
    self.commands.bind(hp, self.__on_hp_heal_command)
    self.commands.bind(mp, self.__on_mp_heal_command)
    self.commands.bind("Back to field", self.__on_back_command)
    self.commands.update()
    self.add(self.commands)
    g1 = TextSprite("G", Game.small_font)
    g1.color = Colors.SYSTEM
    self.add(g1)
    g1.move(self.commands.x + self.commands.rect.w - 36, self.commands.y + 20)
    g2 = TextSprite("G", Game.small_font)
    g2.color = Colors.SYSTEM
    g2.move(g1.x, g1.y + 20)
    self.add(g2)
    self.g1 = g1
    self.g2 = g2

  def update(self):
    from ..managers import Game
    if self.hp_cost() > Game.player.gold:
      self.commands.disable_command(0)
    if self.mp_cost() > Game.player.gold:
      self.commands.disable_command(1)    
    return super().update()

  def __on_hp_heal_command(self):
    from ..managers import Game
    Game.player.heal_hp()
    Game.player.animation_id = 2
    Game.player.gold -= self.hp_cost()

  def __on_mp_heal_command(self):
    from ..managers import Game
    Game.player.heal_mp()
    Game.player.animation_id = 2
    Game.player.gold -= self.mp_cost()

  def __on_back_command(self):
    from ..managers import Scenes
    from .FieldScene import FieldScene
    Scenes.goto(FieldScene())
