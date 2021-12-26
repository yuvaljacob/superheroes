class Squad:

    def __init__(self, name: str, squad_id: int):
        self._name = name
        self._is_resting = True
        self._hero_list = []
        self._squad_id = squad_id
        self._total_power = 0

    @property
    def name(self):
        return self._name

    @property
    def is_resting(self):
        return self._is_resting

    @is_resting.setter
    def is_resting(self, is_resting: bool) -> None:
        if not isinstance(is_resting, bool):
            raise Exception("ERROR: Please provide a valid value for is_resting (expecting bool)")
        self._is_resting = is_resting

    @property
    def hero_list(self):
        return self._hero_list

    @property
    def squad_id(self):
        return self._squad_id

    @property
    def total_power(self):
        return self._total_power

    @total_power.setter
    def total_power(self, total_power: int):
        if not isinstance(total_power, int) or total_power < 1:
            raise Exception("ERROR: Please provide a valid value for total power (an int bigger than 0)")
        self._total_power = total_power

    def add_hero(self, hero_id: int):
        if not isinstance(hero_id, int) or hero_id < 0:
            print("ERROR: Invalid value for hero_id (expecting int)")
        else:
            self._hero_list.append(hero_id)
