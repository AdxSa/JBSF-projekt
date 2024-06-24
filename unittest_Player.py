import unittest
from unittest.mock import MagicMock
from pawn import Pawn
from Player import Player


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player("white", (0, 0, 0), "Alice")

    def test_create_pawn(self):
        self.player.create_pawn()
        self.assertEqual(len(self.player.pawns), 1)
        self.assertEqual(len(self.player.pawns_id), 1)

    def test_choose_pawn(self):
        pawn_mock = MagicMock(spec=Pawn)
        pawn_mock.id = 1
        self.player.pawns = [pawn_mock]
        self.player.choose_pawn(1)
        self.assertEqual(self.player.chosen_pawn, pawn_mock)

    def test_move_chosen_pawn(self):
        pawn_mock = MagicMock(spec=Pawn)
        pawn_mock.is_in_destination_square = False
        self.player.chosen_pawn = pawn_mock
        self.player.current_roll = 2
        self.player.move_chosen_pawn()
        pawn_mock.move.assert_called_once_with(2)

    def test_upgrade_chosen_pawn(self):
        pawn_mock = MagicMock(spec=Pawn)
        pawn_mock.coords = (0, 0, 0)
        pawn_mock.is_in_destination_square = False
        self.player.chosen_pawn = pawn_mock
        self.player.clipboard['Sheep'] = 1
        self.player.upgrade_chosen_pawn()
        pawn_mock.upgrade.assert_called_once()

    def test_degrade_chosen_pawn(self):
        pawn_mock = MagicMock(spec=Pawn)
        pawn_mock.coords = (0, 1, 0)
        pawn_mock.is_in_destination_square = False
        self.player.chosen_pawn = pawn_mock
        self.player.degrade_chosen_pawn()
        pawn_mock.degrade.assert_called_once()

    def test_get_animals(self):
        self.player.fields = []
        animals = self.player.get_animals()
        expected_animals = {"Rabbit": 0, "Sheep": 0, "Pig": 0, "Cow": 0, "Horse": 0}
        self.assertEqual(animals, expected_animals)


if __name__ == '__main__':
    unittest.main()

