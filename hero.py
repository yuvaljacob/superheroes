class Hero:

    def __init__(self, name: str, is_good: bool, power_level: int, hero_id: int):
        self._name = name
        self._is_good = is_good
        self._power_level = power_level
        self._hp = 100
        self._hero_id = hero_id

    @property
    def name(self):
        return self._name

    @property
    def is_good(self):
        return self._is_good

    @property
    def power_level(self):
        return self._power_level

    @power_level.setter
    def power_level(self, new_level: int):
        if new_level <= 0 or not isinstance(new_level, int):
            raise Exception("ERROR: Please provide a valid value for new_level (an integer bigger than 0)")
        self._power_level = new_level

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, hp: int):
        if not 0 <= hp <= 100 or not isinstance(hp, int):
            raise Exception("ERROR: Please provide a valid value for hp (an integer between 0 and 100)")
        self._hp = hp

    @property
    def hero_id(self):
        return self._hero_id
