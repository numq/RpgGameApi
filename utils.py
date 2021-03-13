import random
import string


class Randomizer:
    random_name = lambda n: ''.join([random.choice(string.ascii_lowercase) for i in range(n)]).capitalize()

    def __init__(self) -> None:
        super().__init__()
