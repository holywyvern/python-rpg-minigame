#!/usr/bin/env python3
from random import seed
import time

from src.managers import Game

if __name__ == '__main__':
  seed(time.time())
  Game.play()
