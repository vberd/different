from random import random, choice

class Game_2048():
    def __init__(self, N=3, G = True):
        self.N = N
        self.field = [['_'] * N for i in range(N)]
        self.G = G
        self.free_tiles = [i for i in range(N*N)]
        self.ocup_tiles = []
        self.move = False
        self.result = 0
    def __getitem__(self, index):
        return self.field[index]

    def __str__(self):
        prnt = '\n'.join(' '.join(map(str, game[i])) for i in range(self.N))
        return prnt

    def add_tile(self):
        if len(self.ocup_tiles) == 0:
            for i in range(2):
                    i = choice(self.free_tiles)
                    self.field[i//self.N][i%self.N] = 2
                    self.free_tiles.remove(i)
                    self.ocup_tiles.append(i)
        elif len(self.free_tiles) > 0:
            i = choice(self.free_tiles)
            if random() > 0.2:
                self.field[i//self.N][i%self.N] = 2
            else: self.field[i//self.N][i%self.N] = 4
            self.free_tiles.remove(i)
            self.ocup_tiles.append(i)

    def up(self):
        print("Up")
        self.ocup_tiles.sort()
        oc_tiles = self.ocup_tiles[:]
        for i in oc_tiles:
            k = 0

            j = i
            while (i >= self.N) and True:
                j -= self.N
                if (j >= 0) and (self.field[j // self.N][j % self.N] == '_'):
                    k += 1
                    self.move = True
                    pass
                elif (j >= 0) and (self.field[(j) // self.N][(j) % self.N] == (self.field[(j + self.N * k + self.N) // self.N][(j + self.N * k + self.N) % self.N])):
                    k += 1
                    self.move = True
                    self.ocup_tiles.remove(i)
                    self.free_tiles.append(i)
                    self.field[(i - self.N * k) // self.N][(i - self.N * k) % self.N] *= 2
                    self.result += self.field[(i - self.N * k) // self.N][(i - self.N * k) % self.N]
                    self.field[(i) // self.N][(i) % self.N] = '_'
                    break
                elif k == 0:
                    break
                else:
                    self.ocup_tiles.remove(i)
                    self.ocup_tiles.insert(0, i - self.N*k)
                    self.free_tiles.remove(i - self.N * k)
                    self.free_tiles.append(i)
                    self.field[(i - self.N * k) // self.N][(i - self.N * k) % self.N] = self.field[(i) // self.N][(i) % self.N]
                    self.field[(i) // self.N][(i) % self.N] = '_'
                    break

    def down(self):
        print("Down")
        self.ocup_tiles.sort(reverse=True)
        oc_tiles = self.ocup_tiles[:]
        for i in oc_tiles:
            k = 0
            j = i
            while (i < (self.N ** 2 - self.N )) and True:
                j += self.N
                if (j < (self.N ** 2 )) and (self.field[j // self.N][j % self.N] == '_'):
                    k += 1
                    self.move = True
                    pass
                elif (j < (self.N ** 2 )) and (self.field[(j) // self.N][(j) % self.N] == (self.field[(j - self.N * k - self.N) // self.N][(j - self.N * k - self.N) % self.N])):
                    k += 1
                    self.move = True
                    self.ocup_tiles.remove(i)
                    self.free_tiles.append(i)
                    self.field[(i + self.N * k) // self.N][(i + self.N * k) % self.N] *= 2
                    self.result += self.field[(i + self.N * k) // self.N][(i + self.N * k) % self.N]
                    self.field[(i) // self.N][(i) % self.N] = '_'
                    break
                elif k == 0: break
                else:
                    self.ocup_tiles.remove(i)
                    self.ocup_tiles.insert(0, i + self.N*k)
                    self.free_tiles.remove(i + self.N * k)
                    self.free_tiles.append(i)
                    self.field[(i + self.N * k) // self.N][(i + self.N * k) % self.N] = self.field[(i) // self.N][(i) % self.N]
                    self.field[(i) // self.N][(i) % self.N] = '_'
                    break

    def left(self):
        print("Left")
        self.ocup_tiles.sort()
        oc_tiles = self.ocup_tiles[:]
        for i in oc_tiles:
            k = 0
            j = i
            while (i % self.N > 0 ) and True:
                j -= 1
                if (j // self.N == i // self.N) and (self.field[j // self.N][j % self.N] == '_'):
                    k += 1
                    self.move = True
                    pass
                elif (j // self.N == i // self.N) and (self.field[(j) // self.N][(j) % self.N] == (self.field[(j + 1 + k) // self.N][(j + 1 + k) % self.N])):
                    k += 1
                    self.move = True
                    self.ocup_tiles.remove(i)
                    self.free_tiles.append(i)
                    self.field[(i - k) // self.N][(i - k) % self.N] *= 2
                    self.result += self.field[(i - k) // self.N][(i - k) % self.N]
                    self.field[(i) // self.N][(i) % self.N] = '_'
                    break
                elif k == 0:

                    break
                else:
                    self.ocup_tiles.remove(i)
                    self.ocup_tiles.insert(0, i - k)
                    self.free_tiles.remove(i - k)
                    self.free_tiles.append(i)
                    self.field[(i - k) // self.N][(i - k) % self.N] = self.field[(i) // self.N][(i) % self.N]
                    self.field[(i) // self.N][(i) % self.N] = '_'
                    break

    def right(self):
        print ("Right")
        self.ocup_tiles.sort(reverse=True)
        oc_tiles = self.ocup_tiles[:]
        for i in oc_tiles:
            k = 0
            j = i
            while (i % self.N < (self.N - 1) ) and True:
                j += 1
                if (j // self.N == i // self.N) and (self.field[j // self.N][j % self.N] == '_'):
                    k += 1
                    self.move = True
                    pass
                elif (j // self.N == i // self.N) and (self.field[(j) // self.N][(j) % self.N] == (self.field[(j - 1 - k) // self.N][(j - 1 - k) % self.N])):
                    k += 1
                    self.move = True
                    self.ocup_tiles.remove(i)
                    self.free_tiles.append(i)
                    self.field[(i + k) // self.N][(i + k) % self.N] *= 2
                    self.result += self.field[(i + k) // self.N][(i + k) % self.N]
                    self.field[(i) // self.N][(i) % self.N] = '_'
                    break
                elif k == 0: break
                else:
                    self.ocup_tiles.remove(i)
                    self.ocup_tiles.insert(0, i + k)
                    self.free_tiles.remove(i + k)
                    self.free_tiles.append(i)
                    self.field[(i + k) // self.N][(i + k) % self.N] = self.field[(i) // self.N][(i) % self.N]
                    self.field[(i) // self.N][(i) % self.N] = '_'
                    break

    def test_move(self):
        self.ocup_tiles.sort()
        oc_tiles = self.ocup_tiles[:]
        t_move = True

        if len(self.free_tiles) == 0:
            t_move = False
            for i in oc_tiles:
                if i // self.N != 0:
                    i_up = i - self.N
                else: i_up = i + self.N

                if i // self.N != self.N - 1:
                    i_down = i + self.N
                else: i_down = i - self.N

                if i % self.N != 0:
                    i_left =  i - 1
                else: i_left = i + 1

                if i % self.N != self.N - 1:
                    i_right = i + 1
                else: i_right = i - 1

                if (self.field[i // self.N][i % self.N] == self.field[i_up // self.N][i_up % self.N]) or (
                    self.field[i // self.N][i % self.N] == self.field[i_down // self.N][i_down % self.N]) or (
                    self.field[i // self.N][i % self.N] == self.field[i_left // self.N][i_left % self.N]) or (
                    self.field[i // self.N][i % self.N] == self.field[i_right // self.N][i_right % self.N]):
                    t_move = True
        if t_move != True:
            self.end()

    def end(self):
        print("END")
        print("Score: ", game.result)
        exit()

game = Game_2048()

game.add_tile()
print(game)
while True:
    game.test_move()
    print("Score: ", game.result)
    print("Select side. Up = u, Down = d, Left = l, Right = r, Exit = E")
    action = input()
    game.move = False
    if action == "E":
        game.end()
    elif action in ('l','r','u','d'):
        if action == "l":
            game.left()
        elif action == "r":
            game.right()
        elif action == "u":
            game.up()
        elif action == "d":
            game.down()
        if game.move == True:
            game.add_tile()
        else: print("----- No matching moves -----")
    else: print("Incorrect side. Select side. Up = u, Down = d, Left = l, Right = r, Exit = E")
    print(game)
