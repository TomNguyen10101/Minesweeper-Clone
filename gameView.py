# THIS WILL BE THE VIEW OF THE GAME
import gamecontroller
import tkinter as tk 
import tkinter.ttk as ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk

# SETTING UP VARIABLES 
chosenDif = None
gameGrid = None
window = tk.Tk()
window.title("Minesweeper Clone")
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

originalMineImg = Image.open('Assets/mine.png')
originalFlagImg = Image.open('Assets/red-flag.png')
originalTransImg = Image.open('Assets/transparent.png')
resizedMineImg = originalMineImg.resize((32,32))
resizedFlagImg = originalFlagImg.resize((32,32))
resizedTransImg = originalTransImg.resize((32,32))
resizedFlagImg = ImageTk.PhotoImage(resizedFlagImg)
resizedMineImg = ImageTk.PhotoImage(resizedMineImg)
resizedTransImg = ImageTk.PhotoImage(resizedTransImg)

DifficultyOptions = ['easy', 'medium', 'expert']

def DifficultyPopUp():
    popup = tk.Toplevel(window)
    popup.title("Choose A Difficulty")
    popup.attributes("-topmost", True)

    def GetOption(option):
        global gameGrid
        global chosenDif
        try:
            gameGrid = gamecontroller.GetGrid(option, False)
            chosenDif = option
            popup.destroy()
        except Exception as e:
            print(f"Error in GetGrid: {e}")
    
    easyButton = tk.Button(popup, text="Easy", command=lambda: GetOption('easy'))
    medButton = tk.Button(popup, text='Medium', command=lambda: GetOption('medium'))
    hardButton = tk.Button(popup, text='Expert', command=lambda: GetOption('expert'))

    easyButton.pack(pady = 10)
    medButton.pack(pady = 10)
    hardButton.pack(pady = 10)

    
    popup.grab_set()
    popup.wait_window()

def MainWindow():
    topFrame = tk.Frame(master=window)
    bottomFrame = tk.Frame(master=window, borderwidth=2, relief='solid')  
    
    def TryAgainButtonClick():
        global gameGrid
        global chosenDif
        gameGrid = gamecontroller.GetGrid(chosenDif, False)        
        for widget in window.winfo_children():
            widget.destroy()
        MainWindow()

    topButton = tk.Button(master=topFrame, text=f'{chosenDif}', command=lambda:TryAgainButtonClick())
    topButton.pack(side=tk.LEFT, padx=5)
    
    # Dropdown menus for difficulties
    clicked = tk.StringVar()
    clicked.set(f'{chosenDif}')
    drop = tk.OptionMenu(topFrame, clicked, *DifficultyOptions)
    drop.pack(side=tk.LEFT, padx=5)

    def dropdownCallBack(*args):
        global chosenDif
        chosenDif = clicked.get()
        topButton.config(text=f'{chosenDif}')
        TryAgainButtonClick()
        
    # Bind the callback function to the dropdown menu
    clicked.trace_add('write', dropdownCallBack)

    def DisableAllButtons():
        for row in buttons:
            for button in row:
                button.config(state='disable')

    def Update():
        for i in range(gameGrid.height):
            for j in range(gameGrid.width):
                cellValue = gameGrid.GetValue(j,i)
                if cellValue != '.':
                    if cellValue == 'B':
                        buttons[i][j].config(image=resizedMineImg,relief=tk.SUNKEN,bg='#808080')
                    elif cellValue == 'F':
                        buttons[i][j].config(image=resizedFlagImg)
                    else:
                        buttons[i][j].config(text=cellValue,relief=tk.SUNKEN,bg='#808080')

    def ButtonLeftClick(y, x):
        gameGrid.OpenCell(x, y)
        Update()
        if gameGrid.lose:
            if gameGrid.lose:
                topButton.config(text='You Lose. Try Again?')
            else:
                topButton.config(text='You Win. Try Again?')
            DisableAllButtons()

    def ButtonRightClick(y,x):
        gameGrid.FlagCell(x,y)
        Update()

    def RightClickWrapper(row, col):
        return lambda event: ButtonRightClick(row, col)
    
    buttons = [[] for _ in range(gameGrid.height)]

    # Calculate the size to fit the button while maintaining aspect ratio
    for i in range(gameGrid.height):
        for j in range(gameGrid.width):
            button = tk.Button(master=bottomFrame, command=lambda row=i, col=j: ButtonLeftClick(row, col), compound='center',image=resizedTransImg)
            button.grid(row=i, column=j)
            button.bind("<Button-3>", RightClickWrapper(i,j))
            buttons[i].append(button)

    topFrame.pack()
    bottomFrame.pack()


# The user must enter the command to make a move on the grid
# Open command: 'open <y> <x>'
# Flag command: 'flag <y> <x>'

# print("#" * 37)
# print("## Welcome to Minesweeper Prototype ##")
# print("#" * 37)
# chosenDif = input("Enter the difficulty (easy, medium, expert): ")

# gameGrid = gamecontroller.GetGrid(chosenDif, False)

# while(gameGrid.lose == None):
#     gameGrid.DrawGrid()
#     playerMove = input("Enter your move: ").lower()
        
#     if playerMove.startswith('open') or playerMove.startswith('flag'):
#         parseMove = playerMove.split(' ')
            
#         if len(parseMove) != 3:
#             print("Not valid command. Please try again!")
#             continue
            
#         if parseMove[0] == 'open':
#             gameGrid.OpenCell(int(parseMove[2]), int(parseMove[1]))
#         elif parseMove[0] == 'flag':
#             gameGrid.FlagCell(int(parseMove[2]), int(parseMove[1]))
            
#     elif playerMove == 'quit':
#         print("Thank you for playing the game")
#         break
#     else:
#         print("Not valid command. Please try again!")
    
# #gameGrid._GetNeighbors(0,0)
# if gameGrid.lose == True:
#     print("You Lose. Thank you for playing the game.")
# elif gameGrid.lose == False:
#     print("You Win. Thank you for playing the game.")