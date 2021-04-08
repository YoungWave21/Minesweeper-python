import random


class Board:
    def __init__(self, dimension, num_bombs):
        self.num_bombs = num_bombs
        self.dim_size = dimension
        self.board = self.create_board()
        self.dug = set() # this is a set so that we can add tuples and keep track of areas where we dug
        self.assign_values()
        self.visualboard = []

    def make_visible(self):
        visible_board = []
        for i in range(self.dim_size):
            visible_board.append([])
            for n in range(self.dim_size):
                visible_board[i].append(None)
        # visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for i in range(self.dim_size):
            for n in range(self.dim_size):
                if (i, n) in self.dug:
                    visible_board[i][n] = str(self.board[i][n])
                else:
                    visible_board[i][n] = ' '
        self.visualboard = visible_board

    def create_board(self):
        board = []
        for i in range(self.dim_size):
            board.append([])
            for n in range(self.dim_size):
                board[i].append(None)

        count = 0
        while count < self.num_bombs:
            row = random.randint(0, self.dim_size) - 1
            col = random.randint(0, self.dim_size) - 1
            if board[row][col] == "X":
                continue
            count += 1
            board[row][col] = "X"
        return board

    def dig(self, row, col):
        self.dug.add((row, col))  # keep track that we dug here

        if self.board[row][col] == 'X':
            # game over
            return False
        elif self.board[row][col] > 0:
            return True

        for i in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for n in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if (i, n) in self.dug:
                    continue
                # the idea of recursion, it calls itself until it can't dig, which is when it hits a number other than 0
                self.dig(i, n)

        return True

    def visualize_board(self, bo):
        a = []
        for i in range(1, self.dim_size + 1):
            a.append(i)
        a.insert(0, "   ")
        print(*a, sep="    ")
        print("     |" + self.dim_size * " - -" + " - - - -")
        for i in range(self.dim_size):
            if i % 1 == 0 and i != 0:
                print("     |" + self.dim_size * " - -" + " - - - -")
            if i == 9:
                print(i + 1, end="  ")
            else:
                print(i + 1, end="   ")

            for j in range(len(bo[0])):
                if j % 1 == 0:
                    print(" | ", end="")

                if j == 9:
                    print(bo[i][j])
                else:
                    print(str(bo[i][j]) + " ", end="")

    def assign_values(self):
        for i in range(self.dim_size):
            for n in range(self.dim_size):
                if not self.board[i][n] == "X":
                    self.board[i][n] = self.find_neighbors(i, n)

    def find_neighbors(self, row, col):
        # goes from a cell's left to right and top to bottom to validate the number of bombs around
        total = 0
        for i in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for n in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if i == row and n == col:
                    continue
                if self.board[i][n] == "X":
                    total += 1
        return total


def main():
    minesweeper = Board(10, int(input("How many bombs would you like?: ")))
    safe = True
    # keeps going until all tiles except the bombs are dug
    while len(minesweeper.dug) < pow(minesweeper.dim_size, 2) - minesweeper.num_bombs:
        minesweeper.make_visible()
        minesweeper.visualize_board(minesweeper.visualboard)
        choice = input("Where would you like to dig? Enter as a col,row or x,y (without any spaces): ").split(",")
        row = int(choice[1]) - 1
        col = int(choice[0]) - 1
        if row < 0 or row >= minesweeper.dim_size or col < 0 or col >= minesweeper.dim_size:
            print("Invalid location. Try again.")
            continue

        # returns a True or False Boolean
        safe = minesweeper.dig(row, col)
        if not safe:
            print("SORRY GAME OVER :(")
            minesweeper.visualize_board(minesweeper.board)
            quit()
    if safe:
        print("CONGRATULATIONS!!!! YOU ARE VICTORIOUS!")
        minesweeper.visualize_board(minesweeper.board)

    else:
        print("SORRY GAME OVER :(")
        # let's reveal the whole board!
        minesweeper.visualize_board(minesweeper.board)


main()
