from collections import Counter
import random

class Player:
    def __init__(self, id) -> None:
        self.id = id
        self.fields = []
        if self.id == 0:
            pass    # Append field (nie znam numeracji)
        elif self.id == 1:
            pass
        elif self.id == 2:
            pass
        elif self.id == 3:
            pass
    
    def roll_animal_dice(self):
        first = ["Wolf", "Fox", "Sheep", "Sheep", "Cow", "Horse"] + ["Rabbit"] * 6
        second = ["Wolf", "Fox", "Cow"] + ["Sheep"] * 3 + ["Rabbit"] * 6
        predator = [1, 1, 1, 2, 2, 4]
        roll = [random.choice(first), random.choice(second)]
        animals = self.get_animals()
        new_animals = {}
        if roll[0] == roll[1]:
            only_roll = roll[0]
            if only_roll in ["Fox", "Wolf"]:
                random.choice(predator)
                # Zjadanie
                random.choice(predator)
                # Zjadanie
            else:
                animals[only_roll] += (animals[only_roll] + 2) // 2
        else:
            if "Fox" in roll:
                random.choice(predator)
                # Zjada wszystkich u wszystkich graczy, uwzględnić!!!
            if "Wolf" in roll:
                random.choice(predator)
                # Zjadanie
            for animal in roll:
                if animals.get(animal) > 0:
                    new_animals[animal] = (animals[animal] + 1) // 2
        # Rozmieszczanie zwierzątek
        animals_to_place = []
        for animal in new_animals.keys():
            for i in new_animals[animal]:
                animals_to_place.append(Animal(animal))
                new_animals[animal] -= 1
        # Yyy, tutaj jest pod górkę...
        for animal in animals_to_place:
            animal.place()  # To na razie nic nie robi a ma robić dużo, w tym interfejs, choose field!
    
    def get_animals(self):
        free = 0
        animals = {}
        for field in self.fields:
            content = field.show_field()
            if content == 0:
                free += 1
            content = Counter(content)
            animals = Counter(animals)
            animals = dict(content + animals)
        return animals
    
    def upgrade_chosen_field(self):
        chosen_field = self.choose_field()
        if chosen_field not in self.fields:
            print("Nie Twoje to nie tykaj!")
        else:
            # ROBOCZO   
            value = 1
            field = Field(value)
            if field.value == 5: 
                print("Nie da się podnieść wyżej!") # To się musi gdzies wyświetlać, na razie jest print
                pass
            elif field.value == 1:
                # Płacenie
                # A co jeśli nas nie stać?
                field.upgrade()
            # Powtórzyć elif dla wartości 2 i 4

    def open_marketplace(self):
        pass

    def remove_animal(self, animal_type):
        # klikanie
        chosen_field = self.choose_field()
        if animal_type in chosen_field.show_field().keys():
            chosen_field.animals.pop()
            chosen_field.check_capacity()
        else:   # Wypisze gdzie indziej, na razie konsola
            print(f"There is no {animal_type} in this field")

    def place_animal(self, animal_type):
        # klikanie
        animal = Animal(animal_type)
        iter = 0
        for field in self.fields:
            if field.capacity >= animal.space_needed:
                break
            iter += 1
        if iter == len(self.fields):
            print("There is no space for another animal!")
            return 0
        chosen_field = self.choose_field()
        for i in range(animal.space_needed / 6):    #if i == 2 and NEIGHBOURS - zmodyfikować dla konia (nie mogą być dowolne trzy)
            while chosen_field.capacity < animal.space_needed:
                while chosen_field not in self.fields:
                    chosen_field = self.choose_field()
                chosen_field.animals.append(animal)
                animal.place(chosen_field)
                chosen_field.check_capacity()

    def buy_field(self, id):
        pass

class Animal:
    def __init__(self, animal_type) -> None:
        self.type = "Rabbit"
        if animal_type == 1:
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
            self.space_needed = 18
            self.value = 48
        self.fields = []

    def place(self, field):
        self.fields.append(field)

class Field:
    def __init__(self, value) -> None:  # Pewnie brakuje ID, jestem zmęczony i nie wiem 
        self.value = value
        self.capacity = 6
        self.animals = []

    def upgrade(self):
        field_values = [1, 2, 4, 5]
        self.value = field_values[field_values.index(self.value) + 1]

    def show_field(self):
        if self.animals == []:
            return 0
        else:
            name = self.animals[0].type
            number = len(self.animals)
        return {name : number}
    
    def check_capacity(self):
        actual_capacity = 0
        for animal in self.animals:
            actual_capacity += animal.space_needed
        self.capacity = 6 - actual_capacity
    
class Marketplace:
    def __init__(self, active) -> None:
        self.buy_prices = {"Rabbit" : 1, "Sheep" : 6, "Pig" : 12, "Cow" : 24, "Horse" : 48}    
        # self.sell_prices = {"Rabbit" : 0.75, "Sheep" : 4, "Pig" : 8, "Cow" : 16, "Horse" : 32}    # pieniądze
        self.player = active

    # Przyciski muszą być
    def exchange(self, first_type, second_type):
        new_animal = Animal(second_type)
        player_animals = self.player.get_animals()
        if first_type not in player_animals.keys():
            print(f"You don't have {first_type}!")

        price = self.buy_prices.get(second_type)
        first_val = self.buy_prices.get(first_type)
        
        if price > first_val:
            if player_animals.get(first_type) * first_val < price:
                print(f"Za biedny jesteś")
            else:
                for i in range(price / first_val):
                    self.player.remove_animal(first_type)
            self.player.place_animal(second_type)

        if price < first_val:
            # Tu coś o space_needed, żeby sprawdzać
            self.player.remove_animal(first_type)
            for i in range(first_val / price):
                self.player.place_animal(second_type)

    # def buy_field(self, value):
    #     chosen_field = self.player.choose_field()
    #     for player in players
    #         while chosen_field in self.player.fields:
    #             chosen_field = self.player.choose_field()


def choose_field():
    chosen_field = Field(1) # WIP, domyślnie ma klikać
    return chosen_field   


player = Player(0)
