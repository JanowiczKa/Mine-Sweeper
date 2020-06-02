import random
import pygame
import time
import math

print(time.time())
print(time.time())

red = (255,0,0)
white = (255,255,255)
background = (222, 222, 222)

window = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Mine Sweeper")
pygame.init()

Import = pygame.image.load
clock = pygame.time.Clock()


backgroundTile = Import("./GridBackground.png")
BombIcon = Import("./Bomb - space.png")
TileIcon = Import("./Tile - space.png")
FlagIcon = Import("./Flag - space.png")
ResetIcon = Import("./ResetButton - space.png")
Background = Import("./Background.png")

Matrice = [] #Generate a Matrice with the given specifications
Bombs = [] #A list of bombs
AmountOfBombs = 36 #Default: 27
MatriceSizeX = 20 #Default: 20
MatriceSizeY = 13 #Default: 13

#print(Matrice)

def GenerateMap(MineAmount, Grid):

    Matrice.clear()
    Bombs.clear()
    row = list(range(0,MatriceSizeY))
    row = [0 * i for i in row]
    for x in range(MatriceSizeX):
        Matrice.append(row.copy())
        
    for x in range(MineAmount):
        
        PosX = random.randint(0, MatriceSizeX-1)#find a location with no mine and place a mine there
        PosY = random.randint(0, MatriceSizeY-1)
        #print("Before while PosX: {}, PosY: {}".format(PosX,PosY))
        
        while (Grid[PosX][PosY] >= 100): #100 or more is a bomb          
            PosX = random.randint(0, MatriceSizeX-1)
            PosY = random.randint(0, MatriceSizeY-1)

        #print("After while PosX: {}, PosY: {}".format(PosX,PosY))
            
        Grid[PosX][PosY] += 100
        
        #Add 1 to all adjacent tiles
        for g in range(-1,2):
            for h in range(-1,2):
                plusPosX = PosX+g
                plusPosY = PosY+h
                if (plusPosX >= 0 and plusPosX < MatriceSizeX):
                    if (plusPosY >= 0 and plusPosY < MatriceSizeY):
                        #print("Plus plusPosX: {}, plusPosY: {}".format(plusPosX,plusPosY))
                        Grid[plusPosX][plusPosY] += 1
                        
    #Replace integer matrice with tile matrice
    initialPosX = 80
    initialPosY = 104
    for x in range(0,MatriceSizeX):
        for y in range(0,MatriceSizeY):
            Grid[x][y] = Tile((initialPosX + (x * 32)),(initialPosY + (y * 32)),Grid[x][y],x,y)
            if (Grid[x][y].Bomb == True):
                Bombs.append(Grid[x][y])
        

    return Grid

def UncoverAdjactentTiles(xPosGrid, yPosGrid):

    for x in range(-1, 2):
        for y in range(-1, 2):
            
            currGridPosX = xPosGrid + x
            currGridPosY = yPosGrid + y

            if (currGridPosX >= 0 and currGridPosX <= MatriceSizeX - 1):
                if (currGridPosY >= 0 and currGridPosY <= MatriceSizeY - 1):

                    Matrice[currGridPosX][currGridPosY].Uncover()

    #print("Finished UncoverAdjacentTiles Function")

class Tile():

    def __init__(self, xPos, yPos, Number, xGrid, yGrid):

        self.xPos = xPos #Integer
        self.yPos = yPos #Integer
        self.Number = Number #Integer
        self.xGrid = xGrid
        self.yGrid = yGrid

        self.Bomb = False
        if Number >= 90:
            self.Bomb = True            

        self.Flagged = False
        self.Covered = True
        self.Size = 32
      
        self.font = pygame.font.Font("freesansbold.ttf", 25)
        self.text = self.font.render(str(self.Number), True, (0,0,0))
        self.numberPos = (self.xPos + 16 - self.text.get_width()/2,
                          self.yPos + 18 - self.text.get_height()/2)

    def DisplayTile(self):

        window.blit(backgroundTile,(self.xPos, self.yPos))

        if (self.Bomb):
            window.blit(BombIcon,(self.xPos, self.yPos))
        else:
            if (self.Number != 0):
                window.blit(self.text, self.numberPos)

        if (self.Covered):
            window.blit(TileIcon,(self.xPos, self.yPos))

        if (self.Flagged):
            window.blit(FlagIcon,(self.xPos, self.yPos))

    def Click(self, mousePos, flag):
            
        if ((mousePos[0] >= self.xPos) and (mousePos[0] < self.xPos + self.Size)):
            if ((mousePos[1] >= self.yPos) and (mousePos[1] < self.yPos + self.Size)):
                
                if ((flag == True) and (self.Covered == True)):
                    self.Flagged = not(self.Flagged)
                elif((self.Flagged == False) and (self.Covered == True)):
                    self.Uncover()

    def Uncover(self):
        if((self.Flagged == False) and (self.Covered == True)):
            self.Covered = False
            if self.Number == 0:
                UncoverAdjactentTiles(self.xGrid, self.yGrid)

    def getCover(self):
        return self.Covered
 
    def getFlag(self):
        return self.Flagged    

