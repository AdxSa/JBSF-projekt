import tkinter as tk
from random import choice
from collections import Counter
from Player import Player
from farmer import Field, Animal, Marketplace
from PIL import Image, ImageTk
from bigdict import game_to_normal_coords_dict, normal_to_game_coords_dict

TEMP_PLAYER_1 = Player('red', (0, 0, 0), 'TEMP_PLAYER_1')
TEMP_PLAYER_2 = Player('green', (2, 0, 0), 'TEMP_PLAYER_2')
TEMP_PLAYERS = [TEMP_PLAYER_1, TEMP_PLAYER_2]


class GUI:
    """Klasa GUI obsługuje całą warstwę graficzną gry. Oprócz tego ma w sobie metody sterujące całą rozgrywką, gdyż każda z nich korzysta 
    z warstwy graficznej. Przechowuje graczy, więc zarazem ich pola i zwierzęta. Poza tym wszystkie przyciski i obsługuje ich działanie. 
    """
    chessboard_colours = ['black', 'white']
    error_code = 0

    def __init__(self, players):
        """Inicjalizacja klasy GUI. Tworzy całą warstwę graficzną gry. Dba o poprawne wyświetlanie przycisków i ilustracji.

        Args:
            players (list): lista obiektów typu Player - graczy
        """
        self.players = players
        self.current_player = players[0]
        self.current_player_number = 0
        self.root = tk.Tk()

        self.player_info = tk.StringVar()
        self.player_info.set(f"Tura gracza: {self.current_player.name}")
        self.info = tk.StringVar()
        self.info.set('')
        self.err = tk.StringVar()
        self.err.set('')
        self.player_info_label = tk.Label(self.root, textvariable=self.player_info, font=('Comic sans MS', 20))
        self.info_label = tk.Label(self.root, textvariable=self.info, font=('Comic sans MS', 20))
        self.err_label = tk.Label(self.root, textvariable=self.err, font=('Comic sans MS', 20), fg='red')
        self.player_info_label.pack()
        self.info_label.pack()
        self.err_label.pack()

        self.border_list = dict()
        self.on_off = False

        self.root.geometry("1920x1080")
        self.root.resizable(False, False)
        self.root.title("Jeszcze Lepszy Super Farmer")

        self.end_turn_bt = tk.Button(self.root, text="Koniec tury", font=('Comic sans MS', 16),
                                     command=lambda: self.next_player())
        self.end_turn_bt.place(x=1700, y=980)

        # Przycisk Rzuć kostką:
        self.frame = tk.Frame(self.root, width=310, height=200)
        self.frame.pack_propagate(False)
        self.frame.place(x=1600, y=20)

        self.dice_roll_bt = tk.Button(self.frame, text="Rzuć kostką", font=('Comic sans MS', 16),
                                      command=lambda: self.roll_dice())
        self.dice_roll_bt.pack()

        self.dice_roll_result = tk.StringVar()
        self.dice_roll_result.set("Nie rzucono kostką")
        self.dice_roll_result_label = tk.Label(self.frame, textvariable=self.dice_roll_result, font=('Comic sans MS', 16))
        self.dice_roll_result_label.pack()

        self.dice_roll_done_inform = tk.StringVar()
        self.dice_roll_done_inform.set('')
        self.dice_roll_done_inform_label = tk.Label(self.frame, textvariable=self.dice_roll_done_inform,
                                                    font=('Comic sans MS', 16))
        self.dice_roll_done_inform_label.pack()

        # Przyciski pod planszą z funkcjonalnością choose_pawn!:
        self.pixel = tk.PhotoImage(width=1, height=1)
        self.chessboard = tk.Frame(width=400, height=400)
        self.board = [['' for row in range(8)] for col in range(8)]
        from itertools import cycle
        for col in range(8):
            color = cycle(self.chessboard_colours[::-1] if not col % 2 else self.chessboard_colours)
            for row in range(8):
                self.board[row][col] = tk.Button(self.chessboard, bg=next(color), image=self.pixel, width=50, height=50,
                                                 text=f"",
                                                 compound='center', font=('Comic sans MS', 12),
                                                 command=lambda i=col, j=row:
                                                 self.choose_pawn(j, i))
                # text = f"tile{normal_to_game_coords_dict[(col, row)]}" aby sprawdzić czy na pewno dobra numeracja
                self.board[row][col].grid(row=7 - row, column=col)
        self.chessboard.place(x=100, y=200)

        # inne:

        self.buttonframe = tk.Frame(self.root)
        self.buttonframe.columnconfigure(0, weight=1)
        self.buttonframe.columnconfigure(1, weight=1)

        # Przycisk Porusz się pionkiem
        self.move_pawn_bt = tk.Button(self.buttonframe, text="Porusz się pionkiem", font=('Comic sans MS', 16),
                                      command=lambda: self.move_pawn())
        self.move_pawn_bt.grid(row=0, column=1, sticky=tk.W + tk.E)

        # Przycisk Stwórz pionek:
        self.create_pawn_bt = tk.Button(self.buttonframe, text="Stwórz pionek", font=('Comic sans MS', 16),
                                        command=lambda: self.create_pawn())
        self.create_pawn_bt.grid(row=0, column=0, sticky=tk.W + tk.E)

        # Przycisk Wejdź poziom wyżej:
        self.upgrade_pawn_bt = tk.Button(self.buttonframe, text="Wejdź poziom wyżej", font=('Comic sans MS', 16),
                                         command=lambda: self.upgrade_pawn())
        self.upgrade_pawn_bt.grid(row=1, column=0, sticky=tk.W + tk.E)

        # Przycisk Zejdź poziom niżej
        self.degrade_pawn_bt = tk.Button(self.buttonframe, text="Zejdź poziom niżej", font=('Comic sans MS', 16),
                                         command=lambda: self.degrade_pawn())
        self.degrade_pawn_bt.grid(row=1, column=1, sticky=tk.W + tk.E)

        self.buttonframe.place(x=100, y=670)

        # Grzyb
        from gif import AnimatedGif
        AnimatedGif(self.root, "fungi.gif", x=1380, y=350)

        # FARMER (nie tylko przyciski)
        self.fields = []
        for y in range(8):
            row = []
            for x in range(8):
                if 1 < x < 6 and 1 < y < 6:
                    row.append(Field(1, x, y))
                elif x in [0, 7] or y in [0, 7]:
                    row.append(Field(4, x, y))
                else:
                    row.append(Field(2, x, y))
            self.fields.append(row)

        starting_fields = [self.fields[0][0], self.fields[7][7], self.fields[0][7], self.fields[7][0]]
        num_of_field = 0

        for player in self.players:
            player.fields.append(starting_fields[num_of_field])
            num_of_field += 1

        self.selected_field_var = tk.StringVar()

        self.setup_neighbours()
        self.market = Marketplace()

        #  przyciski do farmera
        # plansza farmera
        self.farmerboard = tk.Frame(width=400, height=400, highlightthickness=1, highlightbackground='black')
        self.farboard = [['' for row in range(8)] for col in range(8)]  # macierz guzików
        for col in range(8):
            for row in range(8):
                self.farboard[row][col] = tk.Button(self.farmerboard, image=self.pixel, width=50, height=50,
                                                    text=f"{self.fields[row][col].value}",
                                                    compound='center', font=('Comic sans MS', 12),
                                                    command=lambda x=col, y=row: self.set_selected_field(x, y))
                self.farboard[row][col].grid(row=7 - row, column=col)
        self.farmerboard.place(x=700, y=200)

        for player in self.players:
            field = player.fields[0]
            x = field.x
            y = field.y
            self.farboard[y][x].configure(bg=player.colour)

        # clipboard
        self.clipboard = tk.Frame(self.root, highlightthickness=1, highlightbackground='black')
        self.clipboard.columnconfigure(0, weight=1)

        self.animal_type_to_animal_tag = {'Rabbit' : '🐰', 'Sheep' : '🐑', 'Pig' : '🐷', 'Cow' : '🐮', 'Horse' : '🐴', 'Fox' : '🦊', 'Wolf' : '🐺'}

        self.rabbit_bt = tk.Button(self.clipboard, text=f'🐰 {self.current_player.clipboard['Rabbit']}', fg='grey', image=self.pixel, width=140, height=80, compound='center',
                                   font=('Comic sans MS', 40), command=lambda: self.relocate_to_board("Rabbit"))
        self.rabbit_bt.grid(row=0, column=1)

        self.sheep_bt = tk.Button(self.clipboard, text=f'🐑 {self.current_player.clipboard['Sheep']}', fg='black', image=self.pixel, width=140, height=80, compound='center',
                                  font=('Comic sans MS', 40), command=lambda: self.relocate_to_board("Sheep"))
        self.sheep_bt.grid(row=1, column=1)

        self.pig_bt = tk.Button(self.clipboard, text=f'🐷 {self.current_player.clipboard['Pig']}', fg='pink', image=self.pixel, width=140, height=80, compound='center',
                                font=('Comic sans MS', 40), command=lambda: self.relocate_to_board("Pig"))
        self.pig_bt.grid(row=2, column=1)

        self.cow_bt = tk.Button(self.clipboard, text=f'🐮 {self.current_player.clipboard['Cow']}', fg='#df546c', image=self.pixel, width=140, height=80, compound='center',
                                font=('Comic sans MS', 40), command=lambda: self.relocate_to_board("Cow"))
        self.cow_bt.grid(row=3, column=1)

        self.horse_bt = tk.Button(self.clipboard, text=f'🐴 {self.current_player.clipboard['Horse']}', fg='brown', image=self.pixel, width=140, height=80, compound='center',
                                  font=('Comic sans MS', 40), command=lambda: self.relocate_to_board("Horse"))
        self.horse_bt.grid(row=4, column=1)

        self.clipboard_mode_bt = tk.Button(self.clipboard, image=self.pixel, bg='red', width=140, height=80, compound='center',
                                           font=('Comic sans MS', 16), command=lambda: self.unlock_clipboard_mode())
        self.clipboard_mode_bt.grid(row=5, column=1)

        self.clipboard.place(x=1200, y=200)

        # marketplace
        self.marketplace = tk.Frame(self.root)
        self.rabbit_label = tk.Label(self.marketplace, text='🐰', fg='grey', font=('Comic sans MS', 80))
        self.rabbit_label.grid(row=0, column=0)

        self.sheep_label = tk.Label(self.marketplace, text='🐑', fg='black', font=('Comic sans MS', 80))
        self.sheep_label.grid(row=0, column=2)

        self.pig_label = tk.Label(self.marketplace, text='🐷', fg='pink', font=('Comic sans MS', 80))
        self.pig_label.grid(row=0, column=4)

        self.cow_label = tk.Label(self.marketplace, text='🐮', fg='#df546c', font=('Comic sans MS', 80))
        self.cow_label.grid(row=0, column=6)

        self.horse_label = tk.Label(self.marketplace, text='🐴', fg='brown', font=('Comic sans MS', 80))
        self.horse_label.grid(row=0, column=8)
        # rabbit-sheep buttons
        self.rabbit_sheep_bt_frame = tk.Frame(self.marketplace)
        self.rabbit_to_sheep_bt = tk.Button(self.rabbit_sheep_bt_frame, text='🡆', image=self.pixel, width=40,
                                            height=40, compound='center',
                                            font=('Comic sans MS', 24),
                                            command=lambda: self.exchange_animals("Rabbit", "Sheep"))
        self.rabbit_to_sheep_bt.grid(row=0, column=0)
        tk.Label(self.rabbit_sheep_bt_frame, text='6 : 1', font=('Arial', 16)).grid(row=1, column=0)
        self.sheep_to_rabbit_bt = tk.Button(self.rabbit_sheep_bt_frame, text='🡄', image=self.pixel, width=40,
                                            height=40, compound='center',
                                            font=('Comic sans MS', 24),
                                            command=lambda: self.exchange_animals("Sheep", "Rabbit"))
        self.sheep_to_rabbit_bt.grid(row=2, column=0)
        self.rabbit_sheep_bt_frame.grid(row=0, column=1)
        # sheep-pig buttons
        self.sheep_pig_bt_frame = tk.Frame(self.marketplace)
        self.sheep_to_pig_bt = tk.Button(self.sheep_pig_bt_frame, text='🡆', image=self.pixel, width=40, height=40,
                                         compound='center',
                                         font=('Comic sans MS', 24), command=lambda: self.exchange_animals("Sheep", "Pig"))
        tk.Label(self.sheep_pig_bt_frame, text='2 : 1', font=('Arial', 16)).grid(row=1, column=0)
        self.sheep_to_pig_bt.grid(row=0, column=0)
        self.pig_to_sheep_bt = tk.Button(self.sheep_pig_bt_frame, text='🡄', image=self.pixel, width=40,
                                         height=40, compound='center',
                                         font=('Comic sans MS', 24), command=lambda: self.exchange_animals("Pig", "Sheep"))
        self.pig_to_sheep_bt.grid(row=2, column=0)
        self.sheep_pig_bt_frame.grid(row=0, column=3)
        # pig-cow buttons
        self.pig_cow_bt_frame = tk.Frame(self.marketplace)
        self.pig_to_cow_bt = tk.Button(self.pig_cow_bt_frame, text='🡆', image=self.pixel, width=40, height=40,
                                       compound='center',
                                       font=('Comic sans MS', 24), command=lambda: self.exchange_animals("Pig", "Cow"))
        self.pig_to_cow_bt.grid(row=0, column=0)
        tk.Label(self.pig_cow_bt_frame, text='2 : 1', font=('Arial', 16)).grid(row=1, column=0)
        self.cow_to_pig_bt = tk.Button(self.pig_cow_bt_frame, text='🡄', image=self.pixel, width=40,
                                       height=40, compound='center',
                                       font=('Comic sans MS', 24), command=lambda: self.exchange_animals("Cow", "Pig"))
        self.cow_to_pig_bt.grid(row=2, column=0)
        self.pig_cow_bt_frame.grid(row=0, column=5)
        # cow-horse buttons
        self.cow_horse_bt_frame = tk.Frame(self.marketplace)
        self.cow_to_horse_bt = tk.Button(self.cow_horse_bt_frame, text='🡆', image=self.pixel, width=40, height=40,
                                         compound='center',
                                         font=('Comic sans MS', 24), command=lambda: self.exchange_animals("Cow", "Horse"))
        self.cow_to_horse_bt.grid(row=0, column=0)
        tk.Label(self.cow_horse_bt_frame, text='2 : 1', font=('Arial', 16)).grid(row=1, column=0)
        self.horse_to_cow_bt = tk.Button(self.cow_horse_bt_frame, text='🡄', image=self.pixel, width=40,
                                         height=40, compound='center',
                                         font=('Comic sans MS', 24), command=lambda: self.exchange_animals("Horse", "Cow"))
        self.horse_to_cow_bt.grid(row=2, column=0)
        self.cow_horse_bt_frame.grid(row=0, column=7)

        # pole pole łyse pole
        # self.polepole = tk.PhotoImage(file='polepole.png')
        self.pola_bt_frame = tk.Frame(self.marketplace)
        self.buy_field_bt = tk.Button(self.pola_bt_frame, text='Kup pole', font=('Comic sans MS', 20), command=self.buy_field)
        self.buy_field_bt.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        self.upgrade_field_bt = tk.Button(self.pola_bt_frame, text='Ulepsz pole', font=('Comic sans MS', 20),
                                          command=self.upgrade_field)
        self.upgrade_field_bt.grid(row=1, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        self.pola_bt_frame.grid(row=0, column=9, padx=50)

        self.marketplace.place(x=100, y=800)

    def play(self):
        """Funkcja uruchamiająca całą grę w głównej pętli.
        """
        self.root.mainloop()

    def next_player(self):
        """Funkcja obsługująca przejście do kolejnej tury. Czyści schowek i ustala atrybuty typu bool na właściwą wartość False.
        """
        self.current_player.rolled = False
        self.current_player.rolled_animal = False  # Farmer
        self.current_player.chosen_pawn = None
        self.current_player.to_clipboard = False  # Farmer
        self.clipboard_mode_bt.configure(bg='red')
        self.current_player_number = self.current_player_number + 1
        self.current_player = self.players[self.current_player_number % len(self.players)]
        self.player_info.set(f"Tura gracza: {self.current_player.name}")
        self.info.set('')
        self.err.set('')
        error_code = 0
        self.dice_roll_done_inform.set('')
        self.dice_roll_result.set('Nie rzucono kostką')
        self.current_player.clipboard = {"Rabbit": 0, "Sheep": 0, "Pig": 0, "Cow": 0, "Horse": 0}
        self.rabbit_bt.configure(text=f'🐰 {int(self.current_player.clipboard['Rabbit'])}')
        self.sheep_bt.configure(text=f'🐑 {int(self.current_player.clipboard['Sheep'])}')
        self.pig_bt.configure(text=f'🐷 {int(self.current_player.clipboard['Pig'])}')
        self.cow_bt.configure(text=f'🐮 {int(self.current_player.clipboard['Cow'])}')
        self.horse_bt.configure(text=f'🐴 {int(self.current_player.clipboard['Horse'])}')

    def roll_dice(self):
        """Metoda obsługująca rzut kośćmi. Do chińczyka i do farmera. Wywołuje ataki drapieżników i obsługuje rozmnażanie zwierząt
        na polach. Korzysta z metod klasy Player: roll_animal_dice() oraz get_animals().
        """
        if self.current_player.rolled:
            self.dice_roll_done_inform.set("Już rzuciłeś kostką w tej turze")
        else:
            roll = self.current_player.roll_animal_dice()
            animals = self.current_player.get_animals()
            predator = [1, 1, 1, 2, 2, 4]
            new_animals = dict()
            if roll[0] == roll[1]:
                only_roll = roll[0]

                if only_roll == "Fox":
                    self.predator_attack(choice(predator), "Fox")
                    self.predator_attack(choice(predator), "Fox")

                elif only_roll == "Wolf":
                    self.predator_attack(choice(predator), "Wolf")
                    self.predator_attack(choice(predator), "Wolf")

                else:
                    new_animals[only_roll] = (animals[only_roll] + 2) // 2
            else:
                if "Fox" in roll:
                    self.predator_attack(choice(predator), "Fox")

                if "Wolf" in roll:
                    self.predator_attack(choice(predator), "Wolf")

                for animal in roll:
                    if animal in ["Fox", "Wolf"]:
                        continue

                    else:
                        if animals[animal] > 0:
                            new_animals[animal] = (animals[animal] + 1) // 2


            tlist = [animal for animal in self.current_player.clipboard.keys() if self.current_player.clipboard[animal] == 0]
            self.current_player.clipboard = dict(Counter(self.current_player.clipboard) + Counter(new_animals))
            self.current_player.roll_dice()
            self.dice_roll_result.set(f'Wynik rzutu kostką:\n'
                                      f'Chińczyk: {self.current_player.current_roll}\n'
                                      f'Farmer: {self.animal_type_to_animal_tag[roll[0]]} {self.animal_type_to_animal_tag[roll[1]]}')
            for animal in tlist:
                self.current_player.clipboard[animal] = 0
            self.rabbit_bt.configure(text=f'🐰 {int(self.current_player.clipboard['Rabbit'])}')
            self.sheep_bt.configure(text=f'🐑 {int(self.current_player.clipboard['Sheep'])}')
            self.pig_bt.configure(text=f'🐷 {int(self.current_player.clipboard['Pig'])}')
            self.cow_bt.configure(text=f'🐮 {int(self.current_player.clipboard['Cow'])}')
            self.horse_bt.configure(text=f'🐴 {int(self.current_player.clipboard['Horse'])}')
            if self.error_code == 1:
                self.err.set('')

    def create_pawn(self):
        """Metoda obsługująca powstawanie nowych pionków. Korzysta z metody create_pawn() klasy Player.
        """
        try:
            self.current_player.create_pawn()
            pawns_on_spawn_tile = ''
            i = 0
            for pawn in self.current_player.pawns:
                if pawn.coords == self.current_player.pawn_spawn_coords:
                    i += 1
                    pawns_on_spawn_tile += pawn.tag
                    if i == 2:
                        pawns_on_spawn_tile += '\n'
            # zamieniamy współrzędne spawn_coords wybranego gracza na współrzędne klasyczne szachownicy,
            # aby pobrać dobry index od self.board
            (self.board[game_to_normal_coords_dict[self.current_player.pawn_spawn_coords][0]]
             [game_to_normal_coords_dict[self.current_player.pawn_spawn_coords][1]]
             .config(text=f'{pawns_on_spawn_tile}', fg=self.current_player.colour))

            # zbijanie jak na polu startowym stoi pionek innego gracza
            for player in self.players:
                if player != self.current_player:
                    for pawn in player.pawns:
                        if (game_to_normal_coords_dict[pawn.coords] ==
                                game_to_normal_coords_dict[self.current_player.pawn_spawn_coords]):
                            player.pawns_id.remove(int(pawn.id))
                            player.pawns.remove(pawn)
                            del pawn

            self.info.set('Utworzono nowy pionek!')
            self.rabbit_bt.configure(text=f'🐰 {int(self.current_player.clipboard['Rabbit'])}')
            self.sheep_bt.configure(text=f'🐑 {int(self.current_player.clipboard['Sheep'])}')
            self.pig_bt.configure(text=f'🐷 {int(self.current_player.clipboard['Pig'])}')
            self.cow_bt.configure(text=f'🐮 {int(self.current_player.clipboard['Cow'])}')
            self.horse_bt.configure(text=f'🐴 {int(self.current_player.clipboard['Horse'])}')
        except:
            self.err.set('Nie możesz stworzyć kolejnego pionka')

    def choose_pawn(self, row, col):
        """Metoda obsługująca wybór pionka

        Args:
            row (int): rząd, w którym znajduje się pionek
            col (int): kolumna, w której znajduje się pionek
        """
        tile_coords = normal_to_game_coords_dict[(row, col)]
        t_pawn = None
        pawn_was_chosen = False
        for pawn in self.current_player.pawns:
            if pawn.is_in_destination_square and (pawn.coords[0] % 4, pawn.coords[1], pawn.coords[2]) == tile_coords:
                t_pawn = pawn
            elif (pawn.coords[0] % 4, pawn.coords[1], pawn.coords[2]) == tile_coords:
                self.info.set(f'Wybrano pionek numer {pawn.id}')
                self.current_player.choose_pawn(pawn.id)
                pawn_was_chosen = True
                if self.error_code == 2:
                    self.err.set('')
                break
        if t_pawn is not None and not pawn_was_chosen:
            self.info.set(f'Wybrano pionek numer {t_pawn.id}')
            self.current_player.choose_pawn(t_pawn.id)

    def move_pawn(self):  # porusza wybranym pionkiem oraz zmienia grafikę na odpowiednich polach
        """Porusza wybranym pionkiem oraz zmienia grafikę na odpowiednich polach. Uwzględnia zbijanie, grafikę i 
        sprawdza warunki zwycięstwa.
        """
        if self.current_player.rolled and self.current_player.chosen_pawn is not None:
            current_coords = self.current_player.chosen_pawn.coords
            self.current_player.move_chosen_pawn()
            pawns_on_current_tile = ''
            pawns_on_next_tile = ''
            i = 0
            k = 0
            if self.current_player.chosen_pawn.is_in_destination_square:
                self.current_player.chosen_pawn.tag = ''
            for pawn in self.current_player.pawns:
                if pawn.coords == current_coords:
                    i += 1
                    pawns_on_current_tile += pawn.tag
                    if i == 2:
                        pawns_on_current_tile += '\n'
                if pawn.coords == self.current_player.chosen_pawn.coords:
                    k += 1
                    pawns_on_next_tile += pawn.tag
                    if k == 2:
                        pawns_on_next_tile += '\n'
            # zmieniamy wspólrzędne wybranego pionka na klasyczne aby pobrać odpowiedni index od self.board
            # następnie usuwamy wizerunek pionka z danego pola po czym przesówamy pionek i
            # tworzymy wizerunek na miejscu w którym znajduje się pionek w sposób odwrotny
            (self.board[game_to_normal_coords_dict[current_coords][0]]
             [game_to_normal_coords_dict[current_coords][1]]
             .config(text=f'{pawns_on_current_tile}', fg=self.current_player.colour))

            (self.board[game_to_normal_coords_dict[self.current_player.chosen_pawn.coords][0]]
             [game_to_normal_coords_dict[self.current_player.chosen_pawn.coords][1]]
             .config(text=f'{pawns_on_next_tile}', fg=self.current_player.colour))

            # potencjalnie kolorowanie pól na które ostatecznie dotarły już pionki

            if self.current_player.chosen_pawn.is_in_destination_square:
                border = Image.open(f'{self.current_player.colour}.png')
                border = border.resize((50, 50))
                self.border_list[(self.current_player.colour, self.current_player.chosen_pawn.id)] = ImageTk.PhotoImage(border)
                (self.board[game_to_normal_coords_dict[self.current_player.chosen_pawn.coords][0]]
                [game_to_normal_coords_dict[self.current_player.chosen_pawn.coords][1]]
                 .config(image=self.border_list[(self.current_player.colour, self.current_player.chosen_pawn.id)]))

            # zbijanie
            for player in self.players:
                if player != self.current_player:
                    for pawn in player.pawns:
                        if ((game_to_normal_coords_dict[pawn.coords] ==
                             game_to_normal_coords_dict[self.current_player.chosen_pawn.coords])
                                and not pawn.is_in_destination_square):
                            player.pawns_id.remove(int(pawn.id))
                            player.pawns.remove(pawn)
                            # print(player.pawns)
                            del pawn

            # sprawdzanie win condition
            if self.current_player.chosen_pawn.is_in_destination_square:
                if len({pawn.coords for pawn in self.current_player.pawns if pawn.is_in_destination_square}) == 4:
                    self.end_game()

        elif self.current_player.chosen_pawn is not None:
            self.err.set('Najpierw rzuć kostką')
            self.error_code = 1
        else:
            self.err.set('Wybierz pionek')
            self.error_code = 2


    def upgrade_pawn(self):
        """Metoda obsługuje graficznie zejście pionka do wyższego rzędu i sprawdza czy gracz wygrał.
        """
        if self.current_player.chosen_pawn is None:
            self.err.set('Wybierz pionek')
            self.error_code = 2
        else:
            current_coords = self.current_player.chosen_pawn.coords
            self.current_player.upgrade_chosen_pawn()
            self.rabbit_bt.configure(text=f'🐰 {int(self.current_player.clipboard['Rabbit'])}')
            self.sheep_bt.configure(text=f'🐑 {int(self.current_player.clipboard['Sheep'])}')
            self.pig_bt.configure(text=f'🐷 {int(self.current_player.clipboard['Pig'])}')
            self.cow_bt.configure(text=f'🐮 {int(self.current_player.clipboard['Cow'])}')
            self.horse_bt.configure(text=f'🐴 {int(self.current_player.clipboard['Horse'])}')
            pawns_on_current_tile = ''
            pawns_on_next_tile = ''
            i = 0
            k = 0
            for pawn in self.current_player.pawns:
                if pawn.coords == current_coords:
                    i += 1
                    pawns_on_current_tile += pawn.tag
                    if i == 2:
                        pawns_on_current_tile += '\n'
                if pawn.coords == self.current_player.chosen_pawn.coords:
                    k += 1
                    pawns_on_next_tile += pawn.tag
                    if k == 2:
                        pawns_on_next_tile += '\n'
            # zmieniamy wspólrzędne wybranego pionka na klasyczne aby pobrać odpowiedni index od self.board
            # następnie usuwamy wizerunek pionka z danego pola po czym przesówamy pionek i
            # tworzymy wizerunek na miejscu w którym znajduje się pionek w sposób odwrotny
            (self.board[game_to_normal_coords_dict[current_coords][0]]
             [game_to_normal_coords_dict[current_coords][1]]
             .config(text=f'{pawns_on_current_tile}', fg=self.current_player.colour))

            (self.board[game_to_normal_coords_dict[self.current_player.chosen_pawn.coords][0]]
             [game_to_normal_coords_dict[self.current_player.chosen_pawn.coords][1]]
             .config(text=f'{pawns_on_next_tile}', fg=self.current_player.colour))

            if self.current_player.chosen_pawn.is_in_destination_square:
                if all(not pawn.is_in_destination_square or pawn.coords != current_coords for pawn in self.current_player.pawns):
                        (self.board[game_to_normal_coords_dict[current_coords][0]]
                        [game_to_normal_coords_dict[current_coords][1]]
                        .config(image=self.pixel))
                (self.board[game_to_normal_coords_dict[self.current_player.chosen_pawn.coords][0]]
                [game_to_normal_coords_dict[self.current_player.chosen_pawn.coords][1]]
                 .config(image=self.border_list[(self.current_player.colour, self.current_player.chosen_pawn.id)]))

            # zbijanie
            for player in self.players:
                if player != self.current_player:
                    for pawn in player.pawns:
                        if (game_to_normal_coords_dict[pawn.coords] ==
                                game_to_normal_coords_dict[self.current_player.chosen_pawn.coords]):
                            player.pawns_id.remove(int(pawn.id))
                            player.pawns.remove(pawn)
                            # print(player.pawns)
                            del pawn

            # sprawdzanie win condition
            if self.current_player.chosen_pawn.is_in_destination_square:
                if len({pawn.coords for pawn in self.current_player.pawns if pawn.is_in_destination_square}) == 4:
                    self.end_game()

    def degrade_pawn(self):
        """Metoda obsługuje graficznie zejście pionka do niższego rzędu i sprawdza czy gracz wygrał.
        """
        if self.current_player.chosen_pawn is None:
            self.err.set('Wybierz pionek')
            self.error_code = 2
        else:
            current_coords = self.current_player.chosen_pawn.coords
            self.current_player.degrade_chosen_pawn()
            pawns_on_current_tile = ''
            pawns_on_next_tile = ''
            i = 0
            k = 0
            for pawn in self.current_player.pawns:
                if pawn.coords == current_coords:
                    i += 1
                    pawns_on_current_tile += pawn.tag
                    if i == 2:
                        pawns_on_current_tile += '\n'
                if pawn.coords == self.current_player.chosen_pawn.coords:
                    k += 1
                    pawns_on_next_tile += pawn.tag
                    if k == 2:
                        pawns_on_next_tile += '\n'
            # zmieniamy wspólrzędne wybranego pionka na klasyczne aby pobrać odpowiedni index od self.board
            # następnie usuwamy wizerunek pionka z danego pola po czym przesówamy pionek i
            # tworzymy wizerunek na miejscu w którym znajduje się pionek w sposób odwrotny
            (self.board[game_to_normal_coords_dict[current_coords][0]]
             [game_to_normal_coords_dict[current_coords][1]]
             .config(text=f'{pawns_on_current_tile}', fg=self.current_player.colour))

            (self.board[game_to_normal_coords_dict[self.current_player.chosen_pawn.coords][0]]
             [game_to_normal_coords_dict[self.current_player.chosen_pawn.coords][1]]
             .config(text=f'{pawns_on_next_tile}', fg=self.current_player.colour))

            if self.current_player.chosen_pawn.is_in_destination_square:
                if all(not pawn.is_in_destination_square or pawn.coords != current_coords for pawn in
                       self.current_player.pawns):
                    (self.board[game_to_normal_coords_dict[current_coords][0]]
                     [game_to_normal_coords_dict[current_coords][1]]
                     .config(image=self.pixel))
                (self.board[game_to_normal_coords_dict[self.current_player.chosen_pawn.coords][0]]
                 [game_to_normal_coords_dict[self.current_player.chosen_pawn.coords][1]]
                 .config(image=self.border_list[(self.current_player.colour, self.current_player.chosen_pawn.id)]))

            # sprawdzanie win condition
            if self.current_player.chosen_pawn.is_in_destination_square:
                if len({pawn.coords for pawn in self.current_player.pawns if pawn.is_in_destination_square}) == 4:
                    self.end_game()

    def end_game(self):
        """Funkcja wyświetlająca okienko z komunikatem o zakończeniu gry i zwycięzcy.
        """
        end_com = tk.Tk()
        end_com.title('Koniec gry')
        tk.Label(end_com, text=f"\n{self.current_player.name} wygrał\n", fg=self.current_player.colour,
                 font=('Comic sans MS', 20)).pack()
        end_com.mainloop()

    # Farmer
    def setup_neighbours(self):
        """Funkcja przy inicjalizacji gry przyporządkowuje wszystkim polom ich sąsiadów
        """
        for y in range(8):
            for x in range(8):
                neighbours = []
                if y > 0:
                    neighbours.append(self.fields[y - 1][x])
                if y < 7:
                    neighbours.append(self.fields[y + 1][x])
                if x > 0:
                    neighbours.append(self.fields[y][x - 1])
                if x < 7:
                    neighbours.append(self.fields[y][x + 1])
                self.fields[y][x].neighbours = neighbours

    def unlock_clipboard_mode(self):
        """Metoda aktywująca tryb pozwalający na przenoszenie zwierząt z planszy do schowka jednym kliknięciem.
        Swego rodzaju odwrotność place_animal().
        """
        if self.current_player.to_clipboard == True:
            self.clipboard_mode_bt.configure(bg='red')
            self.current_player.to_clipboard = False
        else:
            self.current_player.to_clipboard = True
            self.clipboard_mode_bt.configure(bg='green')

    def predator_attack(self, val, predator):
        """Metoda obsługuje atak wilka/lisa. Lisy zjadają wszystkie króliki ze wszystkich pól na planszy o wartości val, wilki zaś
        wszystkie pozostałe zwierzęta (nie jedzą królików). Konie są niewrażliwe na ataki drapieżników.

        Args:
            val (int): przekazywana z roll_dice() losowa wartość pola, na którym drapieżniki będą zjadać zwierzęta.
            predator (string): przekazywany z roll_dice() rodzaj drapieżnika
        """
        for field_row in self.fields:
            for field in field_row:
                if field.value == val:
                    while field.capacity != 6:
                        if predator == "Wolf":
                            if field.animals[0].space_needed != 1 or field.animals[0].type != 'Horse':
                                animal = field.animals[0]
                                for f in animal.fields:
                                    self.farboard[f.y][f.x].config(
                                        text=f'{self.fields[f.y][f.x].value}')
                                    f.animals.pop()
                                    f.check_capacity()
                                del animal
                            else:
                                break
                        else:
                            if field.animals[0].space_needed == 1:
                                self.farboard[field.y][field.x].config(text=f'{self.fields[field.y][field.x].value}')
                                animal = field.animals.pop()
                                del animal
                                field.check_capacity()
                            else:
                                break

    def relocate_to_board(self, animal_type):
        """Metoda jest wywoływania przez kliknięcie jednego z pięciu głównych przycisków w schowku. Przenosi (o ile to możliwe) 
        zwierzę ze schowka na wybrane przez gracza pole. Korzysta z metody place_animal(), gdzie schowane jest jej zasadnicze działanie.

        Args:
            animal_type (_type_): _description_
        """
        self.current_player.to_clipboard = False
        self.clipboard_mode_bt.configure(bg='red')

        chosen_animal = Animal(animal_type)  # Wybranie ikony zwierzaka ze schowka
        if self.current_player.clipboard[animal_type] == 0:
            self.err.set("Nie masz takiego zwierzaka")
            return


        a = self.place_animal(chosen_animal.type)
        if a == 0:
            self.err.set(f"Nie ma miejsca na kolejnego zwierzaka typu {chosen_animal.type}")
        elif a == 'grzyb':
            return


    def place_animal(self, animal_type):
        """Metoda czysto techniczna, wywoływana przez metodę relocate_to_board(). Funkcja sprawdza czy umiejscowienie zwierzęcia jest możliwe
        sprawdzając pojemność pól należących do gracza. Następnie wymusza wybór pola, na które zwierzę zostanie przeniesione ze schowka. 
        W razie braku miejsca wyświetla komunikat. 
        Metoda dba o poprawne wyświetlanie się zwierząt w schowku i na polach. Uwzględnia rozmiar zwierząt,
        W razie grzyba, chroni przed nim jak inne metody.

        Args:
            animal_type (string): typ zwierzęcia do umiejscowienia na planszy. Narzucony z góry przez relocate_to_board().

        Returns:
            bool: zwraca sukces/porażka (ew. grzyb)
        """
        self.current_player.to_clipboard = False
        self.clipboard_mode_bt.configure(bg='red')
        animal = Animal(animal_type)

        if animal.space_needed < 12:
            bad_fields = []
            for field in self.current_player.fields:
                if field.capacity >= animal.space_needed:
                    break
                bad_fields.append(field)
            if len(bad_fields) == len(self.current_player.fields):
                self.err.set("Nie ma miejsca na kolejnego zwierzaka")
                return 0

            chosen_field = self.choose_field()
            if chosen_field == 'grzyb':
                return 'grzyb'
            while (chosen_field.capacity < animal.space_needed) or (chosen_field not in self.current_player.fields):
                chosen_field = self.choose_field()
                if chosen_field == 'grzyb':
                    return 'grzyb'
            chosen_field.animals.append(animal)
            animal.place(chosen_field)
            chosen_field.check_capacity()
            self.current_player.clipboard[animal.type] -= 1
            self.rabbit_bt.configure(text=f'🐰 {int(self.current_player.clipboard['Rabbit'])}')
            self.sheep_bt.configure(text=f'🐑 {int(self.current_player.clipboard['Sheep'])}')
            self.pig_bt.configure(text=f'🐷 {int(self.current_player.clipboard['Pig'])}')
            self.farboard[chosen_field.y][chosen_field.x].config(text=f'{chosen_field.value}\n'
                                                                      f'{self.animal_type_to_animal_tag[animal_type]} '
                                                                      f': {len(chosen_field.animals)}')
            return 1

        else:
            good_fields = []
            potential_pairs = 0

            for field in self.current_player.fields:
                if field.capacity == 6:
                    good_fields.append(field)

            for field in good_fields:
                for neighbour in field.neighbours:
                    if neighbour in good_fields:
                        potential_pairs += 1

            if potential_pairs != 0:
                self.info.set("To duży zwierzak, wybierz pierwsze pole")
                chosen_field = self.choose_field()
                if chosen_field == 'grzyb':
                    return 'grzyb'
            else:
                self.err.set("Nie masz dwoch wolnych pol obok siebie")
                return 0

            while chosen_field not in good_fields:
                chosen_field = self.choose_field()
                if chosen_field == 'grzyb':
                    return 'grzyb'

            self.info.set("Wybierz drugie pole")
            second_field = self.choose_field()
            if second_field == 'grzyb':
                return 'grzyb'
            while second_field not in good_fields or second_field not in chosen_field.neighbours:
                second_field = self.choose_field()
                if second_field == 'grzyb':
                    return 'grzyb'

            animal.place(chosen_field)
            animal.place(second_field)
            chosen_field.animals.append(animal)
            chosen_field.check_capacity()
            second_field.animals.append(animal)
            second_field.check_capacity()
            self.current_player.clipboard[animal.type] -= 1
            self.cow_bt.configure(text=f'🐮 {int(self.current_player.clipboard['Cow'])}')
            self.horse_bt.configure(text=f'🐴 {int(self.current_player.clipboard['Horse'])}')

            if chosen_field.x < second_field.x:
                self.farboard[chosen_field.y][chosen_field.x].config(text=f'{chosen_field.value}  '
                                                                          f'{self.animal_type_to_animal_tag[animal_type]}\n'
                                                                          f'====>')
                self.farboard[second_field.y][second_field.x].config(text=f'{self.animal_type_to_animal_tag[animal_type]}  '
                                                                          f'{second_field.value}\n'
                                                                          f'<====')
            if chosen_field.x > second_field.x:
                temp_field = second_field
                second_field = chosen_field
                chosen_field = temp_field
                self.farboard[chosen_field.y][chosen_field.x].config(text=f'{chosen_field.value}  '
                                                                          f'{self.animal_type_to_animal_tag[animal_type]}\n'
                                                                          f'====>')
                self.farboard[second_field.y][second_field.x].config(text=f'{self.animal_type_to_animal_tag[animal_type]}  '
                                                                          f'{second_field.value}\n'
                                                                          f'<====')

            if chosen_field.y > second_field.y:
                self.farboard[chosen_field.y][chosen_field.x].config(text=f'{chosen_field.value}  '
                                                                          f'{self.animal_type_to_animal_tag[animal_type]}\n'
                                                                          f'||')
                self.farboard[second_field.y][second_field.x].config(text=f'||\n'
                                                                          f'{second_field.value}  '
                                                                          f'{self.animal_type_to_animal_tag[animal_type]}')
            if chosen_field.y < second_field.y:
                temp_field = second_field
                second_field = chosen_field
                chosen_field = temp_field
                self.farboard[chosen_field.y][chosen_field.x].config(text=f'{chosen_field.value}  '
                                                                          f'{self.animal_type_to_animal_tag[animal_type]}\n'
                                                                          f'||')
                self.farboard[second_field.y][second_field.x].config(text=f'||\n'
                                                                          f'{second_field.value}  '
                                                                          f'{self.animal_type_to_animal_tag[animal_type]}')


            return 1

    def exchange_animals(self, first_type, second_type):
        """Metoda korzystająca z 'exchange' z klasy Marketplace. Obsługuje wymianę zwierząt na inne.
        Wywoływana jest przez przyciski ze strzałeczkami pod planszami. 

        Args:
            first_type (string): zwierzę, które gracz chce wymienić
            second_type (string): zwierzę, które gracz chce otrzymać
        """
        self.market.exchange(first_type, second_type, self.current_player)
        self.rabbit_bt.configure(text=f'🐰 {int(self.current_player.clipboard['Rabbit'])}')
        self.sheep_bt.configure(text=f'🐑 {int(self.current_player.clipboard['Sheep'])}')
        self.pig_bt.configure(text=f'🐷 {int(self.current_player.clipboard['Pig'])}')
        self.cow_bt.configure(text=f'🐮 {int(self.current_player.clipboard['Cow'])}')
        self.horse_bt.configure(text=f'🐴 {int(self.current_player.clipboard['Horse'])}')



    def buy_field(self):
        """Metoda korzystająca z 'buy_field' z klasy Marketplace. Metoda jest wywoływania przez kliknięcie przycisku 'kup pole' przez gracza.
        Obsługuje kupowanie pól. W razie nieprawidłowego wyboru pola, wyświetlany jest komunikat i nic sie nie dzieje. 
        Zwracany grzyb widmo chroni przed grzybem (kolejkowaniem się choose_field()).
        """
        self.current_player.to_clipboard = False
        self.clipboard_mode_bt.configure(bg='red')
        self.selected_field = None
        chosen_field = self.choose_field()
        if chosen_field == 'grzyb':
            return 
        set_of_neighbours = set()
        for field in self.current_player.fields:
            for neighbour in field.neighbours:
                set_of_neighbours.add(neighbour)

        if any(chosen_field in player.fields for player in self.players):
            self.err.set("To pole ma już właściciela")
            self.selected_field = None

        elif chosen_field not in set_of_neighbours:
            self.err.set("Mozesz kupowac tylko pola sasiadujace z Twoimi")

        elif self.market.buy_field(chosen_field, self.current_player):
            self.farboard[chosen_field.y][chosen_field.x].configure(bg=self.current_player.colour)
            self.info.set(f"Pole ({chosen_field.x},{chosen_field.y}) zakupione")
            self.rabbit_bt.configure(text=f'🐰 {int(self.current_player.clipboard['Rabbit'])}')





    def upgrade_field(self):
        """Metoda korzystająca z 'upgrade' z klasy Marketplace. Metoda jest wywoływania przez kliknięcie przycisku 'ulepsz pole' przez gracza.
        Obsługuje ulepszanie pól. Metoda dba o poprawne wyświetlanie się
        zwierząt po ulepszeniu. W razie nieprawidłowego wyboru pola, wyświetlany jest komunikat i nic sie nie dzieje.
        Zwracany grzyb chroni przed grzybem (kolejkowaniem się choose_field()).
        """
        self.current_player.to_clipboard = False
        self.clipboard_mode_bt.configure(bg='red')
        self.selected_field = None
        chosen_field = self.choose_field()
        if chosen_field == 'grzyb':
            return 'grzyb'

        if chosen_field not in self.current_player.fields:
            self.err.set("To pole nie należy do Ciebie")
            self.selected_field = None
        elif self.market.upgrade_field(chosen_field, self.current_player):
            self.info.set(f"Ulepszenie pola ({chosen_field.x},{chosen_field.y}) udane")
            self.rabbit_bt.configure(text=f'🐰 {int(self.current_player.clipboard['Rabbit'])}')
            if len(chosen_field.animals) == 0:
                self.farboard[chosen_field.y][chosen_field.x].config(text=f'{chosen_field.value}')
            elif chosen_field.animals[0].space_needed < 12:
                self.farboard[chosen_field.y][chosen_field.x].config(text=f'{chosen_field.value}\n'
                                                                      f'{self.animal_type_to_animal_tag[chosen_field.animals[0].type]} '
                                                                      f': {len(chosen_field.animals)}')
            else:
                animal = chosen_field.animals[0]
                first_field = animal.fields[0]
                second_field = animal.fields[1]
                if first_field.x < second_field.x:
                    self.farboard[first_field.y][first_field.x].config(text=f'{first_field.value}  '
                                                                            f'{self.animal_type_to_animal_tag[animal.type]}\n'
                                                                            f'====>')
                    self.farboard[second_field.y][second_field.x].config(
                        text=f'{self.animal_type_to_animal_tag[animal.type]}  '
                             f'{second_field.value}\n'
                             f'<====')
                if first_field.x > second_field.x:
                    temp_field = second_field
                    second_field = first_field
                    first_field = temp_field
                    self.farboard[first_field.y][first_field.x].config(text=f'{first_field.value}  '
                                                                            f'{self.animal_type_to_animal_tag[animal.type]}\n'
                                                                            f'====>')
                    self.farboard[second_field.y][second_field.x].config(
                        text=f'{self.animal_type_to_animal_tag[animal.type]}  '
                             f'{second_field.value}\n'
                             f'<====')

                if first_field.y > second_field.y:
                    self.farboard[first_field.y][first_field.x].config(text=f'{first_field.value}  '
                                                                            f'{self.animal_type_to_animal_tag[animal.type]}\n'
                                                                            f'||')
                    self.farboard[second_field.y][second_field.x].config(text=f'||\n'
                                                                              f'{second_field.value}  '
                                                                              f'{self.animal_type_to_animal_tag[animal.type]}')
                if first_field.y < second_field.y:
                    temp_field = second_field
                    second_field = first_field
                    first_field = temp_field
                    self.farboard[first_field.y][first_field.x].config(text=f'{first_field.value}  '
                                                                            f'{self.animal_type_to_animal_tag[animal.type]}\n'
                                                                            f'||')
                    self.farboard[second_field.y][second_field.x].config(text=f'||\n'
                                                                              f'{second_field.value}  '
                                                                              f'{self.animal_type_to_animal_tag[animal.type]}')


    def set_selected_field(self, x, y):
        """Metoda wywoływania przez kliknięcie pola przez gracza. Jeżeli tryb 'to_clipboard' jest aktywny, kliknięcie
        przenosi zwierzę z pola do schowka. W przeciwnym wypadku ustawia koordynaty klikniętego pola jako self.selected_field.
        Wywoływane również przez choose_field()

        Args:
            x (int): współrzędna 'x' wybranego pola
            y (int): współrzędna 'y' wybranego pola
        """
        if self.current_player.to_clipboard:
            if self.fields[y][x] in self.current_player.fields:
                if self.fields[y][x].animals != []:
                    animal = self.fields[y][x].animals[0]
                    for field in animal.fields:
                        field.animals.pop()
                        field.check_capacity()
                    self.current_player.clipboard[animal.type] += 1
                    self.rabbit_bt.configure(text=f'🐰 {int(self.current_player.clipboard['Rabbit'])}')
                    self.sheep_bt.configure(text=f'🐑 {int(self.current_player.clipboard['Sheep'])}')
                    self.pig_bt.configure(text=f'🐷 {int(self.current_player.clipboard['Pig'])}')
                    self.cow_bt.configure(text=f'🐮 {int(self.current_player.clipboard['Cow'])}')
                    self.horse_bt.configure(text=f'🐴 {int(self.current_player.clipboard['Horse'])}')
                    if len(self.fields[y][x].animals) != 0:
                        if animal.space_needed <= 6:
                            self.farboard[y][x].config(text=f'{self.fields[y][x].value}\n'
                                                        f'{self.animal_type_to_animal_tag[animal.type]} '
                                                        f': {len(self.fields[y][x].animals)}')
                        else:
                            for field in animal.fields:
                                self.farboard[field.y][field.x].config(text=f'{self.fields[field.y][field.x].value}\n'
                                                        f'{self.animal_type_to_animal_tag[animal.type]} '
                                                        f': {len(self.fields[field.y][field.x].animals)}')
                    else:
                        if animal.space_needed <= 6:
                            self.farboard[y][x].config(text=f'{self.fields[y][x].value}')
                        else:
                            for field in animal.fields:
                                self.farboard[field.y][field.x].config(text=f'{self.fields[field.y][field.x].value}')
                else:
                    self.err.set("Nie ma zwierzat na tym polu")
            else:
                self.err.set("To nie Twoje pole")
        else:
            self.selected_field = (x, y)
            self.selected_field_var.set(f"{x},{y}")
            # print(f"Selected field: ({x},{y})")

    def choose_field(self):
        """Funkcja zwracająca pole wywoływana przez metody potrzebujące wybrania pola.
        on_off blokuje kolejkowanie się wybranych funkcji przy niewłaściwym wyborze kolejności przycisków.

        Returns:
            Field: zwraca pole potrzebne w innej funkcji. W razie niewłaściwego wyboru chroni przed błędami.
        """
        if self.on_off == False:
            self.on_off = True
            self.selected_field_var.set("")
            self.root.wait_variable(self.selected_field_var)
            x, y = self.selected_field
            self.on_off = False
            return self.fields[y][x]
        else:
            return 'grzyb'


if __name__ == "__main__":
    a = GUI(TEMP_PLAYERS)
    a.play()
