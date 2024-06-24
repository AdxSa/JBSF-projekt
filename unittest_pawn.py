import unittest
from pawn import Pawn


class TestPawn(unittest.TestCase):

    def setUp(self):
        self.pawn = Pawn("white", 1, (0, 0, 0))

    def test_move(self):
        self.pawn.move(2)
        self.assertEqual(self.pawn.coords, (0, 0, 2))

    def test_upgrade(self):
        self.pawn.upgrade()
        self.assertEqual(self.pawn.coords, (0, 1, 0))

    def test_degrade(self):
        self.pawn.is_in_destination_square = True
        self.pawn.degrade()
        self.assertEqual(self.pawn.coords, (0, 0, 0))


if __name__ == '__main__':
    unittest.main()

