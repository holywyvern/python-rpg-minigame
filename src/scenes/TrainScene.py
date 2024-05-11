from .FieldScene import FieldScene

from ..sprites import BackgroundSprite, CommandWindow, TextSprite, Colors

class TrainScene(FieldScene):
  def play_field_music(self):
    from ..managers import Music
    Music.play("shop")

  def create_commands(self):
    from ..managers import Game
    spacing = " " * 6
    command_list = [
      f"Train Max HP       - {spacing} - {spacing}   ",
      f"Train Max MP       - {spacing} - {spacing}   ",
      f"Train Attack       - {spacing} - {spacing}   ",
      f"Train Defense      - {spacing} - {spacing}   ",
      f"Train Intelligence - {spacing} - {spacing}   ",
      f"Train Spirit       - {spacing} - {spacing}   ",
      f"Train Agility      - {spacing} - {spacing}   ",
    ]
    command_list.append("Back to field")
    self.commands = CommandWindow(
      command_list, title = "Pick your training"
    )
    self.commands.move(20, 64)
    self.commands.enable()
    self.commands.bind(command_list[0], lambda: self.__on_command_train(0))
    self.commands.bind(command_list[1], lambda: self.__on_command_train(1))
    self.commands.bind(command_list[2], lambda: self.__on_command_train(2))
    self.commands.bind(command_list[3], lambda: self.__on_command_train(3))
    self.commands.bind(command_list[4], lambda: self.__on_command_train(4))
    self.commands.bind(command_list[5], lambda: self.__on_command_train(5))
    self.commands.bind(command_list[6], lambda: self.__on_command_train(6))
    self.commands.bind("Back to field", self.__on_back_to_field_command)
    self.commands.update()
    self.__values: list[TextSprite] = []
    self.__stats: list[TextSprite] = []
    self.add(self.commands)
    for i in range(0, 7):
      spr = TextSprite(f"{Game.player.train_cost(i):8d}", Game.small_font)
      spr.color = Colors.DEFAULT if Game.player.can_train(i) else Colors.DISABLED
      spr.move(self.commands.x + self.commands.rect.w - spr.width - 36, self.commands.y + (i + 1) * 20)
      self.__values.append(spr)
      self.add(spr)
      stat = TextSprite(f"{Game.player.stat(i):6d}", Game.small_font)
      stat.move(spr.x - 20 - stat.width, spr.y)
      self.__stats.append(stat)
      self.add(stat)
      g = TextSprite("G", Game.small_font)
      g.color = Colors.SYSTEM
      g.move(spr.x + spr.width, spr.y)
      self.add(g)

  def __on_command_train(self, stat: int):
    from ..managers import Game
    Game.player.gold -= Game.player.train_cost(stat)
    Game.player.train(stat)

  def __on_back_to_field_command(self):
    from ..managers import Scenes
    from .FieldScene import FieldScene
    Scenes.goto(FieldScene())

  def update(self):
    from ..managers import Game
    for i in range(0, 7):
      self.__values[i].text = f"{Game.player.train_cost(i):8d}"
      self.__stats[i].text = f"{Game.player.stat(i):6d}"
      if Game.player.can_train(i):
        self.commands.enable_command(i)
        self.__values[i].color = Colors.DEFAULT
      else:
        self.commands.disable_command(i)
        self.__values[i].color = Colors.DISABLED
      self.__stats[i].color = self.__values[i].color

    return super().update()
