import pygame

from .EventManager import Events

class MouseManager:
  def setup(self):
    self.__pos = (0, 0)
    Events.on(pygame.MOUSEBUTTONDOWN, self.__on_button_down)
    Events.on(pygame.MOUSEBUTTONUP, self.__on_button_up)
    Events.on(pygame.MOUSEMOTION, self.__on_mouse_move)
    Events.on(pygame.MOUSEWHEEL, self._on_wheel_move)

  def __on_button_down(self, event): pass
  def __on_button_up(self, event): pass
  def __on_mouse_move(self, event): pass
  def _on_wheel_move(self, event): pass

  @property
  def x(self): return self.__pos[0]

  @property
  def y(self): return self.__pos[1]

  @property
  def pos(self): return self.__pos

class KeyboardManager:
  def __init__(self):
    self.__trigger: dict[int, bool] = {}
    self.__down: dict[int, bool] = {}
    self.__repeat: dict[int, int] = {}
    self.__release: dict[int, bool] = {}
    self.__state: dict[int, bool] = {}

  def setup(self):
    Events.on(pygame.KEYDOWN, self.__on_key_down)
    Events.on(pygame.KEYUP, self.__on_key_up)
  
  def __on_key_down(self, event):
    self.__down[event.key] = False
    self.__repeat[event.key] = -1
    self.__state[event.key] = True

  def __on_key_up(self, event):
    self.__state[event.key] = False

  def is_down(self, key: int):
    return (key in self.__down) and self.__down[key]

  def is_up(self, key: int):
    return (key not in self.__down) or not self.__down[key]

  def is_triggered(self, key: int):
    return (key in self.__trigger) and self.__trigger[key]

  def is_reppeated(self, key: int):
    return (key in self.__repeat) and (self.__repeat[key] == 0)

  def update(self):
    for key in self.__state.keys():
      if self.__state[key]:
        self.__trigger[key] = not self.__down[key]
        self.__down[key] = True
        self.__repeat[key]  = (self.__repeat[key] + 1) % Input.REPEAT_INTERVAL
      else:
        self.__release[key] = self.__down[key]
        self.__down[key] = False
        self.__repeat[key] = -1

class GamepadState:
  def __init__(self, id: int):
    self.__hats: dict[int, tuple[float, float]] = {}
    self.__joystick = pygame.joystick.Joystick(id)
    self.__trigger: dict[int, bool] = {}
    self.__down: dict[int, bool] = {}
    self.__repeat: dict[int, int] = {}
    self.__release: dict[int, bool] = {}
    self.__state: dict[int, bool] = {}
  
  def on_button_down(self, button: int):
    self.__down[button] = False
    self.__repeat[button] = -1
    self.__state[button] = True

  def on_button_up(self, button: int):
    if button not in self.__down:
      self.__down[button] = False
    if button not in self.__repeat:
      self.__repeat[button] = -1
    self.__state[button] = False

  def on_hat_change(self, hat: int, value: tuple[float, float]):
    if hat not in self.__hats:
      self.__hats[hat] = (0.0, 0.0)
    old_value = self.__hats[hat]
    if old_value[0] != value[0]:
      self.__update_hat_button(hat, 0, value[0])
    if old_value[1] != value[1]:
      self.__update_hat_button(hat, 1, value[1])
    self.__hats[hat] = value

  def on_axis_change(self, axis: int, value: float):
    key = 10_000 * (axis + 1)
    if value > 0:
      self.on_button_down(key)
      self.on_button_up(key + 1)
    elif value < 0:
      self.on_button_up(key)
      self.on_button_down(key + 1)      
    else:
      self.on_button_up(key)
      self.on_button_up(key + 1)

  def __update_hat_button(self, hat: int, index: int, value: float):
    key = (hat + 1) * 100 + (index + 1) * 1_000
    if value < 0:
      self.on_button_down(key)
      self.on_button_up(key + 1)
    elif value > 0:
      self.on_button_up(key)
      self.on_button_down(key + 1)
    else:
      self.on_button_up(key)
      self.on_button_up(key + 1)

  def is_down(self, key: int):
    return (key in self.__down) and self.__down[key]

  def is_up(self, key: int):
    return (key not in self.__down) or not self.__down[key]

  def is_triggered(self, key: int):
    return (key in self.__trigger) and self.__trigger[key]

  def is_reppeated(self, key: int):
    return (key in self.__repeat) and (self.__repeat[key] == 0)

  @property
  def id(self):
    return self.__joystick.get_instance_id()

  def update(self):
    self.__update_buttons()

  def __update_buttons(self):
    for key in self.__state.keys():
      if self.__state[key]:
        self.__trigger[key] = not self.__down[key]
        self.__down[key] = True
        self.__repeat[key]  = (self.__repeat[key] + 1) % Input.REPEAT_INTERVAL
      else:
        self.__release[key] = self.__down[key]
        self.__down[key] = False
        self.__repeat[key] = -1

