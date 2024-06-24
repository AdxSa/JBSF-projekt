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
        """_summary_

        Args:
            field (_type_): _description_
        """
        self.fields.append(field)


class Field:
    """Klasa Field przechowuje zwierzęta, swoich sąsiadów, swoją wartość i koordynaty. Na polach
    znajdują się zwierzęta i tylko na nich mogą się rozmnażać.
    """
    def __init__(self, value, x, y) -> None:
        """Inicjalizacja klasy Field

        Args:
            value (int): wartość pola
            x (int): kolumna, w której znajduje się pole
            y (int): wiersz, w którym znajduje się pole
        """
        self.value = value
        self.capacity = 6
        self.animals = []
        self.x = x
        self.y = y
        self.neighbours = []

    def __repr__(self):
        return f"Field({self.x},{self.y})"

    def upgrade(self):
        """Metoda upgrade podnosi poziom pola o jeden
        """
        field_values = [1, 2, 4, 5]
        self.value = field_values[field_values.index(self.value) + 1]

    # Chyba nie ma jej nigdzie...

    # def show_field(self):
    #     if self.animals == []:
    #         return "No animals on that field"
    #     else:
    #         name = self.animals[0].type
    #         number = len(self.animals)
    #     return {name: number}

    def check_capacity(self):
        """Metoda sprawdza i aktualizuje wolne miejsca pola na zwierzęta 
        """
        actual_capacity = 0
        for animal in self.animals:
            actual_capacity += animal.space_needed
        self.capacity = 6 - actual_capacity


class Marketplace:  
    """Klasa Marketplace znajduje się wewnątrz GUI jako "sklep", w którym gracze za króliki kupują pola,
    inne zwierzęta i ulepszają pola.
    """
    def __init__(self) -> None:
        """Słownik zwierzę : cena
        """
        self.buy_prices = {"Rabbit": 1, "Sheep": 6, "Pig": 12, "Cow": 24, "Horse": 48}

    def exchange(self, first_type, second_type, player):
        """Metoda zarządzająca wymianą zwierząt. 

        Args:
            first_type (String): zwierzę, które gracz chce wymienić
            second_type (String): zwierzę, które gracz chce otrzymać
            player (Player): aktywny gracz (GUI)

        Returns:
            bool: Zwraca sukces/porażka
        """

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
        """Funkcja sprawdza czy gracz ma odpowiednie zasoby do zakupu pola
        i jeżeli tak, modyfikują liczbę królików w schowku
        Args:
            chosen_field (Field): wybrane w GUI pole
            player (Player): aktywny gracz (GUI)

        Returns:
            bool: Zwraca sukces/porażka
        """
        price = chosen_field.value
        if player.clipboard["Rabbit"] < price:  # Sprawdza czy gracz dysponuje odpowiednią liczbą królików do zakupu
            print("Masz za malo krolikow w schowku")
            return 0
        else:
            player.clipboard["Rabbit"] -= price
            player.fields.append(chosen_field)
            return 1

    def upgrade_field(self, chosen_field, player):
        """Funkcja podwyższa poziom pola o jeden

        Args:
            chosen_field (Field): wybrane w GUI pole
            player (Player): aktywny gracz (GUI)

        Returns:
            bool: Zwraca sukces/porażka
        """
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



