import tkinter as tk
from Player import Player
from PIL import Image, ImageTk
from bigdict import normal_to_game_coords_dict, game_to_normal_coords_dict

TEMP_PLAYER_1 = Player('purple', (0, 0, 0), 'TEMP_PLAYER_1')
TEMP_PLAYER_2 = Player('green', (2, 0, 0), 'TEMP_PLAYER_2')

class GUI:
    chessboard_colours = ['black', 'white']
    def roll_dice(self, player):
        if player.rolled:
            self.dice_roll_done_inform.set("You have already rolled the dice!")
        player.roll_dice()
        self.dice_roll_result.set(player.current_roll)

    def create_pawn(self, player):
        player.create_pawn()
        self.board[game_to_normal_coords_dict[player.pawn_spawn_coords][0]][game_to_normal_coords_dict[player.pawn_spawn_coords][1]].config(text='♟', fg=player.colour)


    def __init__(self):
        self.root = tk.Tk()

        self.player_info = tk.StringVar()
        self.player_info.set(f"Tura gracza: {TEMP_PLAYER_1.name}")
        self.player_info_label = tk.Label(self.root, textvariable=self.player_info, font=('Arial', 20))
        self.player_info_label.pack()

        path = "chessboard.jpg"
        self.chessboardimg = ImageTk.PhotoImage(Image.open(path))

        self.root.geometry("1920x1080")
        self.root.resizable(False, False)
        self.root.title("Jeszcze Lepszy Super Farmer")

        self.bt1 = tk.Button(self.root, text="Koniec tury", font=('Arial', 16))
        self.bt1.place(x=1700, y=980)

        # Przycisk Rzuć kostką:
        self.frame = tk.Frame(self.root, width=310, height=100)
        self.frame.pack_propagate(False)
        self.frame.place(x=1600, y=20)

        self.dice_roll_bt = tk.Button(self.frame, text="Rzuć kostką", font=('Arial', 16), command=lambda: self.roll_dice(TEMP_PLAYER_1))
        self.dice_roll_bt.pack()

        self.dice_roll_result = tk.StringVar()
        self.dice_roll_result.set("You haven't rolled the dice yet")
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
        self.board = [[None for row in range(8)] for col in range(8)]
        from itertools import cycle
        for col in range(8):
            color = cycle(self.chessboard_colours[::-1] if not col % 2 else self.chessboard_colours)
            for row in range(8):
                self.board[row][col] = tk.Button(self.chessboard, bg=next(color), image=self.pixel, width=50, height=50,
                                                 text=f"", compound='center', font=('Arial', 20))
                #text = f"tile{normal_to_game_coords_dict[(col, row)]}" aby sprawdzić czy na pewno dobra numeracja
                self.board[row][col].grid(row=7-row, column=col)
        self.chessboard.place(x=0,y=0)


        # inne:

        self.buttonframe = tk.Frame(self.root)
        self.buttonframe.columnconfigure(0, weight=1)
        self.buttonframe.columnconfigure(1, weight=1)

        self.Choose_pawn_bt = tk.Button(self.buttonframe, text="Wybierz pionek", font=('Arial', 16))
        self.Choose_pawn_bt.grid(row=0, column=0, sticky=tk.W + tk.E)

        self.move_pawn_bt = tk.Button(self.buttonframe, text="Porusz się pionkiem", font=('Arial', 16))
        self.move_pawn_bt.grid(row=0, column=1, sticky=tk.W + tk.E)

        self.upgrade_pawn_bt = tk.Button(self.buttonframe, text="Wejdź poziom wyżej", font=('Arial', 16))
        self.upgrade_pawn_bt.grid(row=1, column=0, sticky=tk.W + tk.E)

        self.degrade_pawn_bt = tk.Button(self.buttonframe, text="Zejdź poziom niżej", font=('Arial', 16))
        self.degrade_pawn_bt.grid(row=1, column=1, sticky=tk.W + tk.E)

        # Przycisk Stwórz pionek:
        self.create_pawn_bt = tk.Button(self.buttonframe, text="Stwórz pionek", font=('Arial', 16), command=lambda: self.create_pawn(TEMP_PLAYER_1))
        self.create_pawn_bt.grid(row=3, column=0, sticky=tk.W + tk.E)


        self.buttonframe.place(x=0, y=470)

        self.chessboardimglabel = tk.Label(self.root, image=self.chessboardimg)
        #self.chessboardimglabel.place(x=0,y=0)

        self.root.mainloop()


a = GUI()



