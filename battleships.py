"""
COMP.CS.100 Ohjelmointi 1
            Programming 1

Battleships

151067413
Daniil Vassilyev
daniil.vassilyev@tuni.fi


Diego Velasquez
diego.velasquez@tuni.fi
"""

ROWS = 10
COLUMNS = 10

def readInput(filename) -> dict:
    """
    Reads the input file and returns the data in a list of lists.
    """
    try:
        with open(filename) as file:
            data = file.readlines()
            data = {line.strip().split(";")[0]: line.strip().split(";")[1:] for line in data}
    except FileNotFoundError:
        print("File can not be read!")
        return
            
    # Checking if there are two different ships in the same cell
    positions = set()
    for ship_positions in data.values():
        for position in ship_positions:
            # Check if the position is valid
            if not ('A' <= position[0] <= 'J' and '0' <= position[1] <= '9'):
                print("Error in ship coordinates!")
                return
            # Check if the position is already occupied
            if position in positions:
                print(f"There are overlapping ships in the input file!")
                return
            positions.add(position)
            
    return data

#TODO Comments for classes and methods
class Ship:
    def __init__(self, name, health, positions) -> None:
        self.name = name
        self.health = health
        self.positions = positions
    
    def getPostitions(self):
        return self.positions

class gameBoard:
    def __init__(self, data) -> None:
        self.board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.shots = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.ships = {}
        for ship in data:
            for position in data[ship]:
                col = ord(position[0]) - ord('A')
                row = int(position[1])
                self.board[row][col] = ship[0]
                if ship[0] not in self.ships:
                    self.ships[ship[0]] = Ship(ship, len(data[ship]), data[ship])

    def printBoard(self) -> None:
        print("  " + " ".join(chr(ord('A') + i) for i in range(COLUMNS)))
        for i in range(ROWS):
            row = []
            for j in range(COLUMNS):
                if self.shots[i][j] == '*':
                    row.append('*')
                elif self.shots[i][j] == 'X':
                    row.append('X')
                elif self.shots[i][j] != ' ':
                    row.append(self.shots[i][j])
                else:
                    row.append(' ')
            print(f"{i} {' '.join(row)} {i}")
        print("  " + " ".join(chr(ord('A') + i) for i in range(COLUMNS)))
        print()

    def shoot(self, position) -> str:
        col = ord(position[0].upper()) - ord('A')
        row = int(position[1])
        if self.shots[row][col] != ' ':
            return "Location has already been shot at!\n"
        elif self.board[row][col] == ' ':
            self.shots[row][col] = '*'
            return ""
        else:
            self.shots[row][col] = 'X'
            ship = self.ships[self.board[row][col]]
            ship.health -= 1
            if ship.health == 0:
                for pos in ship.positions:
                    self.shots[int(pos[1])][ord(pos[0]) - ord('A')] = self.board[row][col].upper()
                return f"You sank a {ship.name}!\n"
            else:
                return ""
    
    def allSunk(self) -> bool:
        return all(ship.health == 0 for ship in self.ships.values())

def main():
    fileName = str(input('Enter file name: '))
    print()
    data = readInput(fileName)
    board = gameBoard(data)
    while True:
        board.printBoard()
        command = input("Enter place to shoot (q to quit): ")
        if command.lower() == 'q':
            print("Aborting game!")
            break
        elif len(command) != 2 or not ('a' <= command[0].lower() <= 'j' and '0' <= command[1] <= '9'):
            print("Invalid command!\n")
        else:
            result = board.shoot(command)
            print(result)
            if "You sank a" in result and board.allSunk():
                board.printBoard()
                print("Congratulations! You sank all enemy ships.")
                break
        
if __name__ == '__main__':
    main()
    