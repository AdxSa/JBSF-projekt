from farmer import Player, Field, Marketplace
from collections import Counter
import random

first_player = Player(0)
second_player = Player(1)

class GUI:  # Do dołączenia 
    def __init__(self) -> None:
        self.fields = []
        for y in range(8):
            for x in range(8):
                if x > 1 and x < 6 and y > 1 and y < 6:
                    self.fields.append(Field(1, x, y))
                elif x in [0, 7] or y in [0, 7]:
                    self.fields.append(Field(4, x, y))
                else:
                    self.fields.append(Field(2, x, y))

    def roll_animal_dice(self, player):
        if player.animal_rolled:
            self.dice_roll_done_inform.set("You have already rolled the dice!")
        else:
            roll = player.roll_animal_dice()
            animals = player.get_animals()
            predator = [1, 1, 1, 2, 2, 4]
            new_animals = {}
            if roll[0] == roll[1]:
                only_roll = roll[0]

                if only_roll == "Fox":
                    self.predator_attack(random.choice(predator), "Fox")
                    self.predator_attack(random.choice(predator), "Fox")

                elif only_roll == "Wolf":
                    self.predator_attack(random.choice(predator), "Wolf")
                    self.predator_attack(random.choice(predator), "Wolf")

                else:
                    animals[only_roll] += (animals[only_roll] + 2) // 2
            else:
                if "Fox" in roll:
                    self.predator_attack(random.choice(predator), "Fox")

                if "Wolf" in roll:
                    self.predator_attack(random.choice(predator), "Wolf")

                for animal in roll:
                    if animal in ["Fox", "Wolf"]:
                        continue

                    else:
                        if animals.get(animal) > 0:
                            new_animals[animal] = (animals[animal] + 1) // 2    

                for animal_type in new_animals.keys():
                    for animal in new_animals[animal_type]:
                        player.place_animal(animal_type)    # Zamiast tego może dodawać do animals_clipboard    

                # animals_clipboard = dict(Counter(animals_clipboard) + Counter(new_animals))   # Jeszcze niezdefniowane wyżej           

    def predator_attack(self, val, predator):
        for field in self.fields:
            if field.value == val:
                while field.capacity != 6:
                    if predator == "Wolf":
                        if field.animals[0].space_needed != 1:
                            animal = field.animals.pop()
                            del animal
                            field.check_capacity()
                    else:
                        if field.animals[0].space_needed == 1:
                            animal = field.animals.pop()
                            del animal
                            field.check_capacity()

    def choose_field(self):
        pass    # Grafika



a = GUI()
print(a.fields[0].coords)
print(a.fields[63].value)
print(a.fields[17].value)
print(a.fields[12].coords)
print(a.fields[0].show_field())

