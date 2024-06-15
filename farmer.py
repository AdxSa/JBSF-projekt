from collections import Counter
import random

players = []
animals_clipboard = {"Rabbit" : 0, "Sheep" : 0, "Pig" : 0, "Cow" : 0, "Horse" : 0}

class Player:
    def __init__(self, id) -> None:
        self.id = id
        self.fields = []
        self.animals = []
        if self.id == 0:
            pass    # Append field (nie znam numeracji)
        elif self.id == 1:
            pass
        elif self.id == 2:
            pass
        elif self.id == 3:
            pass
        self.animal_rolled = False
    
    def roll_animal_dice(self):
        first = ["Wolf", "Fox", "Sheep", "Sheep", "Cow", "Horse"] + ["Rabbit"] * 6
        second = ["Wolf", "Fox", "Cow"] + ["Sheep"] * 3 + ["Rabbit"] * 6
        predator = [1, 1, 1, 2, 2, 4]
        return [random.choice(first), random.choice(second)]

        roll = [random.choice(first), random.choice(second)]
        animals = self.get_animals()
        new_animals = {}
        if roll[0] == roll[1]:
            only_roll = roll[0]
            if only_roll in ["Fox", "Wolf"]:
                victim = random.choice(predator)
                # Zjadanie
                victim = random.choice(predator)
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
        # animals_to_place = []
        for animal_type in new_animals.keys():
            for animal in new_animals[animal_type]:
                self.place_animal(animal_type)

        #         animals_to_place.append(Animal(animal))
        #         new_animals[animal] -= 1
        # # Yyy, tutaj jest pod górkę...
        # for animal in animals_to_place:
        #     self.place_animal(animal)
  
    def get_animals(self):
        animals = {"Rabbit" : 0, "Sheep" : 0, "Pig" : 0, "Cow" : 0, "Horse" : 0}
        for animal_type in animals.keys():
            for animal in self.animals:
                if animal.type == animal_type:
                    animals[animal_type] += 1
        return animals
    
    # MARKETPLACE
    # def upgrade_chosen_field(self):
    #     chosen_field = self.choose_field()
    #     if chosen_field not in self.fields:
    #         print("Nie Twoje to nie tykaj!")
    #     else:
    #         # ROBOCZO   
    #         value = 1
    #         field = Field(value)
    #         if field.value == 5: 
    #             print("Nie da się podnieść wyżej!") # To się musi gdzies wyświetlać, na razie jest print
    #             pass
    #         elif field.value == 1:
    #             # Płacenie
    #             # A co jeśli nas nie stać?
    #             field.upgrade()
    #         # Powtórzyć elif dla wartości 2 i 4

    def remove_animal(self, animal_type):
        # klikanie
        chosen_field = self.choose_field()
        if animal_type in chosen_field.show_field().keys():
            removed_animal = chosen_field.animals.pop()
            chosen_field.check_capacity()
        else:   # Wypisze gdzie indziej, na razie konsola
            print(f"There is no {animal_type} in this field")

        if removed_animal.space_needed == 2:
            for field in removed_animal.fields:
                field.animals.pop()
                field.check_capacity
        del removed_animal

    def place_animal(self, animal_type):
        # klikanie
        animal = Animal(animal_type)

        if animal.space_needed < 12:
            bad_fields = []
            for field in self.fields:
                if field.capacity >= animal.space_needed:
                    break
                bad_fields.append(field)
            if len(bad_fields) == len(self.fields):
                print("There is no space for another animal!")
                return 0
            
            chosen_field = self.choose_field()    
            while (chosen_field.capacity < animal.space_needed) or (chosen_field not in self.fields):
                chosen_field = self.choose_field()
            chosen_field.animals.append(animal)
            animal.place(chosen_field)
            chosen_field.check_capacity()
            return 1

        else:
            good_fields = []
            potential_pairs = 0

            for field in self.fields:
                if field.capacity == 6:
                    good_fields.append(field)

            for field in good_fields:
                for neighbour in field.neighbours:
                    if neighbour.capacity == 6:
                        potential_pairs += 1
            
            if potential_pairs != 0:
                chosen_field = self.choose_field()    
            while (chosen_field.capacity < animal.space_needed) or (chosen_field not in self.fields):
                chosen_field = self.choose_field()

            second_field = self.choose_field()
            while (second_field.capacity < animal.space_needed) or (second_field not in self.fields) or (second_field not in chosen_field.neighbours):
                second_field = self.choose_field()
            
            animal.place(chosen_field)
            animal.place(second_field)
            chosen_field.animals.append(animal)
            chosen_field.check_capacity()
            second_field.animals.append(animal)
            second_field.check_capacity()
            return 1

    def choose_field(self):
        pass

    def relocate_to_clipboard(self):
        chosen_field = self.choose_field()    
        while chosen_field not in self.fields:
            chosen_field = self.choose_field()
        animal = chosen_field.animals[0]
        for field in animal.fields:
            field.animals.pop()
            field.check_capacity()
        animals_clipboard[animal.type] += 1
        del animal

    def relocate_to_board(self):
        chosen_animal = choose_animal() # Wybranie ikony zwierzaka ze schowka, wymaga przycisków. Do GUI
        if not self.place_animal(chosen_animal):
            print(f"There is no space for another {chosen_animal.type}")

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
        self.coords = x, y
        self.neighbours = check_neighbours(x, y)
        self.owner = None

    def upgrade(self):
        field_values = [1, 2, 4, 5]
        self.value = field_values[field_values.index(self.value) + 1]

    def show_field(self):
        if self.animals == []:
            return "No animals on that field"
        else:
            name = self.animals[0].type
            number = len(self.animals)
        return {name : number}
    
    def check_capacity(self):
        actual_capacity = 0
        for animal in self.animals:
            actual_capacity += animal.space_needed
        self.capacity = 6 - actual_capacity
    
