from random import randrange
from pawn import Pawn


class Player:
    def __init__(self, colour, pawn_spawn_coords, name):

        self.colour = colour
        self.pawns = []
        self.pawn_spawn_coords = pawn_spawn_coords
        self.current_roll = 0
        self.farm_animals = {}
        self.chosen_pawn = None
        self.rolled = False
        self.name = name

    def roll_dice(self):
        if self.rolled:
            return print("Can't roll twice in one turn")
        self.current_roll = randrange(1, 5)
        self.rolled = True
        print(self.current_roll)

    def create_pawn(self):
        if len(self.pawns) == 0:
            self.pawns += [Pawn(self.colour, len(self.pawns), self.pawn_spawn_coords)]
        elif len(self.pawns) == 1:  # and self.farm_animals['sheep'] != 0 :
            self.pawns += [Pawn(self.colour, len(self.pawns), self.pawn_spawn_coords)]
        elif len(self.pawns) == 2:  # and self.farm_animals['pig'] != 0 :
            self.pawns += [Pawn(self.colour, len(self.pawns), self.pawn_spawn_coords)]
        elif len(self.pawns) == 3:  # and self.farm_animals['cow'] != 0 :
            self.pawns += [Pawn(self.colour, len(self.pawns), self.pawn_spawn_coords)]
        elif len(self.pawns) == 4:
            return print("Max number of pawns has been reached")
        else:
            return print("Can't afford to create a pawn")

    def choose_pawn(self, id):  # wybiera pionek gracza wyszukując go po id
        for i in self.pawns:
            if i.id == id:
                self.chosen_pawn = i
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
            self.chosen_pawn.degrade_pawn()
        elif self.chosen_pawn.coords[1] == 1:
            self.chosen_pawn.degrade_pawn()
        elif self.chosen_pawn.coords[1] == 2:
            self.chosen_pawn.degrade_pawn()
        elif self.chosen_pawn.coords[1] == 3:
            self.chosen_pawn.degrade_pawn()
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