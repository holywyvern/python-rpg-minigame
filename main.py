#!/usr/bin/env python3
import asyncio
import pygame

from random import seed
import time

from src.managers import Game

pygame.init()

async def main():
    await Game.loop()

seed(time.time())
Game.play()
asyncio.run(main())
