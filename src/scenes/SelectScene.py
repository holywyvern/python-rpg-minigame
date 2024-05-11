from typing import Any
from .Scene import Scene

from ..managers import Screen, Game

from ..sprites import JobSelectSprite, TextSprite, BackgroundSprite, FaceSprite

from .FieldScene import FieldScene

class SelectScene(Scene):
  def start(self):
    from ..managers import Music
    Music.play("select")
    self.__phase = 0
    self.__cursor = 0
    self.__setup_background()
    self.__setup_title()
    self.__setup_jobs()
    self.__setup_face()
    self.__setup_texts()

  def __setup_background(self):
    self.add(BackgroundSprite("grassland"))

  def __setup_title(self):
    title = TextSprite("Select Your Character", Game.big_font)
    title.move((Screen.width - title.width) / 2, 16)
    self.add(title)
  
  def __setup_jobs(self):
    from ..managers import Database
    self.jobs = list(filter(None, Database.jobs))
    self.job_sprites = []
    w = Screen.width / len(self.jobs)
    self.__index = 0
    for i in range(0, len(self.jobs)):
      self.__add_job(i, w)

  def __setup_face(self):
    self.face_sprite = FaceSprite()
    self.face_sprite.job = self.jobs[0]
    self.face_sprite.move(50, 375)
    self.add(self.face_sprite)

  def __setup_texts(self):
    self.title = TextSprite("", Game.big_font)
    self.title.move(150, 375)
    self.line1 = TextSprite("", Game.small_font)
    self.line1.move(150, 400)
    self.line2 = TextSprite("", Game.small_font)
    self.line2.move(150, 416)
    self.line3 = TextSprite("", Game.small_font)
    self.line3.move(150, 432)
    self.add(self.title, self.line1, self.line2, self.line3)

  def __add_job(self, i:int, w: float):
    job = self.jobs[i]
    sprite = JobSelectSprite(job)
    x = i * w + w / 2 - sprite.width / 2
    y = Screen.height * 3 / 5
    self.job_sprites.append(sprite)
    sprite.move(x, y - sprite.height)
    self.add(sprite)
    if self.__index == i:
      sprite.active = True  

  def update(self, *args: Any, **kwargs: Any):
    self.__update_phase()
    self.__update_sprites()
    super().update(*args, **kwargs)

  def __update_phase(self):
    if self.__phase == 0:
      self.__update_selection()
    else:
      self.__update_confirm()

  def __update_selection(self):
    from ..managers import Input
    if Input.is_reppeated("left"):
      self.__select(self.__index - 1)
    elif Input.is_reppeated("right"):
      self.__select(self.__index + 1)
    elif Input.is_triggered("accept"):
      self.__confirm()
  
  def __update_confirm(self):
    from ..managers import Input, Sound
    if Input.is_reppeated("up") or Input.is_reppeated("down"):
      self.__cursor = (self.__cursor + 1) % 2
      Sound.play("cursor")
    elif Input.is_triggered("accept"):
      if self.__cursor == 0:
        self.__start_game()
      else:
        Sound.play("cancel")
        self.__phase = 0

  def __confirm(self):
    from ..managers import Sound
    Sound.play("accept")
    self.__phase = 1
    self.__cursor = 0

  def __start_game(self):
    from ..managers import Sound, Scenes
    from ..game import Player
    Sound.play("accept")
    Game.player = Player()
    Game.player.setup(self.jobs[self.__index].id)
    Scenes.goto(FieldScene())

  def __select(self, index: int):
    from ..managers import Sound
    size = len(self.jobs)
    self.__index = index
    Sound.play("cursor")
    if self.__index < 0:
      self.__index = size - 1
    if self.__index >= size:
      self.__index = 0

  def __update_sprites(self):
    for i in range(0, len(self.job_sprites)):
      sprite = self.job_sprites[i]
      sprite.active = i == self.__index
    job = self.jobs[self.__index]
    self.face_sprite.job = job
    if self.__phase == 0:
      self.title.text = job.name
      self.line1.text = job.description[0]
      self.line2.text = job.description[1]
      self.line3.text = job.description[2]
    else:
      self.title.text = "Are you sure?"
      if self.__cursor == 0:
        self.line1.text = " > Yes"
        self.line2.text = "   No"
      else:
        self.line1.text = "   Yes"
        self.line2.text = " > No"
      self.line3.text = ""

