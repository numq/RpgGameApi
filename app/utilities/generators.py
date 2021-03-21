import math
import random
import string

from database.enums import ItemType, ItemRarity


class AppGenerator:

    def generate_random_name(self, length):
        return ''.join([random.choice(string.ascii_lowercase) for i in range(length)]).capitalize()

    def generate_name_by_pattern(self, pattern):
        vowels = 'aeiou'
        consonants = [i for i in string.ascii_lowercase if i not in vowels]
        return ''.join([random.choice(vowels) if i in vowels else random.choice(consonants) for i in
                        [j for j in pattern.lower() if j.isalpha()]]).capitalize()

    def generate_random_int(self):
        return random.randint(1, (2 ** 63 - 1))


class CharacterGenerator:

    def generate_stats(self, n):
        stats = {'strength': 0, 'agility': 0, 'intelligence': 0}
        first = random.randint(int(n * 0.2), int(n * 0.4))
        second = random.randint(int(n * 0.2), first)
        third = n - first - second
        rands = [first, second, third]
        random.shuffle(rands)
        for i in stats.keys():
            stats[i] = abs(rands.pop())
        return stats

    def generate_classname(self, stats):
        max_stat = max(stats, key=lambda k: stats[k])
        if max_stat == 'strength':
            return 'Warrior'
        elif max_stat == 'agility':
            return 'Ranger'
        elif max_stat == 'intelligence':
            return 'Mage'


class DungeonGenerator:

    def generate_dungeon(self):
        pass

    def generate_level(self):
        return random.randint(1, 100)

    def generate_experience(self, level):
        return random.randint(int(level * math.pi), int(level * math.tau))

    def generate_duration(self):
        return random.randint(1, 3)


class ItemGenerator:
    def generate_item(self):
        pass

    def generate_level_by_dungeon(self, level):
        if level < 10:
            return level
        return random.randint(level - 3, level + 3)

    def generate_type(self):
        return random.choice(list(ItemType))

    def generate_rarity(self):
        return random.choice(list(ItemRarity))

    def generate_stats(self, level, rarity):
        return CharacterGenerator().generate_stats(int(math.sqrt(level + rarity.value)))

    def generate_cost(self, level, rarity):
        return int(level + rarity.value * math.tau * 10)
