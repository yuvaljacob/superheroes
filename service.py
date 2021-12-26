import random
from squad import Squad
from hero import Hero


class Service:
    hero_id = 0
    squad_id = 0

    def __init__(self):
        self._heroes = []
        self._squads = []
        self._roster_a = []
        self._roster_b = []

    @property
    def heroes(self):
        return self._heroes

    @property
    def squads(self):
        return self._squads

    def create_hero(self, hero_name: str, is_good: bool, power_level: int):
        """
        This method checks if the hero already exists, if not it creates it
        :param hero_name: The name of the hero to create
        :param is_good: A property that will determine if the hero is good or bad
        :param power_level: The new hero's power level
        """
        if not self.get_hero_by_name(hero_name):
            print(f"Creating a new hero named {hero_name}, with {power_level} power level")
            self._heroes.append(Hero(hero_name, is_good, power_level, Service.hero_id))
            Service.hero_id += 1
        else:
            print("Hero name already exists, please try a different name")

    def create_squad(self, squad_name: str):
        """
        This method checks if the squad name already exists and if not, it creates a new squad with this name
        :param squad_name: The name of the squad to create
        """
        if not self.get_squad_by_name(squad_name):
            print(f"Creating a new squad named {squad_name}")
            self._squads.append(Squad(squad_name, Service.squad_id))
            Service.squad_id += 1
        else:
            print("Squad name already exists, please try a different name")

    def recruit_heroes(self, hero_names: list, squad_name: str):
        """
        This method checks if the provided squad name exists and then goes over the list of heroes, for each hero, if it
        exists, it will be added to the squad_name provided to the method
        :param hero_names: A list of heroes that need to be added to a squad
        :param squad_name: The name of the squad that we wish to add heroes into
        """
        squad = self.get_squad_by_name(squad_name)
        if squad:
            for x in hero_names:
                hero = self.get_hero_by_name(x)
                if hero:
                    print(f"Adding {hero.name} to {squad.name}!")
                    squad.add_hero(hero.hero_id)
                    self.update_squad_power(squad)
                else:
                    print(f"Hero name {x} could not be found")
        else:
            print(f"Squad name {squad_name} could not be found")

    def show_squad(self, squad_name):
        """
        This method shows the details of all heroes in a specific squad
        :param squad_name: The name of the squad we wish to see the details of
        """
        squad = self.get_squad_by_name(squad_name)
        if squad:
            for x in squad.hero_list:
                hero = self.get_hero_by_id(x)
                print(hero.name)
        else:
            print(f"Squad {squad_name} not found")

    def get_squad_list(self, squad_name) -> list:
        """
        Check if the squad name exists and returns a list of its heroes by id
        :param squad_name: The squad we wish to get a list of heroes for
        """
        squad = self.get_squad_by_name(squad_name)
        squad_list = []
        if squad:
            for x in squad.hero_list:
                squad_list.append(self.get_hero_by_id(x).name)
        else:
            print(f"Squad name {squad_name} could not be found")
        return squad_list

    def show_squads(self):
        """
        Check if the list of squads is not empty and if not, print the list of existing squads
        :return: This method does not return a value
        """
        if self._squads:
            print("SQUADS LIST:")
            for i in range(0, len(self._squads)):
                print(f"{i + 1}. {self._squads[i].name}")
        else:
            print("There are no squads yet!")

    def show_heroes(self):
        """
        Check if the list of existing heroes is not empty, and if not, print a list of them including their nature and
        power level
        :return: This method does not return a value
        """
        if self._heroes:
            print("HEROES LIST:\n")
            table_data = [["Hero Name", "Hero's Nature", "Power Level"]]
            for i in range(0, len(self._heroes)):
                hero_name = self._heroes[i].name
                hero_nature = "Good"
                power_level = self._heroes[i].power_level
                if not self._heroes[i].is_good:
                    hero_nature = "Bad"
                table_data.append([f"{i + 1}. {hero_name}", hero_nature, power_level])

            for row in table_data:
                print("{: <20} {: <20} {: <20}".format(*row))
        else:
            print("The list of heroes is still empty, please add some heroes!")

    def set_squads_activity(self, squads: list, is_resting: bool):
        for x in squads:
            x.is_resting = is_resting

    def battle(self, squad_a: Squad, squad_b: Squad):
        """
        Sets both given squads' resting status to False, checks which squad has a higher total power level, prints
        the winner's name accordingly and sets the squads' resting status back to True.
        If the total power level of both squads is equal, calls the war method with both squads as arguments.
        :param squad_a: The first squad that will join the battle.
        :param squad_b: The second squad that will join the battle.
        """
        print(f"Starting a battle between {squad_a.name} and {squad_b.name}!")
        self.set_squads_activity([squad_a, squad_b], False)
        if squad_a.total_power > squad_b.total_power:
            print(f"{squad_a.name} has won {squad_b.name} with {squad_a.total_power} over {squad_b.total_power} "
                  f"total power")
            self.set_squads_activity([squad_a, squad_b], True)
        elif squad_a.total_power < squad_b.total_power:
            print(f"{squad_b.name} has won {squad_a.name} with {squad_b.total_power} over {squad_a.total_power} "
                  f"total power")
            self.set_squads_activity([squad_a, squad_b], True)
        else:  # draw
            print("Total power is equal between the squads.")
            self._war(squad_a, squad_b)

    def _fight(self, attacker: Hero, defender: Hero, is_attacker_squad_a: bool, squad_a, squad_b):
        """
        Starts a fight between two heroes, each hero strikes in his turn and deals damage according to his power
        level. If the defender is still alive (HP > 0), run recursively while switching between attacker and
        defender until one of them has HP < 0, when that happens, the method removes the fight's loser from his
        squad's temporary roster
        :param attacker: The attacker who deals damage
        :param defender: The defender who receives damage
        :param is_attacker_squad_a: Used to know from which roster to remove the defender
        :return: This method does not return a value
        """
        if defender.hp - attacker.power_level <= 0:
            print(f"{attacker.name} dealt a final blow to of {attacker.power_level} damage to {defender.name} who "
                  f"had {defender.hp} hit points!")
            defender.hp = 0
            if is_attacker_squad_a:
                print(f"Removing {defender.name} from {squad_b.name}'s roster")
                self._roster_b.remove(defender)
            else:
                print(f"Removing {defender.name} from {squad_a.name}'s roster")
                self._roster_a.remove(defender)
            return
        else:
            defender.hp -= attacker.power_level
            print(f"{attacker.name} inflicted {attacker.power_level} damage to {defender.name} and left him with"
                  f" {defender.hp} hit points")
            self._fight(defender, attacker, not is_attacker_squad_a, squad_a, squad_b)

    def _war(self, squad_a: Squad, squad_b: Squad):
        """
        Creates an additional list which acts as a temporary squad roster, checks for each here if it exists in both
        squads, if it does, remove it from both temporary rosters. Then, as long as there are living heroes in both
        squads, start a fight between two random heroes from both rosters. When there is only one squad left with
        heroes, print who won, sets both squad's state to resting and fill all heroes from both squads' HP to back to
        100
        :param squad_a: The first squad to join the war
        :param squad_b: The second squad to join the war
        :return: This method does not return a value
        """
        print(f"Starting a war between {squad_a.name} and {squad_b.name}!")

        # Copy hero list as roster to avoid mutation
        self._roster_a = list(map(self.get_hero_by_id, squad_a.hero_list))
        self._roster_b = list(map(self.get_hero_by_id, squad_b.hero_list))

        # Remove a hero from both rosters in case it's the same hero
        for x in self._roster_a:
            for y in self._roster_b:
                if x == y:
                    self._roster_a.remove(x)
                    self._roster_b.remove(x)

        # As long as there are heroes to fight in both squads, run logic below
        while self._roster_a and self._roster_b:
            random.shuffle(self._roster_a)
            random.shuffle(self._roster_b)
            hero_a = self._roster_a[0]
            hero_b = self._roster_b[0]
            print(f"Starting a fight between {hero_a.name} and {hero_b.name}")
            if hero_a.power_level > hero_b.power_level:
                self._fight(hero_a, hero_b, True, squad_a, squad_b)
            elif hero_a.power_level < hero_b.power_level:
                self._fight(hero_b, hero_a, False, squad_a, squad_b)
            else:
                if len(self._roster_a) == len(self._roster_b) == 1:
                    self._fight(hero_a, hero_b, True, squad_a, squad_b)
                else:
                    continue

        if self._roster_a:
            print(f"Squad {squad_a.name} has defeated {squad_b.name} in the war!")
            self._roster_a = []
        else:
            print(f"Squad {squad_b.name} has defeated {squad_a.name} in the war!")
            self._roster_b = []


        self.set_squads_activity([squad_a, squad_b], True)

        for x in squad_a.hero_list:
            self.get_hero_by_id(x).hp = 100
        for x in squad_b.hero_list:
            self.get_hero_by_id(x).hp = 100

    def update_squad_power(self, squad: Squad):
        """
        Updates the squad's total power after a new hero was added to it
        :param squad: The squad we wish to update
        :return: This method does not return a value
        """
        total_power = 0
        for x in squad.hero_list:
            hero = self.get_hero_by_id(x)
            total_power += hero.power_level
        squad.total_power = total_power

    def get_hero_by_id(self, hero_id) -> Hero:
        return next((x for x in self._heroes if x.hero_id == hero_id), None)

    def get_hero_by_name(self, hero_name: str) -> Hero:
        return next((x for x in self._heroes if x.name == hero_name), None)

    def get_squad_by_name(self, squad_name: str) -> Squad:
        return next((x for x in self._squads if x.name == squad_name), None)
