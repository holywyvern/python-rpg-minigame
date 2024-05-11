#!/usr/bin/env python3
import asyncio
import pygame
import jsonpickle

from random import seed
import time

from src.managers import Game

pygame.init()

async def main():
    seed(time.time())
    Game.play()
    await Game.loop()

asyncio.run(main())
