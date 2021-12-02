#Programmed by: Sean Quan
#Date: 6/8/19
#Description: I will be making a connect 4 game using terminal graphics
#Abstracton function and description:
    #tile = a place for a coin to be dropped
    #coin = the piece the user drops
    #board = 42 tiles in a 7 by 6 arrangement.  Top left position is 0, increasing by 1 in right direction, increasing by 7 in downward direction
        # x position determined by %7
        # y position determined by /7
        #eg: Board number 9 can be determined by taking 9 % 7 = 2 for x position, 9/7 = 1 for y position.
            #therefore, board number 9 is 2 spaces to the right and 1 space down from the top left position.

import sys
import time
def displayBoard(board):  #prints out board nicely with rows and columns from 'board' list
    row = ""
    print (" 1   2   3   4   5   6   7 ")     #helpful column numbers for the player
    endOfBoardPos = 6
    boardHeight = 6
    boardWidth = 7
    
    for pos in range(42):  #iterate through every coin.  7 columns * 6 rows = 42 tiles
        tile = board[pos]
        row = row + tile  #making row longer

        for rowCount in range(boardHeight):  #iterating through the board, row by row
            rightSide = endOfBoardPos + boardWidth*rowCount  #see if it is time to start a new row by seeing if they have hit the rightmost side
            if pos == rightSide:
                row = row + "\n"  #new row creation
                print (row)
                row = ""
            
def dropCoin(board, userChoice, coinType):  #puts coin in the board list and returns its position
    pos = 0
    yPos = 5    #so coins stack on top of each other
    xPos = userChoice - 1

    for row in range(6):
        below = xPos + row*7
        if "X" in board[below] or "O" in board[below]:
            if row == 0:   #it is out of the board, this column is full
                pos = -1       
                return pos   #negative pos indicates it is out of the board
        else:
            pos = xPos + row*7    #if there is a coin here, the position is the x position multiplied by the vertical level it is on, working from the top down
                

    #print ("The y axis position of new coin is ",yPos)
    print ("The board position is: ",pos)
    if coinType == 1:
        board[pos] = "(X) "
    elif coinType == -1:
        board[pos] = "(O) "
                  
    return pos

def winDetection(board, yPos, userChoice, coinType, realPos):  #a function to call all other functions to see if the player has won in any one of three ways
    if winHorizontal(board, yPos, userChoice, coinType) == True:
        return True
    if winVertical(board, yPos, userChoice, coinType) == True:
        return True
    if winDiagonal(board, yPos, userChoice, coinType, realPos) == True:
        return True

def winHorizontal(board, yPos, userChoice, coinType):
    coins = ["X", "O"]
    if coinType == 1:
        currentCoinType = coins[0]
    elif coinType == -1:
        currentCoinType = coins[1]

    boardHeight = 6
    boardWidth = 7
    possibleShiftsForFourInARow = boardWidth - 4  #four because you need four in a row

    for row in range(boardHeight):
        beginning = 34 - (7*row)
        for shift in range(possibleShiftsForFourInARow + 1): #in every row of 7(boardwidth) there are four possible combinations to get four in a row.  let us call each tile in the row 1 to 7.  1234 is one combination, 2345 is another, 3456 is another, and 4567 is the last one.  I used the formula totalTiles - needToWin = shifts.  that equals 7 - 4 = 3.  Add one to count the inital situation
            winCount = 0
            currentTile = board[beginning + shift]

            for x in range(1,5):  #we want the first x to be 1, not 0
                plus4Tile = board[beginning + shift + x]  #go through four times to see four in a row.  
                if currentCoinType in plus4Tile:
                    winCount += 1
                else:
                    break
            if winCount >= 4:  #need four in a row to win!
                return True
        
        
