#!/usr/bin/env python3
import asyncio
import pygame
import jsonpickle

from random import seed
import time

from src.managers import Game, Screen

pygame.init()

Screen.setup()
Game.play()

async def main():
    seed(time.time())
    await Game.loop()

asyncio.run(main())
