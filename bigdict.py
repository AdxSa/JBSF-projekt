a = [(i, j, k) for i in range(7) for j in range(4) for k in range(7 - 2*j)]
t = [
    (0, 0),
    (1, 0),
    (2, 0),
    (3, 0),
    (4, 0),
    (5, 0),
    (6, 0),
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 1),
    (2, 2),
    (3, 2),
    (4, 2),
    (3, 3),
    (7, 0),
    (7, 1),
    (7, 2),
    (7, 3),
    (7, 4),
    (7, 5),
    (7, 6),
    (6, 1),
    (6, 2),
    (6, 3),
    (6, 4),
    (6, 5),
    (5, 2),
    (5, 3),
    (5, 4),
    (4, 3),
    (7, 7),
    (6, 7),
    (5, 7),
    (4, 7),
    (3, 7),
    (2, 7),
    (1, 7),
    (6, 6),
    (5, 6),
    (4, 6),
    (3, 6),
    (2, 6),
    (5, 5),
    (4, 5),
    (3, 5),
    (4, 4),
    (0, 7),
    (0, 6),
    (0, 5),
    (0, 4),
    (0, 3),
    (0, 2),
    (0, 1),
    (1, 6),
    (1, 5),
    (1, 4),
    (1, 3),
    (1, 2),
    (2, 5),
    (2, 4),
    (2, 3),
    (3, 4),
]
b = []
for i in range(len(t)):
    b += [(t[i][1], t[i][0])]
b = b * 4
game_to_normal_coords_dict = dict()

for i in a:
    for j in b:
        game_to_normal_coords_dict[i] = j
        b.remove(j)
        break


a = [(i, j, k) for i in range(4) for j in range(4) for k in range(7 - 2*j)]
b = []
for i in range(len(t)):
    b += [(t[i][1], t[i][0])]
normal_to_game_coords_dict = dict()

for i in b:
    for j in a:
        normal_to_game_coords_dict[i] = j
        a.remove(j)
        break
