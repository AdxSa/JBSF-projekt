import tkinter as tk
from Player import Player
from farmer import Field, Animal, Marketplace
from PIL import Image, ImageTk
from bigdict import game_to_normal_coords_dict, normal_to_game_coords_dict

TEMP_PLAYER_1 = Player('purple', (0, 0, 0), 'TEMP_PLAYER_1')
TEMP_PLAYER_2 = Player('green', (2, 0, 0), 'TEMP_PLAYER_2')
TEMP_PLAYERS = [TEMP_PLAYER_1, TEMP_PLAYER_2]


class GUI:
    chessboard_colours = ['black', 'white']
    error_code = 0

    def __init__(self, players):
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
        self.player_info_label = tk.Label(self.root, textvariable=self.player_info, font=('Arial', 20))
        self.info_label = tk.Label(self.root, textvariable=self.info, font=('Arial', 20))
        self.err_label = tk.Label(self.root, textvariable=self.err, font=('Arial', 20), fg='red')
        self.player_info_label.pack()
        self.info_label.pack()
        self.err_label.pack()

        self.root.geometry("1920x1080")
        self.root.resizable(False, False)
        self.root.title("Jeszcze Lepszy Super Farmer")

        self.end_turn_bt = tk.Button(self.root, text="Koniec tury", font=('Arial', 16),
                                     command=lambda: self.next_player())
        self.end_turn_bt.place(x=1700, y=980)

        # Przycisk Rzuć kostką:
        self.frame = tk.Frame(self.root, width=310, height=100)
        self.frame.pack_propagate(False)
        self.frame.place(x=1600, y=20)

        self.dice_roll_bt = tk.Button(self.frame, text="Rzuć kostką", font=('Arial', 16),
                                      command=lambda: self.roll_dice())
        self.dice_roll_bt.pack()

        self.dice_roll_result = tk.StringVar()
        self.dice_roll_result.set("Nie rzucono kostką")
        self.dice_roll_result_label = tk.Label(self.frame, textvariable=self.dice_roll_result, font=('Arial', 16))
        self.dice_roll_result_label.pack()

        self.dice_roll_done_inform = tk.StringVar()
        self.dice_roll_done_inform.set('')
        self.dice_roll_done_inform_label = tk.Label(self.frame, textvariable=self.dice_roll_done_inform,
                                                    font=('Arial', 16))
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
                                                 compound='center', font=('Arial', 12),
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
        self.move_pawn_bt = tk.Button(self.buttonframe, text="Porusz się pionkiem", font=('Arial', 16),
                                      command=lambda: self.move_pawn())
        self.move_pawn_bt.grid(row=0, column=1, sticky=tk.W + tk.E)

        # Przycisk Stwórz pionek:
        self.create_pawn_bt = tk.Button(self.buttonframe, text="Stwórz pionek", font=('Arial', 16),
                                        command=lambda: self.create_pawn())
        self.create_pawn_bt.grid(row=0, column=0, sticky=tk.W + tk.E)

        # Przycisk Wejdź poziom wyżej:
        self.upgrade_pawn_bt = tk.Button(self.buttonframe, text="Wejdź poziom wyżej", font=('Arial', 16),
                                         command=lambda: self.upgrade_pawn())
        self.upgrade_pawn_bt.grid(row=1, column=0, sticky=tk.W + tk.E)

        # Przycisk Zejdź poziom niżej
        self.degrade_pawn_bt = tk.Button(self.buttonframe, text="Zejdź poziom niżej", font=('Arial', 16),
                                         command=lambda: self.degrade_pawn())
        self.degrade_pawn_bt.grid(row=1, column=1, sticky=tk.W + tk.E)

        self.buttonframe.place(x=100, y=670)

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
        self.setup_neighbours()
        self.market = Marketplace()

        #  przyciski do farmera
        # plansza farmera
        self.farmerboard = tk.Frame(width=400, height=400, highlightthickness=1, highlightbackground='black')
        self.farboard = [['' for row in range(8)] for col in range(8)]  # macierz guzików
        for col in range(8):
            for row in range(8):
                self.farboard[row][col] = tk.Button(self.farmerboard, image=self.pixel, width=50, height=50,
                                                    text=f"",
                                                    compound='center', font=('Arial', 12),
                                                    command=lambda i=col, j=row:
                                                    self.choose_field(j, i))
                self.farboard[row][col].grid(row=7 - row, column=col)
        self.farmerboard.place(x=700, y=200)

        # clipboard
        self.clipboard = tk.Frame(self.root, highlightthickness=1, highlightbackground='black')
        self.clipboard.columnconfigure(0, weight=1)

        self.rabbit_bt = tk.Button(self.clipboard, image=self.pixel, width=80, height=80, compound='center',
                                   font=('Arial', 16), command=lambda: self.relocate_to_board("Rabbit"))
        self.rabbit_bt.grid(row=0, column=1)

        self.sheep_bt = tk.Button(self.clipboard, image=self.pixel, width=80, height=80, compound='center',
                                  font=('Arial', 16), command=lambda: self.relocate_to_board("Sheep"))
        self.sheep_bt.grid(row=1, column=1)

        self.pig_bt = tk.Button(self.clipboard, image=self.pixel, width=80, height=80, compound='center',
                                font=('Arial', 16), command=lambda: self.relocate_to_board("Pig"))
        self.pig_bt.grid(row=2, column=1)

        self.cow_bt = tk.Button(self.clipboard, image=self.pixel, width=80, height=80, compound='center',
                                font=('Arial', 16), command=lambda: self.relocate_to_board("Cow"))
        self.cow_bt.grid(row=3, column=1)

        self.horse_bt = tk.Button(self.clipboard, image=self.pixel, width=80, height=80, compound='center',
                                  font=('Arial', 16), command=lambda: self.relocate_to_board("Horse"))
        self.horse_bt.grid(row=4, column=1)

        self.clipboard_mode_bt = tk.Button(self.clipboard, image=self.pixel, width=80, height=80, compound='center',
                                           font=('Arial', 16), command=lambda: self.unlock_clipboard_mode())
        self.clipboard_mode_bt.grid(row=5, column=1)

        self.clipboard.place(x=1200, y=200)

        # marketplace
        # self.sheep = tk.PhotoImage(file='360.png')
        self.marketplace = tk.Frame(self.root)
        self.rabbit_label = tk.Label(self.marketplace, text='🐰', fg='grey', font=('Arial', 80))
        self.rabbit_label.grid(row=0, column=0)

        self.sheep_label = tk.Label(self.marketplace, text='🐑', fg='black', font=('Arial', 80))
        self.sheep_label.grid(row=0, column=2)

        self.pig_label = tk.Label(self.marketplace, text='🐷', fg='pink', font=('Arial', 80))
        self.pig_label.grid(row=0, column=4)

        self.cow_label = tk.Label(self.marketplace, text='🐮', fg='#df546c', font=('Arial', 80))
        self.cow_label.grid(row=0, column=6)

        self.horse_label = tk.Label(self.marketplace, text='🐴', fg='brown', font=('Arial', 80))
        self.horse_label.grid(row=0, column=8)
        # rabbit-sheep buttons
        self.rabbit_sheep_bt_frame = tk.Frame(self.marketplace)
        self.rabbit_to_sheep_bt = tk.Button(self.rabbit_sheep_bt_frame, text='🡆', image=self.pixel, width=40,
                                            height=40, compound='center',
                                            font=('Arial', 24), command=lambda: self.exchange_animals("Rabbit", "Sheep"))
        self.rabbit_to_sheep_bt.grid(row=0, column=0)
        tk.Label(self.rabbit_sheep_bt_frame, text='6 : 1', font=('Arial', 16)).grid(row=1, column=0)
        self.sheep_to_rabbit_bt = tk.Button(self.rabbit_sheep_bt_frame, text='🡄', image=self.pixel, width=40,
                                            height=40, compound='center',
                                            font=('Arial', 24), command=lambda: self.exchange_animals("Sheep", "Rabbit"))
        self.sheep_to_rabbit_bt.grid(row=2, column=0)
        self.rabbit_sheep_bt_frame.grid(row=0, column=1)
        # sheep-pig buttons
        self.sheep_pig_bt_frame = tk.Frame(self.marketplace)
        self.sheep_to_pig_bt = tk.Button(self.sheep_pig_bt_frame, text='🡆', image=self.pixel, width=40, height=40,
                                            compound='center',
                                            font=('Arial', 24))
        tk.Label(self.sheep_pig_bt_frame, text='2 : 1', font=('Arial', 16)).grid(row=1, column=0)
        self.sheep_to_pig_bt.grid(row=0, column=0)
        self.pig_to_sheep_bt = tk.Button(self.sheep_pig_bt_frame, text='🡄', image=self.pixel, width=40,
                                            height=40, compound='center',
                                            font=('Arial', 24))
        self.pig_to_sheep_bt.grid(row=2, column=0)
        self.sheep_pig_bt_frame.grid(row=0, column=3)
        # pig-cow buttons
        self.pig_cow_bt_frame = tk.Frame(self.marketplace)
        self.pig_to_cow_bt = tk.Button(self.pig_cow_bt_frame, text='🡆', image=self.pixel, width=40, height=40,
                                            compound='center',
                                            font=('Arial', 24))
        self.pig_to_cow_bt.grid(row=0, column=0)
        tk.Label(self.pig_cow_bt_frame, text='2 : 1', font=('Arial', 16)).grid(row=1, column=0)
        self.cow_to_pig_bt = tk.Button(self.pig_cow_bt_frame, text='🡄', image=self.pixel, width=40,
                                            height=40, compound='center',
                                            font=('Arial', 24))
        self.cow_to_pig_bt.grid(row=2, column=0)
        self.pig_cow_bt_frame.grid(row=0, column=5)
        # cow-horse buttons
        self.cow_horse_bt_frame = tk.Frame(self.marketplace)
        self.cow_to_horse_bt = tk.Button(self.cow_horse_bt_frame, text='🡆', image=self.pixel, width=40, height=40,
                                            compound='center',
                                            font=('Arial', 24))
        self.cow_to_horse_bt.grid(row=0, column=0)
        tk.Label(self.cow_horse_bt_frame, text='2 : 1', font=('Arial', 16)).grid(row=1, column=0)
        self.horse_to_cow_bt = tk.Button(self.cow_horse_bt_frame, text='🡄', image=self.pixel, width=40,
                                            height=40, compound='center',
                                            font=('Arial', 24))
        self.horse_to_cow_bt.grid(row=2, column=0)
        self.cow_horse_bt_frame.grid(row=0, column=7)

        # pole pole łyse pole
        # self.polepole = tk.PhotoImage(file='polepole.png')
        self.pola_bt_frame = tk.Frame(self.marketplace)
        self.buy_field_bt = tk.Button(self.pola_bt_frame, text='Kup pole', font=('Arial, 20'))
        self.buy_field_bt.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        self.upgrade_field_bt = tk.Button(self.pola_bt_frame, text='Ulepsz pole', font=('Arial, 20'))
        self.upgrade_field_bt.grid(row=1, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        self.pola_bt_frame.grid(row=0, column=9, padx=50)

        self.marketplace.place(x=100, y=800)

    def play(self):
        self.root.mainloop()

    def next_player(self):
        self.current_player.rolled = False
        self.current_player.chosen_pawn = None
        self.current_player_number = self.current_player_number + 1
        self.current_player = self.players[self.current_player_number % len(self.players)]
        self.player_info.set(f"Tura gracza: {self.current_player.name}")
        self.info.set('')
        self.err.set('')
        error_code = 0
        self.dice_roll_done_inform.set('')
        self.dice_roll_result.set('Nie rzucono kostką')

    def roll_dice(self):
        if self.current_player.rolled:
            self.dice_roll_done_inform.set("Już rzuciłeś kostką w tej turze")
        self.current_player.roll_dice()
        self.dice_roll_result.set(self.current_player.current_roll)
        if self.error_code == 1:
            self.err.set('')

    def create_pawn(self):
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
            # zamieniamy współrzędne spawn_coords wybranego gracza na współrzędne kalsyczne szachownicy,
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
        except:
            self.err.set('Nie możesz stworzyć kolejnego pionka')

    def choose_pawn(self, row, col):
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
        #  if player.current_roll is not None:

    def move_pawn(self):  # porusza wybranym pionkiem oraz zmienia grafikę na odpowiednich polach
        # dodać zbijanie pionków innych graczy (realnie, graficznie już jest)
        if self.current_player.rolled and self.current_player.chosen_pawn is not None:
            current_coords = self.current_player.chosen_pawn.coords
            self.current_player.move_chosen_pawn()
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

            # print(player.chosen_pawn.coords)
            # print(self.board[game_to_normal_coords_dict[player.chosen_pawn.coords][0]]
            # [game_to_normal_coords_dict[player.chosen_pawn.coords][1]])
            (self.board[game_to_normal_coords_dict[self.current_player.chosen_pawn.coords][0]]
             [game_to_normal_coords_dict[self.current_player.chosen_pawn.coords][1]]
             .config(text=f'{pawns_on_next_tile}', fg=self.current_player.colour))


            # potencjalnie kolorowanie pól na które ostatecznie dotarły już pionki
            #if self.current_player.chosen_pawn.is_in_destination_square:
                #(self.board[game_to_normal_coords_dict[self.current_player.chosen_pawn.coords][0]]
                #[game_to_normal_coords_dict[self.current_player.chosen_pawn.coords][1]]
                #.config(bg=self.current_player.colour))


            # zbijanie
            for player in self.players:
                if player != self.current_player:
                    for pawn in player.pawns:
                        if ((game_to_normal_coords_dict[pawn.coords] ==
                                game_to_normal_coords_dict[self.current_player.chosen_pawn.coords])
                                and not pawn.is_in_destination_square):
                            player.pawns_id.remove(int(pawn.id))
                            player.pawns.remove(pawn)
                            print(player.pawns)
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
        if self.current_player.chosen_pawn is None:
            self.err.set('Wybierz pionek')
            self.error_code = 2
        else:
            current_coords = self.current_player.chosen_pawn.coords
            self.current_player.upgrade_chosen_pawn()
            pawns_on_current_tile = ''
            pawns_on_next_tile = ''
            for pawn in self.current_player.pawns:
                if pawn.coords == current_coords:
                    pawns_on_current_tile += pawn.tag + '\n'
                if pawn.coords == self.current_player.chosen_pawn.coords:
                    pawns_on_next_tile += pawn.tag + '\n'
            # zmieniamy wspólrzędne wybranego pionka na klasyczne aby pobrać odpowiedni index od self.board
            # następnie usuwamy wizerunek pionka z danego pola po czym przesówamy pionek i
            # tworzymy wizerunek na miejscu w którym znajduje się pionek w sposób odwrotny
            (self.board[game_to_normal_coords_dict[current_coords][0]]
             [game_to_normal_coords_dict[current_coords][1]]
             .config(text=f'{pawns_on_current_tile}', fg=self.current_player.colour))

            (self.board[game_to_normal_coords_dict[self.current_player.chosen_pawn.coords][0]]
             [game_to_normal_coords_dict[self.current_player.chosen_pawn.coords][1]]
             .config(text=f'{pawns_on_next_tile}', fg=self.current_player.colour))

            # zbijanie
            for player in self.players:
                if player != self.current_player:
                    for pawn in player.pawns:
                        if (game_to_normal_coords_dict[pawn.coords] ==
                                game_to_normal_coords_dict[self.current_player.chosen_pawn.coords]):
                            player.pawns_id.remove(int(pawn.id))
                            player.pawns.remove(pawn)
                            print(player.pawns)
                            del pawn

            # sprawdzanie win condition
            if self.current_player.chosen_pawn.is_in_destination_square:
                if len({pawn.coords for pawn in self.current_player.pawns if pawn.is_in_destination_square}) == 4:
                    self.end_game()

    def degrade_pawn(self):
        if self.current_player.chosen_pawn is None:
            self.err.set('Wybierz pionek')
            self.error_code = 2
        else:
            current_coords = self.current_player.chosen_pawn.coords
            self.current_player.degrade_chosen_pawn()
            pawns_on_current_tile = ''
            pawns_on_next_tile = ''
            for pawn in self.current_player.pawns:
                if pawn.coords == current_coords:
                    pawns_on_current_tile += pawn.tag + '\n'
                if pawn.coords == self.current_player.chosen_pawn.coords:
                    pawns_on_next_tile += pawn.tag + '\n'
            # zmieniamy wspólrzędne wybranego pionka na klasyczne aby pobrać odpowiedni index od self.board
            # następnie usuwamy wizerunek pionka z danego pola po czym przesówamy pionek i
            # tworzymy wizerunek na miejscu w którym znajduje się pionek w sposób odwrotny
            (self.board[game_to_normal_coords_dict[current_coords][0]]
             [game_to_normal_coords_dict[current_coords][1]]
             .config(text=f'{pawns_on_current_tile}', fg=self.current_player.colour))

            (self.board[game_to_normal_coords_dict[self.current_player.chosen_pawn.coords][0]]
             [game_to_normal_coords_dict[self.current_player.chosen_pawn.coords][1]]
             .config(text=f'{pawns_on_next_tile}', fg=self.current_player.colour))

            # sprawdzanie win condition
            if self.current_player.chosen_pawn.is_in_destination_square:
                if len({pawn.coords for pawn in self.current_player.pawns if pawn.is_in_destination_square}) == 4:
                    self.end_game()

    def end_game(self):
        end_com = tk.Tk()
        end_com.title('Koniec gry')
        tk.Label(end_com, text=f"\n{self.current_player.name} wygrał\n", fg=self.current_player.colour,
                 font=('Comic sans MS', 20)).pack()
        end_com.mainloop()

    # Farmer
    def setup_neighbours(self):
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
        if self.current_player.to_clipboard == True:
            self.current_player.to_clipboard = False
        else:
            self.current_player.to_clipboard = True
        print(self.current_player.to_clipboard)

    def choose_field(self, x, y):
        if self.current_player.to_clipboard == True:
            if self.fields[x][y].animals != []:
                animal = self.fields[x][y].animals.pop()
                self.current_player.clipboard[animal.animal_type] += 1
            else:
                print("Nie ma zwierzat na tym polu")
        else:
            return self.fields[x][y]

    def relocate_to_board(self, animal_type):
        self.current_player.to_clipboard = False

        chosen_animal = Animal(animal_type)  # Wybranie ikony zwierzaka ze schowka
        if self.current_player.clipboard[animal_type] == 0:
            print("Nie masz takiego zwierzaka")

        elif not self.place_animal(chosen_animal.type):
            print(f"There is no space for another {chosen_animal.type}")

    def place_animal(self, animal_type):    
        self.current_player.to_clipboard = False
        animal = Animal(animal_type)
        selected = False

        if animal.space_needed < 12:
            bad_fields = []
            for field in self.current_player.fields:
                if field.capacity >= animal.space_needed:
                    break
                bad_fields.append(field)
            if len(bad_fields) == len(self.current_player.fields):
                print("There is no space for another animal!")
                return 0
            
            chosen_field = self.choose_field()    
            while (chosen_field.capacity < animal.space_needed) or (chosen_field not in self.current_player.fields):
                chosen_field = self.choose_field()
            chosen_field.animals.append(animal)
            animal.place(chosen_field)
            chosen_field.check_capacity()
            return 1

        else:
            good_fields = []
            potential_pairs = 0

            for field in self.current_player.fields:
                if field.capacity == 6:
                    good_fields.append(field)

            for field in good_fields:
                for neighbour in field.neighbours:
                    if neighbour.capacity == 6:
                        potential_pairs += 1

            if potential_pairs != 0:
                chosen_field = self.choose_field()
            while (chosen_field.capacity < animal.space_needed) or (chosen_field not in self.current_player.fields):
                chosen_field = self.choose_field()

            second_field = self.choose_field()
            while (second_field.capacity < animal.space_needed) or (second_field not in self.current_player.fields) or (
                    second_field not in chosen_field.neighbours):
                second_field = self.choose_field()

            animal.place(chosen_field)
            animal.place(second_field)
            chosen_field.animals.append(animal)
            chosen_field.check_capacity()
            second_field.animals.append(animal)
            second_field.check_capacity()
            return 1




if __name__ == "__main__":
    a = GUI(TEMP_PLAYERS)
    a.play()