class Timer():

    def __init__(self, xPos, yPos, running = False):
        self.startTime = time.time()
        self.currentTime = self.startTime
        self.displayTime = 0
        self.xPos = xPos
        self.yPos = yPos
        self.running = running

        self.font = pygame.font.Font("freesansbold.ttf", 35)

    def resetTimer(self):
        self.running = False
        self.startTime = time.time()
        self.currentTime = self.startTime
        self.displayTime = 0

    def updateTimer(self):
        if self.running == True:
            self.currentTime = time.time()
            self.displayTime = self.startTime - self.currentTime

    def startTimer(self):
        self.resetTimer()
        self.running = True

    def displayTimer(self):

        newText = "{0:.2f}".format(round(-self.displayTime,2))
        self.text = self.font.render(newText, True, (0,0,0))
        
        text_width, text_height = self.font.size(newText)
        self.numberPos = (400 - text_width/2, self.yPos)
        
        window.blit(self.text, self.numberPos)

class ResetButton():

    def __init__(self, xPos, yPos, Timer, grid):
        self.xPos = xPos
        self.yPos = yPos
        self.Size = 64
        self.gameTimer = Timer
        self.gameGrid = grid
        
    def displayButton(self):
        window.blit(ResetIcon,(self.xPos, self.yPos))
        
    def checkClick(self, mousePos):
        
        if ((mousePos[0] >= self.xPos) and (mousePos[0] < self.xPos + self.Size)):
            if ((mousePos[1] >= self.yPos) and (mousePos[1] < self.yPos + self.Size)):
                self.ResetGame()
                return True

    def ResetGame(self):
        self.gameGrid = GenerateMap(AmountOfBombs, self.gameGrid)
        self.gameTimer.resetTimer()
    
def Update():

    timer = Timer(650, 35, False)

    gameIsRunning = True

    gameFinished = False
    
    resetButton = ResetButton(80, 20, timer, Matrice)
    
    while gameIsRunning:
        
        
        mouse_pos = pygame.mouse.get_pos()     

        for event in pygame.event.get():

            if event.type == pygame.QUIT:           
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if (resetButton.checkClick(mouse_pos)):
                    gameFinished = False
                
                if (gameFinished == False):
                    for x in range(0,MatriceSizeX): #Check if a tile was clicked
                        for y in range(0,MatriceSizeY):
                            if (event.button == 1):
                                Matrice[x][y].Click(mouse_pos, False)
                            if (event.button == 3):
                                Matrice[x][y].Click(mouse_pos, True)

                    if (mouse_pos[1] >= 104 and mouse_pos[1] <= 104 + (32*MatriceSizeY)):
                        if (mouse_pos[0] >= 80 and mouse_pos[0] <= 80 + (32*MatriceSizeX)):
                            #print("yas")
                            if (timer.running == False):
                                timer.startTimer()
            
        window.fill(background)

        window.blit(Background,(0,0))

        for x in range(0,MatriceSizeX): #Display the Tiles
            for y in range(0,MatriceSizeY):
                Matrice[x][y].DisplayTile()

        timer.updateTimer()
        timer.displayTimer()

        resetButton.displayButton()

        bombTotal = len(Bombs)
        flagged = 0
        for x in range(len(Bombs)): #Check if all the bombs have been flagged (Win condition) or uncovered (Lose Condition)
            
            if (Bombs[x].getCover() == False):
                #print("You Lose!!!")
                timer.running = False
                gameFinished = True
                break
            
            if (Bombs[x].getFlag() == True):
                flagged += 1         
            
            if (flagged == bombTotal):
                #print("You Win!!!")
                timer.running = False
                gameFinished = True

        
        pygame.display.update()
        clock.tick(60)

#Sets up the game
Matrice = GenerateMap(AmountOfBombs, Matrice)
#print(Matrice)
Update()
