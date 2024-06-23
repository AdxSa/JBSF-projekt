class Animal:
    def __init__(self, animal_type) -> None:
        self.type = animal_type
        if animal_type == 'Rabbit':
            self.space_needed = 1
            self.value = 1
        elif animal_type == "Sheep":
            self.space_needed = 6
            self.value = 6
        elif animal_type == "Pig":
            self.space_needed = 6
            self.value = 12
        elif animal_type == "Cow":
            self.space_needed = 12
            self.value = 24
        elif animal_type == "Horse":
            self.space_needed = 12
            self.value = 48
        self.fields = []

    def place(self, field):
        self.fields.append(field)


class Field:
    def __init__(self, value, x, y) -> None:
        self.value = value
        self.capacity = 6
        self.animals = []
        self.x = x
        self.y = y
        self.coords = x, y
        self.neighbours = check_neighbours(x, y)
        self.owner = None

    def __repr__(self):
        return f"Field({self.x},{self.y})"

    def upgrade(self):
        field_values = [1, 2, 4, 5]
        self.value = field_values[field_values.index(self.value) + 1]

    def show_field(self):
        if self.animals == []:
            return "No animals on that field"
        else:
            name = self.animals[0].type
            number = len(self.animals)
        return {name: number}

    def check_capacity(self):
        actual_capacity = 0
        for animal in self.animals:
            actual_capacity += animal.space_needed
        self.capacity = 6 - actual_capacity


class Marketplace:  # Pamięta aktywnego gracza i listę graczy
    def __init__(self) -> None:
        self.buy_prices = {"Rabbit": 1, "Sheep": 6, "Pig": 12, "Cow": 24, "Horse": 48}

        # Przyciski muszą być

    def exchange(self, first_type, second_type, player):

        price = self.buy_prices.get(second_type)
        first_val = self.buy_prices.get(first_type)

        if price > first_val:
            if player.clipboard[first_type] * first_val < price:
                print("Masz za mało zwierzat tego typu")
                return 0
            else:
                player.clipboard[first_type] -= price / first_val
                player.clipboard[second_type] += 1

        if price < first_val:
            if player.clipboard[first_type] == 0:
                print("Masz za mało zwierzat tego typu")
                return 0
            else:
                player.clipboard[first_type] -= 1
                player.clipboard[second_type] += first_val / price

    def buy_field(self, chosen_field, player):
        # DO IMPLEMENTACJI W GUI!!!

        # chosen_field = self.player.choose_field()

        # while any(chosen_field in player.fields for player in players):    # Sprawdza czy pole już do kogoś należy
        #     print("Field is already owned")
        #     chosen_field = self.player.choose_field()

        price = chosen_field.value
        if player.clipboard["Rabbit"] < price:  # Sprawdza czy gracz dysponuje odpowiednią liczbą królików do zakupu
            print("Masz za malo krolikow w schowku")
            return 0
        else:
            player.clipboard["Rabbit"] -= price
            player.fields.append(chosen_field)
            return 1
        #   ZMIANA KOLORU DO IMPLEMENTACJI W GUI!!!

    def upgrade_field(self, chosen_field, player):
        # DO IMPLEMENTACJI W GUI!!!
        #
        # chosen_field = self.player.choose_field()
        # while chosen_field not in self.player.fields:
        #     print("It's not your field")
        #     chosen_field = self.player.choose_field()
        if chosen_field.value == 1:
            price = 4
        elif chosen_field.value == 2:
            price = 10
        elif chosen_field.value == 4:
            price = 18
        else:
            print("Osiagnales maksymalny poziom pola")
            return 0
        if player.clipboard["Rabbit"] < price:
            print("Masz za malo krolikow w schowku")
            return 0
        else:
            player.clipboard["Rabbit"] -= price
            chosen_field.upgrade()
            return 1


def choose_field():
    chosen_field = Field(1)  # WIP, domyślnie ma klikać
    return chosen_field


def check_neighbours(x, y):
    neighbours = []
    if x < 8:
        neighbours.append((x + 1, y))
    if x > 1:
        neighbours.append((x - 1, y))
    if y < 8:
        neighbours.append((x, y + 1))
    if y > 1:
        neighbours.append((x, y - 1))
    return neighbours


def choose_animal():  # Do GUI, wybiera zwierzę ze schowka
    pass  # switch... case...
