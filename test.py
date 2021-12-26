import unittest
import io
import sys
from service import Service

service = Service()


class TestService(unittest.TestCase):
    def test_create_hero(self):
        service.create_hero("test_hero", True, 87)
        hero = service.heroes[0]
        result = [hero.name, hero.is_good, hero.power_level]
        self.assertEqual(result, ["test_hero", True, 87])

    def test_create_squad(self):
        service.create_squad("test_squad")
        result = service.squads[0].name
        self.assertEqual(result, "test_squad")

    def test_recruit_heroes(self):
        service.recruit_heroes([service.heroes[0].name], service.squads[0].name)
        result = service.get_hero_by_id(service.squads[0].hero_list[0]).name
        self.assertEqual(result, "test_hero")

    def test_get_squad_list(self):
        service.recruit_heroes([service.heroes[0].name], service.squads[0].name)
        result = service.get_squad_list("test_squad")
        self.assertEqual(result, ["test_hero"])

    def test_show_squads(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        service.show_squads()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), "SQUADS LIST:\n1. test_squad\n")

    def test_set_squads_activity(self):
        squad = service.squads[0]
        print(f"squad {squad}")
        service.set_squads_activity([squad], False)
        self.assertEqual(squad.is_resting, False)

    def test_y_battle(self):
        service.create_squad("Guardians of the Galaxy")
        service.create_hero("Star-Lord", True, 86)
        service.create_hero("Gamora", True, 94)
        service.create_hero("Drax", True, 73)
        service.create_hero("Rocket Raccoon", True, 54)
        service.create_hero("Groot", True, 66)

        service.create_squad("The Avengers")
        service.create_hero("Wolverine", True, 83)
        service.create_hero("Spider-Man", True, 67)
        service.create_hero("Ant-Man", True, 42)
        service.create_hero("Doctor Strange", True, 81)
        service.create_hero("Deadpool", True, 60)
        service.create_hero("Iron Man", True, 100)
        service.create_hero("Thor", True, 39)

        captured_output = io.StringIO()
        sys.stdout = captured_output
        squad_a = service.squads[1]
        squad_b = service.squads[2]
        service.battle(squad_a, squad_b)
        sys.stdout = sys.__stdout__
        expected_message = "The Avengers has defeated Guardians of the Galaxy in the war!\n"
        self.assertEqual(captured_output.getvalue().endswith(expected_message), True)

    def text_y_war(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        squad_a = service.squads[1]
        squad_b = service.squads[2]
        service._war(squad_a, squad_b)
        sys.stdout = sys.__stdout__
        expected_message = "The Avengers has defeated Guardians of the Galaxy in the war!\n"
        self.assertEqual(captured_output.getvalue().endswith(expected_message), True)

    def test_update_squad_power(self):
        old_total_power = service.get_squad_by_name("test_squad").total_power
        service.create_hero("hero_b", True, 80)
        service.recruit_heroes(["hero_b"], "test_squad")
        self.assertEqual(old_total_power + 80, service.get_squad_by_name("test_squad").total_power)


if __name__ == '__main__':
    unittest.main()
