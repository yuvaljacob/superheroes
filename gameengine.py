import random


class GameEngine:
    @staticmethod
    def get_random_power_level():
        return random.randint(1, 99)
    
    RULES = '''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ RULES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            - Basic fights between squads are determined by the total power level of a squad, the squad with the higher
             total power level wins the match-up

            - If both squad's power level is equal, a grand war starts between the squads

            - In each fight between two heroes, they strike in turns, the hero with the higher power level will strike first

            - Each strike will handle the striker's power_level and will remove this value from the defender's 
              HP (hit points)

            - The round will end when a defender's HP drops to zero or below, he will be removed from the squad until the
              war is over

            - When a fight between two heroes ends, the rosters' order is shuffled for a new random fight, injured heroes
              start with the updated hp value following their injuries from prior battles of the same war

            - The HP of the hero will be refreshed to 100 when the war ends, defeated heroes will be revived :)    
    '''

    MENU = '''                *********************************************************************************************
                * 1. Show rules                                                                             *
                * 2. Show current squads                                                                    *
                * 3. Show all heroes                                                                        *
                * 4. Show a specific squad's roster                                                         *
                * 5. Create squads and heroes with pre-written data, heroes will have a random power level  *
                * 6. Create hero                                                                            *
                * 7. Create squad                                                                           *
                * 8. Recruit a hero to a specific squad                                                     *
                * 9. Start game!                                                                            *
                *********************************************************************************************
                Type 'menu' in order to see this menu again
    '''

    def __init__(self, service):
        self._service = service
        self._switcher = {
            1: self._show_rules,
            2: self._show_squads,
            3: self._show_heroes,
            4: self._show_squad,
            5: self._fill_data,
            6: self._create_hero,
            7: self._create_squad,
            8: self._recruit_hero,
            9: self._start_game
        }

        print("Welcome to the Squad Battle Simulator\n")
        self._show_menu()
        self._get_user_input()

    def _show_rules(self):
        print(GameEngine.RULES)
        self._get_user_input()

    def _show_squads(self):
        self._service.show_squads()
        self._get_user_input()

    def _show_heroes(self):
        self._service.show_heroes()
        self._get_user_input()

    def _show_squad(self):
        squad_name = input("\nPlease enter the name of the squad you wish to see\n")
        self._service.show_squad(squad_name)
        self._get_user_input()

    def _fill_data(self):
        """
        This method creates a preset of heroes and squads, some heroes with a fixed power level in order to have a draw
        between two squads, and some heroes with random power levels
        """

        # Totally random stats squads (power levels of heroes in roster is random)
        # Note that "Anakin Skywalker" is recruited into two squads, if they will have a war he will not participate

        self._service.create_squad("The Rebels")
        self._service.create_hero("Anakin Skywalker", True, GameEngine.get_random_power_level())
        self._service.create_hero("Luke Skywalker", True, GameEngine.get_random_power_level())
        self._service.create_hero("C3PO", True, GameEngine.get_random_power_level())
        self._service.create_hero("R2D2", True, GameEngine.get_random_power_level())
        self._service.create_hero("Chewbacca", True, GameEngine.get_random_power_level())
        self._service.create_hero("Han Solo", True, GameEngine.get_random_power_level())

        self._service.create_squad("The Dark Side")
        self._service.create_hero("Senator Palpatine", False, GameEngine.get_random_power_level())
        self._service.create_hero("General Tarkin", False, GameEngine.get_random_power_level())
        self._service.create_hero("Darth Maul", False, GameEngine.get_random_power_level())
        self._service.create_hero("Count Dooku", False, GameEngine.get_random_power_level())

        self._service.recruit_heroes(["Anakin Skywalker", "Luke Skywalker", "C3PO", "R2D2", "Chewbacca", "Han Solo"],
                                     "The Rebels")

        self._service.recruit_heroes(["Anakin Skywalker", "Senator Palpatine", "General Tarkin", "Darth Maul",
                                      "Count Dooku", "Han Solo"], "The Dark Side")

        # End of random powered squads

        # Two squads with a different number of members, but an equal number of total power (so the "war" mode will get
        # activated)

        self._service.create_squad("Guardians of the Galaxy")
        self._service.create_hero("Star-Lord", True, 86)
        self._service.create_hero("Gamora", True, 94)
        self._service.create_hero("Drax", True, 73)
        self._service.create_hero("Rocket Raccoon", True, 54)
        self._service.create_hero("Groot", True, 66)

        self._service.create_squad("The Avengers")
        self._service.create_hero("Wolverine", True, 83)
        self._service.create_hero("Spider-Man", True, 67)
        self._service.create_hero("Ant-Man", True, 42)
        self._service.create_hero("Doctor Strange", True, 81)
        self._service.create_hero("Deadpool", True, 60)
        self._service.create_hero("Iron Man", True, 1)
        self._service.create_hero("Thor", True, 39)

        self._service.recruit_heroes(["Star-Lord", "Gamora", "Drax", "Rocket Raccoon", "Groot"],
                                     "Guardians of the Galaxy")

        self._service.recruit_heroes(["Wolverine", "Spider-Man", "Ant-Man", "Doctor Strange", "Deadpool", "Iron Man",
                                      "Thor"], "The Avengers")

        self._get_user_input()

    def _create_hero(self):
        """
        This method gets the needed inputs from the user and calls the service after in order to
        create a new hero
        """
        while True:
            hero_name = input("Please enter a desired name for the new hero!\n")
            if isinstance(hero_name, str):
                break
            else:
                print("Please provide a valid string for the hero's name\n")
        while True:
            is_good = input("Is this hero good, or bad?\n")
            if is_good == "good":
                is_good = True
                break
            elif is_good == "bad":
                is_good = False
                break
            else:
                print("Try again, please type good or bad\n")
        while True:
            power_level = input("What is the hero's power level? Please provide a number between 1 to 100\n")
            if power_level.isdigit():
                print(int(power_level))
                if 0 < int(power_level) <= 100:
                    print(f"New hero created! Name: {hero_name}, it is a {is_good} hero with a power level of "
                          f"{power_level}")
                    break
                else:
                    print("Please try again, you need to provide a number between 1 to 100\n")
            else:
                print("Please try again, you need to provide a number between 1 to 100\n")

        power_level = int(power_level)
        self._service.create_hero(hero_name, is_good, power_level)
        self._get_user_input()

    def _create_squad(self):
        """
        This method gets the input from the user and calls the service after in order to
        create a new squad
        """
        squad_name = input("Please choose a name for the new squad\n")
        if not squad_name == "back":
            self._service.create_squad(squad_name)
        self._get_user_input()

    def _recruit_hero(self):
        """
        This method asks the user to provide a hero name and a squad name, checks if they exist, and finally adds the
        hero to the given squad
        """
        hero_name = input("Please enter the name of the hero you wish to recruit (must be an existing hero)\n")
        if hero_name == "back":
            self._get_user_input()
            return
        all_heroes = map(lambda x: x.name, self._service.heroes)
        if hero_name not in all_heroes:
            print("Hero name could not be found, please try again or type back if you wish to cancel the operation")
            self._recruit_hero()
            return

        all_squads = list(map(lambda x: x.name, self._service.squads))
        while True:
            squad_name = input(f"Please enter the name of the squad you wish to add {hero_name} into\n")
            if squad_name == "back":
                self._get_user_input()
                return
            if squad_name not in all_squads:
                print("Squad name could not be found, please try again or type back if you wish to cancel the operation")
            else:
                squad_roster_names = self._service.get_squad_list(squad_name)
                print("H")
                print(squad_roster_names)
                if hero_name in squad_roster_names:
                    print(f"Hero {hero_name} is already in {squad_name}, try again or type back to cancel")
                else:
                    self._service.recruit_heroes([hero_name], squad_name)
                    self._get_user_input()
                    break

    def _start_game(self):
        """
        This method checks if there are more than two squads saved in the service and starts a battle between two random
        squads
        """
        print("Starting game...\n")
        squads = self._service.squads
        if not squads or len(squads) < 2:
            print("Can't start game, create more squads!\n")
            self._get_user_input()
            return
        random.shuffle(squads)
        self._service.battle(squads[0], squads[1])
        self._get_user_input()

    def _show_menu(self):
        print(GameEngine.MENU)
        self._get_user_input()

    def _default(self):
        print("Please enter a number between 1 to 9\n")
        self._get_user_input()

    def _get_user_input(self):
        """
        This method represents the main menu part of the simulation, it gets the desired operation as an input from the
        user, checks that it is a number between 1 and 10 and then runs the desired operation as a method by
        using the switcher which holds all of these relevant methods
        """
        operation = input("\nPlease choose the desired operation by entering its number\n"
                          "You can write menu again in order to see it\n")
        if operation == "menu":
            self._show_menu()
        elif operation.isdigit():
            operation = int(operation)
            if 0 < operation < 10:
                self._switcher.get(operation, self._default)()
        else:
            print("Please enter a number between 1 to 9\n")
            self._get_user_input()
