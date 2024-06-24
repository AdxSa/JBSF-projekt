import unittest
from unittest.mock import MagicMock
from farmer import Marketplace, Field, Animal


class TestAnimal(unittest.TestCase):

    def test_animal_initialization_rabbit(self):
        animal = Animal("Rabbit")
        self.assertEqual(animal.type, "Rabbit")
        self.assertEqual(animal.space_needed, 1)
        self.assertEqual(animal.value, 1)

    def test_animal_initialization_sheep(self):
        animal = Animal("Sheep")
        self.assertEqual(animal.type, "Sheep")
        self.assertEqual(animal.space_needed, 6)
        self.assertEqual(animal.value, 6)

    def test_animal_initialization_pig(self):
        animal = Animal("Pig")
        self.assertEqual(animal.type, "Pig")
        self.assertEqual(animal.space_needed, 6)
        self.assertEqual(animal.value, 12)

    def test_animal_initialization_cow(self):
        animal = Animal("Cow")
        self.assertEqual(animal.type, "Cow")
        self.assertEqual(animal.space_needed, 12)
        self.assertEqual(animal.value, 24)

    def test_animal_initialization_horse(self):
        animal = Animal("Horse")
        self.assertEqual(animal.type, "Horse")
        self.assertEqual(animal.space_needed, 12)
        self.assertEqual(animal.value, 48)

    def test_animal_place_on_field(self):
        animal = Animal("Rabbit")
        field_mock = MagicMock(spec=Field)
        animal.place(field_mock)
        self.assertIn(field_mock, animal.fields)


class TestField(unittest.TestCase):

    def test_field_initialization(self):
        field = Field(1, 0, 0)
        self.assertEqual(field.value, 1)
        self.assertEqual(field.capacity, 6)
        self.assertEqual(field.animals, [])
        self.assertEqual(field.x, 0)
        self.assertEqual(field.y, 0)
        self.assertEqual(field.neighbours, [])

    def test_field_upgrade(self):
        field = Field(1, 0, 0)
        field.upgrade()
        self.assertEqual(field.value, 2)

    def test_field_check_capacity(self):
        field = Field(1, 0, 0)
        animal_mock = MagicMock(spec=Animal)
        animal_mock.space_needed = 1
        field.animals = [animal_mock]
        field.check_capacity()
        self.assertEqual(field.capacity, 5)


class TestMarketplace(unittest.TestCase):

    def test_buy_field(self):
        marketplace = Marketplace()
        player_mock = MagicMock()
        player_mock.clipboard = {"Rabbit": 10}
        field_mock = MagicMock(spec=Field)
        field_mock.value = 1
        success = marketplace.buy_field(field_mock, player_mock)
        self.assertEqual(success, 1)

    def test_upgrade_field(self):
        marketplace = Marketplace()
        player_mock = MagicMock()
        player_mock.clipboard = {"Rabbit": 20}
        field_mock = MagicMock(spec=Field)
        field_mock.value = 1
        success = marketplace.upgrade_field(field_mock, player_mock)
        self.assertEqual(success, 1)


if __name__ == '__main__':
    unittest.main()

