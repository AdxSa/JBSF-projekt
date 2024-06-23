from random import randrange, choice
from collections import Counter
from pawn import Pawn
from farmer import Animal


class Player:
    def __init__(self, colour, pawn_spawn_coords, name):

        self.colour = colour
        self.pawns = []
        self.pawn_spawn_coords = pawn_spawn_coords
        self.current_roll = 0
        self.chosen_pawn = None
        self.rolled = False
        self.name = name
        self.pawns_id = set()
        # Farmer
        self.fields = []
        self.clipboard = {"Rabbit": 8, "Sheep": 12, "Pig": 4, "Cow": 10, "Horse": 2}
        self.to_clipboard = False

    def roll_dice(self):
        # if self.rolled:
        #     return print("Can't roll twice in one turn")
        self.current_roll = randrange(1, 5)
        self.rolled = True
        print(self.current_roll)

    def create_pawn(self):
        if len(self.pawns) == 0:
            m = min({0, 1, 2, 3} - self.pawns_id)
            self.pawns += [Pawn(self.colour, m, self.pawn_spawn_coords)]
            self.pawns_id.add(m)
        elif len(self.pawns) == 1:  # and self.farm_animals['sheep'] != 0 :
            m = min({0, 1, 2, 3} - self.pawns_id)
            self.pawns += [Pawn(self.colour, m, self.pawn_spawn_coords)]
            self.pawns_id.add(m)
        elif len(self.pawns) == 2:  # and self.farm_animals['pig'] != 0 :
            m = min({0, 1, 2, 3} - self.pawns_id)
            self.pawns += [Pawn(self.colour, m, self.pawn_spawn_coords)]
            self.pawns_id.add(m)
        elif len(self.pawns) == 3:  # and self.farm_animals['cow'] != 0 :
            m = min({0, 1, 2, 3} - self.pawns_id)
            self.pawns += [Pawn(self.colour, m, self.pawn_spawn_coords)]
            self.pawns_id.add(m)
        elif len(self.pawns) == 4:
            raise Exception("Osiągnięto maksymalną ilość pionków")
        else:
            raise Exception("Nie stać Cię na stworzenie nowego pionka")

    def choose_pawn(self, id):  # wybiera pionek gracza wyszukując go po id
        for i in self.pawns:
            if i.id == id:
                self.chosen_pawn = i
                print(f'wybrano pionek o id {i.id}')  # temp w celu informacji
                break

    def move_chosen_pawn(self):  # porusza wybranym przez gracza pionkiem o current_roll, następnie zeruje current_roll
        if self.chosen_pawn.is_in_destination_square:
            return print("Can't move pawn from destination square")
        self.chosen_pawn.move(self.current_roll)
        self.current_roll = 0

    def upgrade_chosen_pawn(self):
        if self.chosen_pawn.coords[1] == 0:  # and self.farm_animals['sheep'] != 0 :
            self.chosen_pawn.upgrade()
        elif self.chosen_pawn.coords[1] == 1:  # and self.farm_animals['pig'] != 0 :
            self.chosen_pawn.upgrade()
        elif self.chosen_pawn.coords[1] == 2:  # and self.farm_animals['cow'] != 0 :
            self.chosen_pawn.upgrade()
        elif self.chosen_pawn.coords[1] == 3:
            self.chosen_pawn.upgrade()  # powininno wyskoczyć "Max level of pawn has been reached"
        else:
            return print("Can't afford to upgrade a pawn")

    def degrade_chosen_pawn(self):
        if self.chosen_pawn.coords[1] == 0:  # powininno wyskoczyć "Min level of pawn has been reached"
            self.chosen_pawn.degrade()
        elif self.chosen_pawn.coords[1] == 1:
            self.chosen_pawn.degrade()
        elif self.chosen_pawn.coords[1] == 2:
            self.chosen_pawn.degrade()
        elif self.chosen_pawn.coords[1] == 3:
            self.chosen_pawn.degrade()
        else:
            return print("Can't afford to upgrade a pawn")

    def action(self, a):
        if a == 'roll dice':
            self.roll_dice()
        if a == 'choose pawn':
            self.choose_pawn(input('Enter pawn id:   '))
        if a == 'move pawn':
            self.move_chosen_pawn()
        if a == 'create pawn':
            self.create_pawn()
        if a == 'upgrade pawn':
            self.upgrade_chosen_pawn()
        if a == 'degrade pawn':
            self.degrade_chosen_pawn()

    # Farmer
    def get_animals(self):
        animals = Counter({"Rabbit": 0, "Sheep": 0, "Pig": 0, "Cow": 0, "Horse": 0})
        for field in self.fields:
            if len(field.animals) != 0:
                animals_on_field = Counter(dict())
                animals_on_field[field.animals[0].type] = len(field.animals)
                animals += animals_on_field
                animals["Cow"] //= 2
                animals["Horse"] //= 2
        return dict(animals)

    def roll_animal_dice(self):
        first_dice = ["Wolf", "Fox", "Sheep", "Sheep", "Cow", "Horse"] + ["Rabbit"] * 6
        second_dice = ["Wolf", "Fox", "Sheep", "Sheep", "Sheep", "Cow"] + ["Rabbit"] * 6
        a = choice(first_dice)
        b = choice(second_dice)
        print([a, b])
        return [a, b]
        # animals = self.get_animals()
        # predator = [1, 1, 1, 2, 2, 4]
        # new_animals = {}
        # if roll[0] == roll[1]:
        #     only_roll = roll[0]

        #     if only_roll == "Fox":
        #         self.predator_attack(choice(predator), "Fox")
        #         self.predator_attack(choice(predator), "Fox")

        #     elif only_roll == "Wolf":
        #         self.predator_attack(choice(predator), "Wolf")
        #         self.predator_attack(choice(predator), "Wolf")

        #     else:
        #         animals[only_roll] += (animals[only_roll] + 2) // 2
        # else:
        #     if "Fox" in roll:
        #         self.predator_attack(choice(predator), "Fox")

        #     if "Wolf" in roll:
        #         self.predator_attack(choice(predator), "Wolf")

        #     for animal in roll:
        #         if animal in ["Fox", "Wolf"]:
        #             continue

        #         else:
        #             if animals.get(animal) > 0:
        #                 new_animals[animal] = (animals[animal] + 1) // 2

        #     self.clipboard = dict(Counter(self.clipboard) + Counter(new_animals))

    # def predator_attack(self, val, predator):
    #     for field in self.fields:
    #         if field.value == val:
    #             while field.capacity != 6:
    #                 if predator == "Wolf":
    #                     if field.animals[0].space_needed != 1:
    #                         animal = field.animals.pop()
    #                         del animal
    #                         field.check_capacity()
    #                 else:
    #                     if field.animals[0].space_needed == 1:
    #                         animal = field.animals.pop()
    #                         del animal
    #                         field.check_capacity()


