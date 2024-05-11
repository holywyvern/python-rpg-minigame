import pygame

class EventHandler():
  def __init__(self):
     self.__events: dict[any, set] = {}

  def on(self, handle: int, callback):
    if handle not in self.__events:
      self.__events[handle] = set()
    self.__events[handle].add(callback)

  def off(self, handle: int, callback):
    if handle not in self.__events:
      self.__events[handle] = set()
    callbacks = self.__events[handle]
    if callback in callbacks:
       callbacks.remove(callback)

  def __fire(self, event: pygame.event.Event):
    handle = event.type
    if handle not in self.__events:
      self.__events[handle] = set()
    for callback in self.__events[handle]:
       callback(event)

  def clear(self, handle: int):
     self.__events[handle] = set()

  def update(self):
    for event in pygame.event.get():
      self.__fire(event)

Events = EventHandler()