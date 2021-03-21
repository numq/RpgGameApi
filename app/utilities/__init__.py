# from abc import abstractmethod, ABCMeta
#
#
# class Generator(metaclass=ABCMeta):
#     pass
#
#
# class AppGenerator(Generator):
#
#     @abstractmethod
#     def generate_random_name(self, length):
#         pass
#
#     @abstractmethod
#     def generate_name_by_pattern(self, pattern):
#         pass
#
#     @abstractmethod
#     def generate_random_int(self):
#         pass
#
#
# class CharacterGenerator(Generator):
#
#     @abstractmethod
#     def generate_stats(self, n):
#         pass
#
#     @abstractmethod
#     def generate_classname(self, stats):
#         pass
#
#
# class DungeonGenerator(Generator):
#
#     @abstractmethod
#     def generate_dungeon(self):
#         pass
#
#     @abstractmethod
#     def generate_level(self):
#         pass
#
#     @abstractmethod
#     def generate_experience(self, level):
#         pass
#
#
# class ItemGenerator(Generator):
#
#     @abstractmethod
#     def generate_item(self):
#         pass
#
#     @abstractmethod
#     def generate_level_by_dungeon(self, dungeon):
#         pass
#
#     @abstractmethod
#     def generate_type(self):
#         pass
#
#     @abstractmethod
#     def generate_rarity(self):
#         pass
#
#     @abstractmethod
#     def generate_stats(self, level, rarity):
#         pass
#
#     @abstractmethod
#     def generate_cost(self, level, rarity):
#         pass
