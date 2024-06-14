from Player import Player


class Chessboard:
    def __init__(self, players):
        self.win_condition = False
        self.players = players  # jako lista graczy
        self.pawns = []  # lista krotek ('colour', id, coords) wszystkich pionków wszystkich graczy
        self.squares = {(i, j, k) : False for i in range(4) for j in range(4) for k in range(7 - 2*j)}
        # coords = (bok, tor, pole na boku (modulo 7)), bool czy jest tam gracz

    def refresh_pawns_info(self):
        self.pawns = []
        for player in self.players:
            for pawn in player.pawns:
                self.pawns += [(pawn.colour, pawn.id, pawn.coords)]

    def play(self):
        print(f"commands: \n"
              f"create pawn"
              f"choose pawn \n"
              f"move pawn \n"
              f"roll dice \n"
              f"upgrade pawn \n"
              f"degrade pawn \n"
              f"show pawns (shows positions of pawns) \n"
              f"stop (next player)\n")
        while True:
            for player in self.players:
                print(f"Tura gracza {player}")
                player.rolled = False
                while True:
                    t = input('Command:   ')
                    if t == 'stop':
                        player.rollen = False
                        break
                    elif t == 'show pawns':
                        self.refresh_pawns_info()
                        for i in self.pawns:
                            if i[0] == player.colour:
                                print(f'pionek o id = {i[1]} jest na polu {i[2]} (sektor, poziom, kratka)')
                    else:
                        player.action(t)




if __name__ == "__main__":
    Adam = Player('purple', (0, 0, 0), 'Adam')
    Adam2 = Player('green', (2, 0, 0), 'Żuku')
    chess = Chessboard([Adam, Adam2])
    print(chess.squares)
    chess.play()
    print(chess.squares)