class GamepadManager():
  def setup(self):    
    pygame.joystick.init()
    self.__gamepads: dict[int, GamepadState] = {}
    Events.on(pygame.JOYDEVICEADDED, self.__on_gamepad_added)
    Events.on(pygame.JOYDEVICEREMOVED, self.__on_gamepad_removed)
    Events.on(pygame.JOYBUTTONDOWN, self.__on_gamepad_button_down)
    Events.on(pygame.JOYBUTTONUP, self.__on_gamepad_button_up)
    Events.on(pygame.JOYAXISMOTION, self.__on_gamepad_axis_move)
    Events.on(pygame.JOYHATMOTION, self.__on_gamepad_hat_move)

  def __on_gamepad_added(self, event):
    self.__gamepads[event.device_index] = GamepadState(event.device_index)

  def __on_gamepad_removed(self, event):
    if event.device_index in self.__gamepads:
      self.__gamepads.pop(event.device_index)

  def __on_gamepad_button_down(self, event):
    if event.joy in self.__gamepads:
      pad = self.__gamepads[event.joy]
      pad.on_button_down(event.button)

  def __on_gamepad_button_up(self, event):
    if event.joy in self.__gamepads:
      pad = self.__gamepads[event.joy]
      pad.on_button_up(event.button)

  def __on_gamepad_axis_move(self, event):
    if event.joy in self.__gamepads:
      pad = self.__gamepads[event.joy]
      if abs(event.value) > Input.AXIS_DEADZONE:
        pad.on_axis_change(event.axis, event.value)
      else:
        pad.on_axis_change(event.axis, 0)

  def __on_gamepad_hat_move(self, event):
    if event.joy in self.__gamepads:
      pad = self.__gamepads[event.joy]
      pad.on_hat_change(event.hat, event.value)


  def update(self):
    for pad in self.__gamepads.values():
      pad.update()

  @property
  def gamepads(self):
    return list(self.__gamepads.values())

  def is_down(self, key: int):
    return any(map(lambda i: i.is_down(key), self.gamepads))

  def is_up(self, key: int):
    return any(map(lambda i: i.is_up(key), self.gamepads))

  def is_triggered(self, key: int):
    return any(map(lambda i: i.is_triggered(key), self.gamepads))

  def is_reppeated(self, key: int):
    return any(map(lambda i: i.is_reppeated(key), self.gamepads))

Mouse = MouseManager()
Keyboard = KeyboardManager()
Gamepad = GamepadManager()

class InputManager:
  AXIS_DEADZONE = 0.3
  REPEAT_INTERVAL = 16

  KEYBOARD_MAPPINGS = {
    'accept': [pygame.K_SPACE, pygame.K_RETURN, pygame.K_x],
    'cancel': [pygame.K_ESCAPE, pygame.K_z],
    'up': [pygame.K_UP],
    'down': [pygame.K_DOWN],
    'left': [pygame.K_LEFT],
    'right': [pygame.K_RIGHT]
  }
  GAMEPAD_BUTTON_MAPPINGS = {
    'accept': [0],
    'cancel': [1],
    'up': [2_101, 20_001],
    'down': [2_100, 20_000],
    'left': [1_100, 10_001],
    'right': [1_101, 10_000],
  }

  def is_down(self, key: str):
    if key in InputManager.KEYBOARD_MAPPINGS:
      keys = InputManager.KEYBOARD_MAPPINGS[key]
      if any(map(lambda i: Keyboard.is_down(i), keys)):
        return True
    if key in InputManager.GAMEPAD_BUTTON_MAPPINGS:
      keys = InputManager.GAMEPAD_BUTTON_MAPPINGS[key]
      if any(map(lambda i: Gamepad.is_down(i), keys)):
        return True
    return False

  def is_up(self, key: str):
    if key in InputManager.KEYBOARD_MAPPINGS:
      keys = InputManager.KEYBOARD_MAPPINGS[key]
      if any(map(lambda i: Keyboard.is_up(i), keys)):
        return True
    if key in InputManager.GAMEPAD_BUTTON_MAPPINGS:
      keys = InputManager.GAMEPAD_BUTTON_MAPPINGS[key]
      if any(map(lambda i: Gamepad.is_up(i), keys)):
        return True
    return False

  def is_triggered(self, key: str):
    if key in InputManager.KEYBOARD_MAPPINGS:
      keys = InputManager.KEYBOARD_MAPPINGS[key]
      if any(map(lambda i: Keyboard.is_triggered(i), keys)):
        return True
    if key in InputManager.GAMEPAD_BUTTON_MAPPINGS:
      keys = InputManager.GAMEPAD_BUTTON_MAPPINGS[key]
      if any(map(lambda i: Gamepad.is_triggered(i), keys)):
        return True
    return False
  
  def is_reppeated(self, key: str):
    if key in InputManager.KEYBOARD_MAPPINGS:
      keys = InputManager.KEYBOARD_MAPPINGS[key]
      if any(map(lambda i: Keyboard.is_reppeated(i), keys)):
        return True
    if key in InputManager.GAMEPAD_BUTTON_MAPPINGS:
      keys = InputManager.GAMEPAD_BUTTON_MAPPINGS[key]
      if any(map(lambda i: Gamepad.is_reppeated(i), keys)):
        return True
    return False


  def setup(self):
    Gamepad.setup()
    Keyboard.setup()
    Mouse.setup()
  
  def update(self):
    Keyboard.update()
    Gamepad.update()

Input = InputManager()