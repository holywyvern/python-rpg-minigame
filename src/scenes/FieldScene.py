from random import randint
from .Scene import Scene

from .BattleScene import BattleScene

from ..sprites import CommandWindow, BackgroundSprite, CharacterHUD, CharacterBag, BattlerSprite, AnimationPlayer, TextSprite

class FieldScene(Scene):
  def start(self):
    self.play_field_music()
    self.create_background()
    self.create_commands()
    self.__create_hero_sprite()
    self.__create_hud()

  def play_field_music(self):
    from ..managers import Game, Music
    Music.play(Game.player.location.music_name)

  def create_background(self):
    from ..managers import Game
    self.background = BackgroundSprite(Game.player.location.background_name)
    self.add(self.background)

  def create_commands(self):
    from ..managers import Game
    self.commands = CommandWindow(
      ["Battle Monster", "Check Stats", "Train Stat", "Rest", "Change Map", "Quit Game"], title = "What should I do?"
    )
    self.commands.move(20, 64)
    self.commands.enable()
    self.commands.select(Game.player.last_field_command)
    self.commands.bind("Battle Monster", self.__on_battle_command)
    self.commands.bind("Check Stats", self.__on_check_command)
    self.commands.bind("Train Stat", self.__on_train_command)
    self.commands.bind("Rest", self.__on_rest_command)
    self.commands.bind("Change Map", self.__on_change_command)
    self.commands.bind("Quit Game", self.__on_quit_command)
    self.commands.update()
    self.add(self.commands)

  def __create_hud(self):
    self.hud = CharacterHUD()
    self.add(self.hud)
    self.bag = CharacterBag()
    self.add(self.bag)

  def __on_battle_command(self):
    from ..managers import Game, Scenes
    Game.player.last_field_command = 0
    monster_id = randint(0, len(Game.player.location.enemy_ids) - 1)
    monster_id = Game.player.location.enemy_ids[monster_id]
    Scenes.goto(BattleScene(monster_id))

  def __on_check_command(self):
    from .StatsScene import StatsScene
    from ..managers import Game, Scenes
    Game.player.last_field_command = 1
    Scenes.goto(StatsScene())

  def __on_train_command(self):
    from ..managers import Game, Scenes
    from .TrainScene import TrainScene
    Game.player.last_field_command = 2
    Scenes.goto(TrainScene())

  def __on_rest_command(self):
    from .RestScene import RestScene
    from ..managers import Game, Scenes
    Game.player.last_field_command = 3
    Scenes.goto(RestScene())

  def __on_change_command(self):
    from ..managers import Game, Scenes
    Game.player.last_field_command = 0
    next_location = self.__find_next_location()
    Game.player.change_location(next_location)
    Scenes.goto(FieldScene())

  def __find_next_location(self):
    from ..managers import Game, Database
    next_id = randint(1, len(Database.locations) - 1)
    if next_id == Game.player.location.id:
      return self.__find_next_location()
    return next_id

  def __on_quit_command(self):
    exit(0)

  def __create_hero_sprite(self):
    from ..managers import Game
    popup = TextSprite("", Game.big_font)
    self.hero = BattlerSprite(Game.player, popup)
    animation = AnimationPlayer(self.hero)
    self.hero.active = True
    self.hero.move(512 - self.hero.width / 2, 320 - self.hero.height)
    self.add(self.hero)
    self.add(animation)
    self.add(popup)