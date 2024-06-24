import tkinter as tk
from GUI import GUI
from Player import Player


class ConfigGui:
    """Swego rodzaju menu. Pozwala na dodanie graczy i przypisanie im nazw.
    """

    #  all_config_colours = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow']
    def first_switch(self):
        if self.is_1_on:
            self.on_1_bt_text.set('Dodaj gracza')
            self.on_1_bt.config(fg='green')
            self.is_1_on = not self.is_1_on
            self.on_2_bt.grid_forget()
            self.name1_entry.grid_forget()
            self.first_player_color_bt.grid_forget()
        else:
            self.on_1_bt_text.set('Usuń gracza')
            self.on_1_bt.config(fg='red')
            self.on_2_bt_text.set('Dodaj gracza')
            self.on_2_bt.config(fg='green')
            self.is_1_on = not self.is_1_on
            self.name1_entry.grid(row=1, column=1, padx=15, pady=10, ipady=5, sticky=tk.E+tk.W+tk.N)
            self.first_player_color_bt.grid(row=1, column=2, padx=15, pady=10, ipady=5, sticky=tk.E+tk.W+tk.N)
            self.on_2_bt.grid(row=2, column=0)

    def second_switch(self):
        if self.is_2_on:
            self.on_2_bt_text.set('Dodaj gracza')
            self.on_2_bt.config(fg='green')
            self.on_1_bt.grid(row=1, column=0)
            self.on_3_bt.grid_forget()
            self.name2_entry.grid_forget()
            self.is_2_on = not self.is_2_on
            self.second_player_color_bt.grid_forget()
        else:
            self.on_1_bt.grid_forget()
            self.on_2_bt_text.set('Usuń gracza')
            self.on_2_bt.config(fg='red')
            self.on_3_bt_text.set('Dodaj gracza')
            self.on_3_bt.config(fg='green')
            self.is_2_on = not self.is_2_on
            self.name2_entry.grid(row=2, column=1, padx=15, pady=10, ipady=5, sticky=tk.E+tk.W+tk.N)
            self.second_player_color_bt.grid(row=2, column=2, padx=15, pady=10, ipady=5, sticky=tk.E + tk.W + tk.N)
            self.on_3_bt.grid(row=3, column=0)

    def third_switch(self):
        if self.is_3_on:
            self.on_3_bt_text.set('Dodaj gracza')
            self.on_3_bt.config(fg='green')
            self.on_2_bt.grid(row=2, column=0)
            self.on_4_bt.grid_forget()
            self.name3_entry.grid_forget()
            self.is_3_on = not self.is_3_on
            self.third_player_color_bt.grid_forget()
        else:
            self.on_2_bt.grid_forget()
            self.on_3_bt_text.set('Usuń gracza')
            self.on_3_bt.config(fg='red')
            self.on_4_bt_text.set('Dodaj gracza')
            self.on_4_bt.config(fg='green')
            self.is_3_on = not self.is_3_on
            self.name3_entry.grid(row=3, column=1, padx=15, pady=10, ipady=5, sticky=tk.E+tk.W+tk.N)
            self.third_player_color_bt.grid(row=3, column=2, padx=15, pady=10, ipady=5, sticky=tk.E + tk.W + tk.N)
            self.on_4_bt.grid(row=4, column=0)

    def fourth_switch(self):
        if self.is_4_on:
            self.on_4_bt_text.set('Dodaj gracza')
            self.on_4_bt.config(fg='green')
            self.is_4_on = not self.is_4_on
            self.on_3_bt.grid(row=3, column=0)
            self.name4_entry.grid_forget()
            self.fourth_player_color_bt.grid_forget()
        else:
            self.on_4_bt_text.set('Usuń gracza')
            self.on_4_bt.config(fg='red')
            self.is_4_on = not self.is_4_on
            self.name4_entry.grid(row=4, column=1, padx=15, pady=10, ipady=5, sticky=tk.E+tk.W+tk.N)
            self.fourth_player_color_bt.grid(row=4, column=2, padx=15, pady=10, ipady=5, sticky=tk.E + tk.W + tk.N)
            self.on_3_bt.grid_forget()

    def start_game(self):
        """Uruchamia grę.
        """
        a = self.is_1_on + self.is_2_on + self.is_3_on + self.is_4_on
        if a == 0:
            ehh = tk.Tk()
            ehh.title('Błąd')
            tk.Label(ehh, text="Nie można utworzyć gry bez graczy.\nZamknij to okno aby kontynuować", fg='red',
                     font=('Arial', 20)).pack()
            ehh.mainloop()
            return
        players = []
        if a > 0:
            players.append(Player('red', (0, 0, 0), self.name1_entry.get()))

        if a > 1:
            players.append(Player('green', (2, 0, 0), self.name2_entry.get()))
        if a > 2:
            players.append(Player('blue', (1, 0, 0), self.name3_entry.get()))
        if a > 3:
            players.append(Player('magenta', (3, 0, 0), self.name4_entry.get()))

        self.root.destroy()
        GUI(players).play()



    def __init__(self):
        self.n_players = 1
        self.is_1_on = False
        self.is_2_on = False
        self.is_3_on = False
        self.is_4_on = False

        self.root = tk.Tk()
        self.root.geometry("500x400")
        self.root.title("Ustawienia")
        # self.root.resizable(False, False)

        self.frame = tk.Frame(self.root)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)

        self.first_row_second_col = tk.Label(self.frame, text="Nazwa gracza", font=('Arial', 16))
        self.first_row_third_col = tk.Label(self.frame, text="Kolor", font=('Arial', 16))
        self.first_row_second_col.grid(row=0, column=1)
        self.first_row_third_col.grid(row=0, column=2)

        self.on_1_bt_text = tk.StringVar()
        self.on_1_bt_text.set('Dodaj gracza')
        self.on_1_bt = tk.Button(self.frame, textvariable=self.on_1_bt_text, fg='green',
                                 command=lambda: self.first_switch(), font=('Arial', 16))
        self.on_1_bt.grid(row=1, column=0)


        self.on_2_bt_text = tk.StringVar()
        self.on_2_bt_text.set('Dodaj gracza')
        self.on_2_bt = tk.Button(self.frame, textvariable=self.on_2_bt_text, fg='green',
                                 command=lambda: self.second_switch(), font=('Arial', 16))

        self.on_3_bt_text = tk.StringVar()
        self.on_3_bt_text.set('Dodaj gracza')
        self.on_3_bt = tk.Button(self.frame, textvariable=self.on_3_bt_text, fg='green',
                                 command=lambda: self.third_switch(), font=('Arial', 16))

        self.on_4_bt_text = tk.StringVar()
        self.on_4_bt_text.set('Dodaj gracza')
        self.on_4_bt = tk.Button(self.frame, textvariable=self.on_4_bt_text, fg='green',
                                 command=lambda: self.fourth_switch(), font=('Arial', 16))

        self.name1_entry = tk.Entry(self.frame, font=('Arial', 16))
        self.first_player_color_bt = tk.Button(self.frame, bg='red')
        self.name2_entry = tk.Entry(self.frame, font=('Arial', 16))
        self.second_player_color_bt = tk.Button(self.frame, bg='green')
        self.name3_entry = tk.Entry(self.frame, font=('Arial', 16))
        self.third_player_color_bt = tk.Button(self.frame, bg='blue')
        self.name4_entry = tk.Entry(self.frame, font=('Arial', 16))
        self.fourth_player_color_bt = tk.Button(self.frame, bg='magenta')

        self.start_game_bt = tk.Button(self.root, text='Rozpocznij grę', bg='green',
                                       font=('Arial', 16), command=lambda: self.start_game())
        self.start_game_bt.place(x=310, y=330)

        self.frame.pack()

    def open_game(self):
        self.root.mainloop()


ConfigGui().open_game()
