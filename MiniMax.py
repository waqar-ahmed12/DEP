import tkinter as tk

root = tk.Tk()

winner = None

global state

def checkWin(player):
    for row in state:   # check row winning conditions
        if all(s == player for s in row):
            return True
        
    for col in range(3):    # check column winning conditions
        if all(state[row][col] == player for row in range(3)):
            return True
        
    # check diagonal winnings
    if all(state[i][i] == player for i in range(3)): 
        return True
    
    if all(state[i][2 - i] == player for i in range(3)):
        return True
    return False

def isTie():
    return all(all(cell != '' for cell in row) for row in state)

def checkLine(button1, button2, button3):   # this returns false or true to disable buttons calledin 
    if button1['text'] == button2['text'] == button3['text'] and button1['text'] in ["X", "O"]:
        button1.config(bg="green")
        button2.config(bg="green")
        button3.config(bg="green")

        global winner
        winner = button1['text']
        return True
    return False


def disable(buttons):
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state='disabled')  
        

def checkEnd(buttons):
    if (checkLine(buttons[0][0], buttons[0][1], buttons[0][2]) or
        checkLine(buttons[1][0], buttons[1][1], buttons[1][2]) or
        checkLine(buttons[2][0], buttons[2][1], buttons[2][2]) or
        checkLine(buttons[0][0], buttons[1][0], buttons[2][0]) or
        checkLine(buttons[0][1], buttons[1][1], buttons[2][1]) or
        checkLine(buttons[0][2], buttons[1][2], buttons[2][2]) or
        checkLine(buttons[0][0], buttons[1][1], buttons[2][2]) or
        checkLine(buttons[0][2], buttons[1][1], buttons[2][0])):

        global gameEnd
        gameEnd = True

        disable(buttons)

                  
def MiniMax(state, buttons, depth, isMaximizingPlayer):
    
    if checkWin('O'):
        return -1
    if checkWin('X'):
        return 1
    if isTie():
        return 0
        

    if(isMaximizingPlayer):
        bestScore = -10 # simulating -Infinity

        for i in range(3):
            for j in range(3):
                if(state[i][j] == ''):
                    state[i][j] = "X"
                    score = MiniMax(state, buttons, depth+1, False)
                    state[i][j] = ''

                    bestScore = max(score, bestScore)
                
        return bestScore
    
    else:
        bestScore = 10

        for i in range(3):
            for j in range(3):
                if(state[i][j] == ''):
                    state[i][j] = "O"
                    score = MiniMax(state, buttons, depth+1, True)
                    state[i][j] = ''
                    
                    bestScore = min(score, bestScore)
                    
        return bestScore

def Action(state):
    places = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == "":
                places.append((i, j))
    return places


def ComputerPlay(state, buttonList):
    
    action = Action(state)
    bestScore = -10
    bestMove = None


    if len(action) != 0:
        for actions in action:
            
            row, col = actions 
            state[row][col] = "X"
            
            score = MiniMax(state, buttonList, 0, False)
            
            state[row][col] = ""
            

            if score > bestScore:
                bestScore = score
                bestMove = actions
        
    if bestMove:
        row, col = bestMove
        buttons[row][col].config(text='X', state='disabled')
        state[row][col] = "X"
        checkEnd(buttons)
    

global turn
turn = False
gameEnd = False

def function(state, button, i, j, buttons):
    
    global turn   
    global gameEnd   
    
    if not turn:
        button.config(text='O', state = 'disabled')
        button.config(disabledforeground=button.cget('foreground'))
        state[i][j] = 'O'
        checkEnd(buttons)
        
        if not gameEnd:
            ComputerPlay(state, buttons)
            checkEnd(buttons)
        
buttons = []    # a button array to manage the buttons

state = []   # this is the state of the game

for i in range(3):
    temp = []
    tempButton = []
    for j in range(3):
        button = tk.Button(root, padx=80, pady=80, text="   ", font=('Karla', 18))
        
        button.config(command=lambda state=state, button=button, i=i, j=j, buttons=buttons: function(state, button, i, j, buttons))
        button.grid(row=i, column=j)

        temp.append("")
        tempButton.append(button)
    state.append(temp)
    buttons.append(tempButton)

root.mainloop()
