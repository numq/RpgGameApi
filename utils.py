import datetime
import random
import string


class AppConstants:
    MAX_NEW_CHAR_STATS = 30


class AppExceptions:
    DbEntryExists = ('DATABASE: ENTRY IS ALREADY EXISTS', 409)


class Generator:

    def __init__(self) -> None:
        super().__init__()

    def generate_stats(self, n):
        stats = {'strength': 0, 'agility': 0, 'intelligence': 0}
        first = abs(random.randint(n / 10, n - int(n / 3)))
        second = abs(random.randint(n / 10, n - int(n / 3)))
        third = abs(n - first - second)
        rands = [first, second, third]
        random.shuffle(rands)
        for i in stats.keys():
            stats[i] = rands.pop()
        return stats


class Randomizer:

    def random_name(self, n):
        return ''.join([random.choice(string.ascii_lowercase) for i in range(n)]).capitalize()

    def __init__(self) -> None:
        super().__init__()


class SqlAlchemyUtils:

    def datetime_sqlalchemy(self, value):
        return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