class Marketplace:  # Pamięta aktywnego gracza i listę graczy
    def __init__(self, active) -> None:
        self.buy_prices = {"Rabbit" : 1, "Sheep" : 6, "Pig" : 12, "Cow" : 24, "Horse" : 48}    
        self.player = active

    # Przyciski muszą być
    def exchange(self, first_type, second_type):
        player_animals = self.player.get_animals()
        if first_type not in player_animals.keys():
            print(f"You don't have {first_type}!")
            return 0

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
            if first_type not in player_animals.keys():
                print(f"You don't have {first_type}")
                return 0
            else:
                self.player.remove_animal(first_type)
                for i in range(first_val / price):
                    self.player.place_animal(second_type)

    def buy_field(self):
        chosen_field = self.player.choose_field() 

        while any(chosen_field in player.fields for player in players):    # Sprawdza czy pole już do kogoś należy
            print("Field is already owned")
            chosen_field = self.player.choose_field()
        
        price = chosen_field.value
        if self.player.check_animals["Rabbit"] < price: # Sprawdza czy gracz dysponuje odpowiednią liczbą królików do zakupu
            print("You have too little rabbits")
            return 0
        else:
            for i in range(price):
                self.player.remove_animal("Rabbit")
            self.player.fields.append(chosen_field)

    def upgrade_field(self):
        chosen_field = self.player.choose_field()
        while chosen_field not in self.player.fields:
            print("It's not your field")
            chosen_field = self.player.choose_field()
        if chosen_field.value == 1:
            price = 4
        elif chosen_field.value == 2:
            price = 10
        elif chosen_field.value == 4:
            price = 18
        else:
            print("You can't upgrade further!")
        if self.player.check_animals["Rabbit"] < price:
            print("You have too little rabbits")
            return 0
        else:
            for i in range(price):
                    self.player.remove_animal("Rabbit")
            chosen_field.upgrade()



def choose_field():
    chosen_field = Field(1) # WIP, domyślnie ma klikać
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

def choose_animal():    # Do GUI, wybiera zwierzę ze schowka
    pass    # switch... case...

player = Player(0)
