import jsonpickle

from .. import rpg

class DataManager:
  DATABASE_FILES = [
    'animations',
    'enemies',
    'jobs',
    'locations',
    'skills',
  ]

  def __init__(self):
    self.__data = {}

  @property
  def animations(self) -> list[rpg.Animation]:
    return self.__data['animations']

  @property
  def enemies(self) -> list[rpg.Enemy]:
    return self.__data['enemies']

  @property
  def jobs(self) -> list[rpg.Job]:
    return self.__data['jobs']

  @property
  def locations(self) -> list[rpg.Location]:
    return self.__data['locations']

  @property
  def skills(self) -> list[rpg.Skill]:
    return self.__data['skills']

  def load_database(self):
    for file in Database.DATABASE_FILES:
      self.load_data(file)

  def load_data(self, filename: str):
    with open(f'data/{filename}.json', 'r') as file:
      json = file.read()
      self.__data[filename] = jsonpickle.decode(json)
      

Database = DataManager()
