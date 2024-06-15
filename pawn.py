class Pawn:
    def __init__(self, colour, id, spawn_coords):
        self.colour = colour
        self.id = str(id)  # Uwaga str
        self.coords = spawn_coords
        self.destination_squares_coords = [(spawn_coords[0], t, 0) for t in range(4)]
        self.is_in_destination_square = False
        self.tag = f'♟{self.id}'

    def move(self, n):  # porusza pionkiem o argument n pól po aktualnym torze
        for _ in range(n):
            if self.is_in_destination_square:
                break
            self.coords = (self.coords[0], self.coords[1], self.coords[2] + 1)
            if self.coords[2] >= 7 - 2 * self.coords[1]:
                self.coords = (self.coords[0] + 1, self.coords[1], self.coords[2] % (7 - 2 * self.coords[1]))
                if self.coords[0] == self.destination_squares_coords[0][0] + 1:
                    self.coords = self.destination_squares_coords[self.coords[1]]
                    self.is_in_destination_square = True

    def upgrade(self):  # przesówa pionek na wyższy tor (zgodnie ze schematem tzn. po skosie do tyłu)
        if self.coords[1] == 3:
            return print("Max level of pawn has been reached")
        elif self.is_in_destination_square:
            self.coords = (self.coords[0], self.coords[1] + 1, self.coords[2])
        elif self.coords[2] - 1 >= 0:
            self.coords = (self.coords[0], self.coords[1] + 1, self.coords[2] - 2)
        else:
            self.coords = (self.coords[0], self.coords[1] + 1, self.coords[2] - 1)

    def degrade(self):  # przesówa pionek na niższy tor (tylko w destination squares - przesówa po diagonali)
        if self.coords[1] == 0:
            return print("Min level of pawn has been reached")
        elif self.is_in_destination_square:
            self.coords = (self.coords[0], self.coords[1] - 1, self.coords[2])
        else:
            return print("Can't degrade pawn while not on destination square")





if __name__ == "__main__":
    A1 = Pawn('red', 0, (0,0,0))
    print(A1.destination_squares_coords)
