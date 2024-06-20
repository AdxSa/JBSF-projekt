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
        self.clipboard = {"Rabbit" : 0, "Sheep" : 0, "Pig" : 0, "Cow" : 0, "Horse" : 0}
    

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

    def place_animal(self, animal_type):    # Jest w GUI, jeśli działa to można zlikwidować
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

    def choose_field(self): # Jest w GUI, jeśli działa to można zlikwidować
        pass

    def relocate_to_clipboard(self):    # Jest w GUI, jeśli działa to można zlikwidować
        chosen_field = self.choose_field()    
        while chosen_field not in self.fields:
            chosen_field = self.choose_field()
        animal = chosen_field.animals[0]
        for field in animal.fields:
            field.animals.pop()
            field.check_capacity()
        animals_clipboard[animal.type] += 1
        del animal

    def relocate_to_board(self):    # Jest w GUI, jeśli działa to można zlikwidować
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
        return {name : number}
    
    def check_capacity(self):
        actual_capacity = 0
        for animal in self.animals:
            actual_capacity += animal.space_needed
        self.capacity = 6 - actual_capacity
    
class Marketplace:  # Pamięta aktywnego gracza i listę graczy
    def __init__(self) -> None:
        self.buy_prices = {"Rabbit" : 1, "Sheep" : 6, "Pig" : 12, "Cow" : 24, "Horse" : 48}    

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
            player.clipboard[second_type]

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
        if player.clipboard["Rabbit"] < price: # Sprawdza czy gracz dysponuje odpowiednią liczbą królików do zakupu
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
            print("Masz za malo krolikow")
            return 0
        else:
            player.clipboard["Rabbit"] -= price
            chosen_field.upgrade()
            return 1



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
