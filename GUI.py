import tkinter as tk
from Player import Player
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
                self.board[row][col].grid(row=7-row, column=col)
        self.chessboard.place(x=0, y=0)

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

        self.buttonframe.place(x=0, y=470)

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
            # if self.current_player.chosen_pawn.is_in_destination_square:
            #    (self.board[game_to_normal_coords_dict[self.current_player.chosen_pawn.coords][0]]
            #     [game_to_normal_coords_dict[self.current_player.chosen_pawn.coords][1]]
            #     .config(bg=self.current_player.colour))

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


a = GUI(TEMP_PLAYERS)
