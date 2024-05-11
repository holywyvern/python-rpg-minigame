

from ..scenes import Scene
from .ScreenManager import Screen

class SceneManager:
  def __init__(self):
    self.__scene: Scene = None

  def test_battle(self):
    return False

  def test_monster_id(self):
    return 7
  
  def test_job_id(self):
    return 3

  def setup(self):
    from ..scenes import ControlsScene, BattleScene
    if self.test_battle():
      self.__setup_battle_test()
      self.goto(BattleScene(self.test_monster_id(), test = True))
    else:
      self.goto(ControlsScene())

  def __setup_battle_test(self):
    from ..managers import Game
    from ..game import Player
    Game.player = Player()
    Game.player.setup(self.test_job_id())
    for x in range(0, 100):
      for stat in range(0, 7):
        Game.player.train(stat)
    Game.player.full_heal()

  def goto(self, scene: Scene):
    if self.__scene:
      self.__fadein()
      self.__scene.end()
    self.__scene = scene
    if self.__scene != None:
      self.__scene.start()
      self.__fadeout()

  def __fadein(self):
    Screen.fadein()
    self.__wait_for_fade()

  def __fadeout(self):
    Screen.fadeout()
    self.__wait_for_fade()

  def __wait_for_fade(self):
    from .GameManager import Game
    while Screen.is_fading:
      Game.update()

  def update(self):
    if not Screen.is_fading and self.__scene:
      self.__scene.update()

  def draw(self):
    if self.__scene and Screen.display:
      self.__scene.draw(Screen.display)

Scenes = SceneManager()