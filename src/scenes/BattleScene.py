from random import randint

from .Scene import Scene

from ..game import Enemy, Action

from ..sprites import BackgroundSprite, CharacterHUD, BattlerSprite, TextSprite, Colors, PlayerActionSelect, Bar, Sprite, AnimationPlayer

class BattleScene(Scene):
  def __init__(self, monster_id: int, test: bool = False):
    from ..managers import Game
    super().__init__()
    self.player = Game.player
    self.enemy = Enemy()
    self.enemy.setup(monster_id, self.player.level + randint(self.player.location_changes, self.player.location_changes * 2))
    if test:
      self.enemy.hp //= 8
    self.__update_phase = lambda: None

  def start(self):
    self.__play_battle_music()
    self.__create_background()
    self.__create_hero_sprite()
    self.__create_enemy_sprite()
    self.__create_hud()
    self.__create_vs_text()
    self.__roll_initiative()

  def __play_battle_music(self):
    from ..managers import Music
    Music.play(self.enemy.race.battle_name)

  def __create_background(self):
    from ..managers import Game
    self.background = BackgroundSprite(Game.player.location.background_name)
    self.add(self.background)

  def __create_hero_sprite(self):
    from ..managers import Game
    popup = TextSprite("", Game.big_font)
    self.hero_sprite = BattlerSprite(self.player, popup)
    self.hero_sprite.move(512 - self.hero_sprite.width / 2, 320 - self.hero_sprite.height)
    animations = AnimationPlayer(self.hero_sprite)
    self.add(self.hero_sprite)
    self.add(animations)
    self.add(popup)

  def __create_enemy_sprite(self):
    from ..managers import Game
    popup = TextSprite("", Game.big_font)
    self.enemy_sprite = BattlerSprite(self.enemy, popup)
    animations = AnimationPlayer(self.enemy_sprite)
    self.enemy_sprite.move(120 - self.enemy_sprite.width / 2, 320 - self.enemy_sprite.height)
    self.add(self.enemy_sprite)
    self.add(animations)
    self.add(popup)

  def __create_hud(self):
    self.hud = CharacterHUD()
    self.add(self.hud)
    self.select = PlayerActionSelect()
    self.select.accept = self.__use_player_skill
    self.add(self.select)

  def __create_vs_text(self):
    from ..managers import Game, Screen, Cache
    font = Game.big_font
    vs = TextSprite("Vs", font)
    vs.color = Colors.SYSTEM
    self.add(vs)
    name = TextSprite(self.enemy.name, font)
    self.add(name)
    lvl = TextSprite("Lv", font)
    lvl.color = Colors.SYSTEM
    self.add(lvl)
    value = TextSprite(f"{self.enemy.level:3d}", font)
    self.add(value)
    bg = Sprite()
    bg.image = Cache.image("assets/system/bar.png")
    self.add(bg)
    self.enemy_bar = Bar((98, 7), Colors.HP_COLOR)
    self.add(self.enemy_bar)
    w = vs.width + name.width + lvl.width + value.width + bg.width + 64
    vs.move((Screen.width - w) / 2, 16)
    name.move(vs.x + vs.width + 8, 16)
    lvl.move(name.x + name.width + 16, 16)
    bg.move(name.x + name.width + value.width + lvl.width + 24, 20)
    self.enemy_bar.move(bg.x + 6, bg.y)
    value.move(lvl.x + lvl.width + 8, 16)

  def update(self):
    self.__update_phase()
    self.enemy_bar.ratio = self.enemy.hp_ratio
    return super().update()

  def __roll_initiative(self):
    if self.enemy.speed > self.player.speed:
      self.__start_enemy_turn()
    else:
      self.__start_player_turn()

  def __start_enemy_turn(self):
    actions = self.enemy.actions(self.player)
    i = 0
    # Only use other actions but the first on low HP
    if self.enemy.hp_ratio < 0.5:
      i = randint(0, len(actions) - 1)
    self.__execute_action(actions[i], self.__start_player_turn)

  def __start_player_turn(self):
    self.select.active = True
    self.__update_phase = self.__update_player_turn

  def __update_player_turn(self):
    pass

  def __use_player_skill(self, skill):
    action = Action(self.player, self.enemy, skill.id)
    self.__execute_action(action, self.__start_enemy_turn)

  def __execute_action(self, action: Action, on_finish):
    from ..managers import Database
    self.__action = action
    self.__check_animation = True
    self.__update_phase = self.__update_action
    self.__on_action_finish = on_finish
    self.__on_motion_finish = self.__perform_action
    action.user.start_motion(action.skill.motion, loops = 1)
    if action.skill.type == "damage":
      self.__animation_target = action.target
    elif self.__action.skill.type == "heal":
      action.user.animation_id = 2
      action.user.animation_loops = 0
      self.__animation_target = action.user
    self.__motion_battler = action.user

  def __update_action(self):
    skill = self.__action.skill
    if self.__check_animation and self.__motion_battler.motion_count == skill.animation_wait:
      self.__animation_target.animation_id = skill.animation_id
      self.__animation_target.animation_loops = skill.animation_loops
      self.__check_animation = False
    if self.__motion_battler.is_in_animation:
      return
    self.__on_motion_finish()

  def __perform_action(self):
    value = self.__action.perform()
    self.__check_animation = False
    if self.__action.skill.type == "damage":
      self.__action.target.start_motion("hurt", loops = 1)
      self.__action.target.popup(value)
      self.__motion_battler = self.__action.target
    if self.__action.skill.type == "heal":
      self.__action.user.popup(value)
    self.__on_motion_finish = self.__check_victory

  def __check_victory(self):
    if self.player.is_dead:
      return self.__perform_defeat()
    if self.enemy.is_dead:
      return self.__perform_success()
    self.__on_action_finish()

  def __perform_defeat(self):
    from ..managers import Music, Game, Screen
    text = TextSprite("YOU HAVE BEEN DEFEATED!", Game.big_font)
    text.move((Screen.width - text.width) / 2, (Screen.height - text.height * 3) / 2)
    self.add(text)
    v = "victory" if Game.player.victories == 1 else "victories"
    text2 = TextSprite(f"You died after {Game.player.victories} {v}!", Game.big_font)
    text2.move((Screen.width - text2.width) / 2, text.y + text.height)
    self.add(text2)
    text3 = TextSprite(f"Your final score is {Game.player.score // 10:,d}!", Game.big_font)
    text3.move((Screen.width - text3.width) / 2, text2.y + text2.height)
    self.add(text3)
    Music.play("game_over")
    self.__update_phase = self.__update_defeat_message

  def __update_defeat_message(self):
    from ..managers import Scenes, Input, Sound
    from ..scenes import SelectScene
    if Input.is_triggered("accept"):
      Sound.play("accept")
      Scenes.goto(SelectScene())

  def __perform_success(self):
    from ..managers import Scenes
    from ..scenes import FieldScene
    from ..sprites import VictoryWindow
    self.player.victories += 1
    self.player.score += (1 + self.enemy.level - self.player.level) * 100_000
    self.__old_stats = self.player.stats
    self.__old_level = self.player.level
    gold = self.enemy.gold
    self.player.gold += gold
    exp = self.enemy.experience
    self.player.gain_experience(exp)
    self.__update_phase = self.__update_victory
    self.__level_up = self.player.level != self.__old_level
    self.add(VictoryWindow(exp, gold))
   

  def __update_victory(self):
    from ..managers import Music, Input, Sound, Scenes
    from ..scenes import FieldScene
    Music.play_once("victory")
    if Input.is_triggered("accept"):
      Sound.play("accept")
      if self.__level_up:
        self.__show_level_up()
      else:
        Scenes.goto(FieldScene())

  def __show_level_up(self):
    from ..sprites import LevelUpWindow
    self.add(LevelUpWindow(self.__old_level, self.__old_stats))
    self.__update_phase = self.__update_level_up

  def __update_level_up(self):
    from ..managers import Input, Sound, Scenes
    from ..scenes import FieldScene
    if Input.is_triggered("accept"):
      Sound.play("accept")
      Scenes.goto(FieldScene())