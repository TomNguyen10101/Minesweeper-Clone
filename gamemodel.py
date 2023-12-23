# Cell Class
class Cell:
    # There are 4 states for the content of the cell: Bomb (B), Flag (F), None (.), Pass (x)
    # 1. 'Flag' only being set if the user choose to flag a cell, however
    # 2. 'Bomb' will be randomize, and 'None' will be set for the rest of cells after there is no bomb left
    # to assign.
    # 3. 'Pass' will be set if the user choose to open that cell and there is no bomb on it
    def __init__(self, content):
        self.content = content
        self.value = '.'

# Game Setting Class
class GameSetting:
    def __init__(self, difficulty, timer) -> None:
        self.difSetting = {'test' : [2,2,1], 'easy': [9,9,10], 'medium':[16,16,40], 'expert': [16,30,99]}
        self.difficulty = difficulty
        self.gridHeight = self.difSetting[difficulty][0]
        self.gridWidth = self.difSetting[difficulty][1]
        self.bombNum = self.difSetting[difficulty][2]
        self.timerActive = timer