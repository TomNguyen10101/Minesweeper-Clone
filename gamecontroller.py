import random
from collections import deque
from gamemodel import Cell
from gamemodel import GameSetting

# Grid Class
class Grid:
    def __init__(self, GameSetting) -> None:
        self.height = GameSetting.gridHeight
        self.width = GameSetting.gridWidth
        self.bomb = GameSetting.bombNum
        self.lose = None
        self.win = None
        self.grid = self.GenerateGrid()
        self.totalCellWithoutBomb = (self.height * self.width) - GameSetting.bombNum
        self.cellNumToWin = self.totalCellWithoutBomb
    
    def NewGame(self):
        self.grid = self.GenerateGrid()
        print(self)
        self.cellNumToWin = (self.height * self.width) - GameSetting.bombNum

    def GenerateGrid(self):
        grid = []
        temp = []
        for _ in range(self.height):
            for _ in range(self.width):
                newCell = self.RandomizeCell()
                temp.append(newCell)
            grid.append(temp.copy())
            temp.clear()
                
        return grid
    
    def RandomizeCell(self) -> Cell:
        if self.bomb > 0:
            isBomb = random.choice([True, False, False])
            if isBomb:
                self.bomb -= 1
                return Cell('B')

        return Cell('N')
     
    # Opening up a cell at coordinate x and y
    # When openning up we do need to check if that is a bomb or not 
    def OpenCell(self, x, y) -> None:
        if self.grid[y][x].content == "B":
            self.grid[y][x].value = 'B'
            self.lose = True
            print("This is a bomb")
        elif self.grid[y][x].content == "P":
            print("This cell has opened. Please try other cell.")
            return
        else:
            print("Num of cell to win: ", self.cellNumToWin)
            self._BFS((x,y))
            if self.cellNumToWin == 0:
                self.DrawGrid()
                self.lose = False            
        return
    
    def FlagCell(self, x, y) -> None:
        if self.grid[y][x].value == '.':
            self.grid[y][x].value = 'F'
        return

    def DrawGrid(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.grid[i][j].value, end=' ')
            print()
    
    def DrawGridTest(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.grid[i][j].content, end=' ')
            print()
    

    def _BFS(self, start):
        q = deque([start])
        visited = set()
        visited.add(start)
        while q:
            x, y = q.popleft()
            if self.grid[y][x].content == 'B' or self.grid[y][x].content == 'F':
                continue
            
            # Check if the neighbors around have bombs
            numBomb = self.CheckNeighborsBomb(x,y)
            if numBomb > 0:
                self.grid[y][x].content = 'P'
                self.grid[y][x].value = f'{numBomb}'
                continue

            self.grid[y][x].content = 'P'
            self.grid[y][x].value = ''
            self.cellNumToWin -= 1
            
            if(self.cellNumToWin == 0):
                break
            
            neighbors = self._GetNeighbors(x, y)
            for neighbor in neighbors:
                if neighbor not in visited:
                    q.append(neighbor)
                    visited.add(neighbor)

    def CheckNeighborsBomb(self,x,y):
        bombAmt = 0
        # neighbors will consist of 8 cells around it
        # making sure they are in bound of the grid
        if x - 1 > -1:
            # 3 cells on the left
            if self.grid[y][x-1].content == 'B':
                bombAmt += 1
            if y - 1 > -1:
                if self.grid[y-1][x-1].content == 'B':
                    bombAmt += 1
            if y + 1 < self.height:
                if self.grid[y+1][x-1].content == 'B':
                    bombAmt += 1
        if x + 1 < self.width:
            # 3 cells on the right 
            if self.grid[y][x+1].content == 'B':
                bombAmt += 1
            if y - 1 > -1:
                if self.grid[y-1][x+1].content == 'B':
                    bombAmt += 1
            if y + 1 < self.height:
                if self.grid[y+1][x+1].content == 'B':
                    bombAmt += 1
        if y + 1 < self.height:
            if self.grid[y+1][x].content == 'B':
                bombAmt += 1
        if y - 1 > -1:
            if self.grid[y-1][x].content == 'B':
                bombAmt += 1
        return bombAmt


    def _GetNeighbors(self, x, y):
        neighbors = []

        # neighbors will consist of 8 cells around it
        # making sure they are in bound of the grid
        if x - 1 > -1:
            # 3 cells on the left
            neighbors.append((x-1, y))
            if y - 1 > -1:
                neighbors.append((x-1,y-1))
            if y + 1 < self.height:
                neighbors.append((x-1,y+1))
        if x + 1 < self.width:
            # 3 cells on the right 
            neighbors.append((x+1,y))
            if y - 1 > -1:
                neighbors.append((x+1,y-1))
            if y + 1 < self.height:
                neighbors.append((x+1,y+1))
        if y + 1 < self.height:
            neighbors.append((x,y + 1))
        if y - 1 > -1:
            neighbors.append((x, y-1))

        return neighbors
    
    def GetValue(self,x,y):
        return self.grid[y][x].value
    
def GetGrid(difficulty, timer):
    return Grid(GameSetting(difficulty=difficulty,timer=timer))
