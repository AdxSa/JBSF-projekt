from random import randrange, choice
from collections import Counter
from pawn import Pawn
from farmer import Animal


class Player:
    """Klasa reprezentująca gracza. Przechowuje jego kolor, nazwę, posiadane pola, pionki, posiadane zwierzęta i
    schowek (clipboard). Atrybuty self.rolled i self.to_clipboard obsługują rzut kostką i funkcje w GUI.
    """
    def __init__(self, colour, pawn_spawn_coords, name):
        """Inicjalizacja klasy Player określająca kolor gracza i położenie poczatkowe. 

        Args:
            colour (string): kolor gracza
            pawn_spawn_coords (tuple): koordynaty nowych pionków
            name (string): nazwa gracza
        """
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
        self.clipboard = {"Rabbit": 0, "Sheep": 0, "Pig": 0, "Cow": 0, "Horse": 0}
        self.to_clipboard = False

    def roll_dice(self):
        """Metoda losuje wynik rzutu kością (1-4) i ustawia atrybut self.rolled = True
        """
        self.current_roll = randrange(1, 5)
        self.rolled = True

    def create_pawn(self):
        """Metoda tworząca pionek i pobierająca jego koszt

        Raises:
            Exception: wyjątek gdy wystawiono wszystkie pionki
            Exception: wyjątek gdy koszt pionka przewyższa zasoby gracza
        """
        if len(self.pawns) == 0:
            m = min({0, 1, 2, 3} - self.pawns_id)
            self.pawns += [Pawn(self.colour, m, self.pawn_spawn_coords)]
            self.pawns_id.add(m)
        elif len(self.pawns) == 1 and self.clipboard['Sheep'] != 0:
            m = min({0, 1, 2, 3} - self.pawns_id)
            self.pawns += [Pawn(self.colour, m, self.pawn_spawn_coords)]
            self.pawns_id.add(m)
            self.clipboard['Sheep'] -= 1
        elif len(self.pawns) == 2 and self.clipboard['Pig'] != 0:
            m = min({0, 1, 2, 3} - self.pawns_id)
            self.pawns += [Pawn(self.colour, m, self.pawn_spawn_coords)]
            self.pawns_id.add(m)
            self.clipboard['Pig'] -= 1
        elif len(self.pawns) == 3 and self.clipboard['Cow'] != 0:
            m = min({0, 1, 2, 3} - self.pawns_id)
            self.pawns += [Pawn(self.colour, m, self.pawn_spawn_coords)]
            self.pawns_id.add(m)
            self.clipboard['Cow'] -= 1
        elif len(self.pawns) == 4:
            raise Exception("Osiągnięto maksymalną ilość pionków")
        else:
            raise Exception("Nie stać Cię na stworzenie nowego pionka")

    def choose_pawn(self, id):  # wybiera pionek gracza wyszukując go po id
        """wybiera pionek gracza wyszukując go po id

        Args:
            id (string): id pionka do wybrania
        """
        for i in self.pawns:
            if i.id == id:
                self.chosen_pawn = i
                print(f'wybrano pionek o id {i.id}')  # temp w celu informacji
                break

    def move_chosen_pawn(self):  # porusza wybranym przez gracza pionkiem o current_roll, następnie zeruje current_roll
        """porusza wybranym przez gracza pionkiem o current_roll, następnie zeruje current_roll
        """
        if self.chosen_pawn.is_in_destination_square:
            return print("Can't move pawn from destination square")
        self.chosen_pawn.move(self.current_roll)
        self.current_roll = 0

    def upgrade_chosen_pawn(self):
        """Metoda obsługuje wejście pionka na wyższy poziom ("krąg" szachownicy)
        """
        if self.chosen_pawn.coords[1] == 0 and self.clipboard['Sheep'] != 0:
            self.chosen_pawn.upgrade()
            self.clipboard['Sheep'] -= 1
        elif self.chosen_pawn.coords[1] == 1 and self.clipboard['Pig'] != 0:
            self.chosen_pawn.upgrade()
            self.clipboard['Pig'] -= 1
        elif self.chosen_pawn.coords[1] == 2 and self.clipboard['Cow'] != 0:
            self.chosen_pawn.upgrade()
            self.clipboard['Cow'] -= 1
        elif self.chosen_pawn.coords[1] == 3:
            self.chosen_pawn.upgrade()  # powininno wyskoczyć "Max level of pawn has been reached"
        else:
            return print("Can't afford to upgrade a pawn")

    def degrade_chosen_pawn(self):
        """Metoda obsługuje zejście pionka do niższego rzędu
        """
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

    # Farmer
    def get_animals(self):
        """Metoda zlicza zwierzęta znajdujące się na polach gracza.

        Returns:
            dict: zwraca słownik zwierzę : liczba 
        """
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
        """Rzut kośćmi zwierząt (D12)

        Returns:
            list: lista przechowująca wynik pierwszego i drugiego rzutu koścmi
        """
        first_dice = ["Wolf", "Fox", "Sheep", "Sheep", "Cow", "Horse"] + ["Rabbit"] * 6
        second_dice = ["Wolf", "Fox", "Sheep", "Sheep", "Sheep", "Cow"] + ["Rabbit"] * 6
        a = choice(first_dice)
        b = choice(second_dice)
        print([a, b])
        return [a, b]

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
