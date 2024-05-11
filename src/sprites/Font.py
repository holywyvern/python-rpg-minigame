import pygame

class Font:
  LETTER_TABLE = [
    " ", "!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".",
    "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=",
    ">", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
    "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[",
   "\\", "]", "^", "_", " ", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
    "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y",
    "z", "{", "|", "}", "~", " ", "Ç", "Ü", "É", "Â", "Ä", "À", "Á", "ç", "Ê",
    "Ë", "È", "Ï", "Ì", "Ä", "A", "É", "æ", "æ", "Ô", "Ö", "Ò", "Ò", "Û", "Ù",
  ]
  
  def __init__(self, image: pygame.Surface, size: int, kerning: int):
    self.__size = size
    self.__kerning = kerning
    self.__sheet = image
    self.__cols = 15
    self.__rows = 8
    self.__letters = []
    for y in range(0, self.__rows):
      for x in range(0, self.__cols):
        self.__letters.append(self.__letter_at(x, y))
  
  def __letter_at(self, x: int, y: int):
    image = pygame.surface.Surface((self.__size, self.__size)).convert_alpha()
    image.fill((0, 0, 0, 0))
    image.blit(
      self.__sheet,
      (0, 0),
      pygame.Rect(x * self.__size, y * self.__size, self.__size, self.__size)
    )
    return image
  
  @property
  def kerning(self):
    return self.__kerning

  @property
  def size(self):
    return self.__size

  def measure_text(self, text: str):
    size = len(str(text))
    return size * self.__size - max(0, size - 2) * self.kerning

  def get_text(self, text: str):
    result: list[pygame.Surface] = []
    for c in list(text):
      index = 0
      try:
        index = Font.LETTER_TABLE.index(c)
      except ValueError: pass
      result.append(self.__letters[index])
    return result