def winVertical(board, yPos, userChoice, coinType):
    coins = ['(X) ', '(O) ']
    if coinType == 1:
        currentCoinType = coins[0]
    elif coinType == -1:
        currentCoinType = coins[1]

    checkCoins = []
    check1 = []
    check2 = []
    check3 = []

    boardHeight = 6  #board is 6 tiles high
    boardLength = 7
    for row in range(boardHeight):
        currentCoinNum = (userChoice-1) + row*boardLength  #userChoice - 1 because computers count from 0
        checkCoins.append(board[currentCoinNum])  #a list of all the coins in a given column
    winCount = 0
    
    check1.append(checkCoins[0:4])  #checks positions 0,1,2,3: this is the same principal as the checkHorizontal function.  The height of any given column is 6, and you need four in a row to win.  totalTiles - coinsToWin = shifts.  Add one to take the first position into account.
    check2.append(checkCoins[1:5])  #checks positions 1,2,3,4
    check3.append(checkCoins[2:6])  #checks positions 2,3,4,5

    def seeIfSame(checkX):
        win = True  #boolean to keep track to see if they are four in a row
        same = currentCoinType  #example of a tlie with a coin
        for tile in checkX:  #iterate through the 
            if tile != same:
                win = False
                break
        if win == True:
            return True
    check1 = check1[0]  #check1 was in an unnecessary extra list, so this gets rid of it quickly
    check2 = check2[0]
    check3 = check3[0]

    if seeIfSame(check1) == True:
        return True
    elif seeIfSame(check2) == True:
        return True
    elif seeIfSame(check3) == True:
        return True


def winDiagonal(board, yPos, userChoice, coinType, realPos):
    coins = ["X", "O"]
    if coinType == 1:
        currentCoinType = coins[0]
    elif coinType == -1:
        currentCoinType = coins[1]

    boardWidth = 7
    uprightORupleft = [(boardWidth-1),(boardWidth+1)]  #to move upRight in my grid, you subtract 6.  to go to the position up left, you subtract 8
    edgeTilesR = [6,13,20,27,34]  #used to see if the checker has hit the rightside of the board 48,55,62,69,76,83
    edgeTilesL = [7,14,21,28,35] #used to see if the checker has hit the leftside of the board

    winLup = []
    winRup = []
    winLdown = []
    winRdown = []
    for x in range(1,4):  #check three spaces in every direction
        newPos = realPos + uprightORupleft[0]*x
        if newPos not in edgeTilesR and newPos < 42 and newPos > -1:  #do not wrap around the board, nor do you go above or below its boundaries
            winLdown.append(board[newPos])

        newPos = realPos - uprightORupleft[1]*x
        if newPos not in edgeTilesR and newPos < 42 and newPos > -1:
            winLup.append(board[newPos])

        newPos = realPos + uprightORupleft[1]*x
        if newPos not in edgeTilesL and newPos < 42 and newPos > -1:
            winRdown.append(board[newPos])

        newPos = realPos - uprightORupleft[0]*x
        if newPos not in edgeTilesL and newPos < 42 and newPos > -1:
            winRup.append(board[newPos])

    winCount = 1  #start at one because you need to count the coin the user puts in
    for tile in winLdown:  #checks downleft and upright, if there are 3 coins in either direction, in succession, you win 
        if currentCoinType in tile:
            winCount += 1
        else:
            break
    for tile in winRup:
        if currentCoinType in tile:
            winCount += 1
        else:
            break

    if winCount >= 4:
        return True


    winCount = 1
    for tile in winLup: #checks upleft and downright, if there are 3 coins in either direction, in succession, you win 
        if currentCoinType in tile:
            winCount += 1
        else:
            break
    for tile in winRdown:
        if currentCoinType in tile:
            winCount += 1
        else:
            break

    if winCount >= 4:
        return True
  
print ("Welcome to...\nC O N N E C T  4!!!\n")
board = []  #the board is one giant list
singleTile = "( ) "
for x in range(42):
    board.append(singleTile)     #make a board with 42 tiles
coinType = -1  #have a variable for player 1 and 2

running = True
while running:
    coinType = coinType * -1    #alternate between player 1 and player 2
    if coinType == 1:
        print ("Player 1's turn...You are 'X'\n")
    elif coinType == -1:
        print ("Player 2's turn...You are 'O'\n")
    userChoice = int(input("What column do you want to put the coin in? 1 to 7:  "))

    realPos  = dropCoin(board, userChoice, coinType)
    if realPos < 0: 
        print ("You have reached the top of the board.  Put your coin in another slot, please!\n")
        coinType = coinType * -1     #keep the player the same, so one player cannot have two turns

    displayBoard(board)
    yPos = realPos/7
    if winDetection(board, yPos, userChoice, coinType, realPos) == True:
        if coinType == 1:
            print ("Player 1 wins!!!  Congrats!")
            time.sleep(3)
            sys.exit()
        elif coinType == -1:
            print ("Player 2 wins!!!  Congrats!")
            time.sleep(3)
            sys.exit()
