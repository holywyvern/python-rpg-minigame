from .Scene import Scene

class ControlsScene(Scene):
  def start(self):
    from ..sprites import ControlsWindow
    self.add(ControlsWindow())
  
  def update(self):
    from ..managers import Input, Sound, Scenes
    from ..scenes import SelectScene
    if Input.is_triggered("accept"):
      Sound.play("accept")
      Scenes.goto(SelectScene())    
    super().update()