if __name__ == "__main__":
    Adam = Player('purple', (1, 0, 0), 'Adam')
    Adam.create_pawn()
    Adam.create_pawn()
    print(Adam.pawns)
    Adam.choose_pawn('0')
    print(Adam.chosen_pawn)
    print(Adam.chosen_pawn.coords)
    Adam.current_roll = 4
    Adam.move_chosen_pawn()
    Adam.current_roll = 4
    Adam.move_chosen_pawn()
    Adam.current_roll = 4
    Adam.move_chosen_pawn()
    Adam.current_roll = 4
    Adam.move_chosen_pawn()

    Adam.chosen_pawn.upgrade()

    Adam.current_roll = 4
    Adam.move_chosen_pawn()
    Adam.current_roll = 1
    Adam.move_chosen_pawn()
    Adam.current_roll = 4
    Adam.move_chosen_pawn()
    Adam.current_roll = 1
    Adam.move_chosen_pawn()
    Adam.current_roll = 4
    Adam.move_chosen_pawn()
    print(Adam.chosen_pawn.coords)
    Adam.chosen_pawn.upgrade()
    Adam.chosen_pawn.upgrade()
    Adam.chosen_pawn.upgrade()
    print(Adam.chosen_pawn.coords)
    Adam.chosen_pawn.degrade()
    Adam.chosen_pawn.degrade()
    Adam.chosen_pawn.degrade()
    Adam.chosen_pawn.degrade()
    Adam.chosen_pawn.degrade()
    print(Adam.chosen_pawn.coords)
    print(Adam.chosen_pawn)
