
import pygame, os, time, random
os.system('cls')

def drawCell():
    global occCells
    pos = pygame.mouse.get_pos()
    newX =  pygame.mouse.get_pos()[0] - (pygame.mouse.get_pos()[0] % cellDim)
    newY =  pygame.mouse.get_pos()[1] - (pygame.mouse.get_pos()[1] % cellDim)

    if (newX,newY) not in occCells:
        occCells.append((newX,newY))
        pygame.draw.rect(screen, cellColour, pygame.Rect(newX,newY,cellDim,cellDim))


def spawnCell(cell):
    global occCells
    X = cell[0]
    Y = cell[1]

    occCells.append((X,Y))
    pygame.draw.rect(screen, cellColour, pygame.Rect(X,Y,cellDim,cellDim))

def killCell(cell):
    X = cell[0]
    Y = cell[1]

    pygame.draw.rect(screen, (255,255,255), pygame.Rect(X,Y,cellDim,cellDim))

def getNumSurrounding(cellPos):
    numSurrounding = 0
    cellX = cellPos[0]
    cellY = cellPos[1]

    if screen.get_at((cellX+cellDim,cellY)) == cellColour:
        numSurrounding += 1

    if screen.get_at((cellX-cellDim,cellY)) == cellColour:
        numSurrounding += 1

    if screen.get_at((cellX,cellY+cellDim)) == cellColour:
        numSurrounding += 1

    if screen.get_at((cellX,cellY-cellDim)) == cellColour:
        numSurrounding += 1

    if screen.get_at((cellX+cellDim,cellY+cellDim)) == cellColour:
        numSurrounding += 1

    if screen.get_at((cellX-cellDim,cellY-cellDim)) == cellColour:
        numSurrounding += 1

    if screen.get_at((cellX+cellDim,cellY-cellDim)) == cellColour:
        numSurrounding += 1

    if screen.get_at((cellX-cellDim,cellY+cellDim)) == cellColour:
        numSurrounding += 1

    return numSurrounding

def getSpawnCells():
    spawnCells = []
    checkCells = []
    for cellPos in occCells: #gets 8 surrounding cells of each coloured cell
        checkCells.append((cellPos[0]+cellDim,cellPos[1]))
        checkCells.append((cellPos[0]-cellDim,cellPos[1]))
        checkCells.append((cellPos[0],cellPos[1]+cellDim))
        checkCells.append((cellPos[0],cellPos[1]-cellDim))
        checkCells.append((cellPos[0]+cellDim,cellPos[1]+cellDim))
        checkCells.append((cellPos[0]-cellDim,cellPos[1]-cellDim))
        checkCells.append((cellPos[0]+cellDim,cellPos[1]-cellDim))
        checkCells.append((cellPos[0]-cellDim,cellPos[1]+cellDim))
        
    for index in range(len(checkCells)):
        cell = checkCells[index]
        try:
            if screen.get_at(cell) == (255,255,255):
                numSurrounding = getNumSurrounding(cell)
                #if numSurrounding == spawnState:
                if numSurrounding in spawnNums: 
                    if cell not in spawnCells:
                        spawnCells.append(cell)
        except:
            pass
    return spawnCells

def getKillCells():
    killSpots = []
    for index in range(len(occCells)):
        numSurrounding = getNumSurrounding(occCells[index])
        # if numSurrounding < lowDeath:
        #     killSpots.append(index)

        # if numSurrounding > highDeath: 
        #     killSpots.append(index)
    
        if numSurrounding not in surviveNums:
            killSpots.append(index)

    return killSpots

cellDim = 10
cellColour = (0,0,0)

highDeath = 3
lowDeath = 2
spawnState = 3


#https://www.conwaylife.com/wiki/List_of_Life-like_cellular_automata
#B - Spawn states, S - Survive states

#favourite:
#walled cities - B45678/S2345
#slow blob - B367/S125678
#mazectric - B3/S1234
#conway's life - B3/S23
#dense bugs - B45678/S4567
#flashing expanse B2348/S123


ruleString = 'B3/S23' # CHANGE THIS TO MODIFY RULES

if ruleString == '': # random rule
    ruleString += 'B'
    for i in range(8):
        if random.randint(0,1) == 1:
            ruleString += str(i+1)
    
    ruleString += '/S'
    for i in range(8):
        if random.randint(0,1) == 1:
            ruleString += str(i+1)

spawnNums = []
surviveNums = []

writeSurvive = False
for char in ruleString:
    if char.isnumeric():
        if writeSurvive:
            surviveNums.append(int(char))
        else:
            spawnNums.append(int(char))
    elif char == '/':
        writeSurvive = True

size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.init()

screen.fill((255,255,255))

playGame = False
print('Simulation Paused')
print('Rule:',ruleString, '| Left Mouse -> Draw   Right Mouse -> Clear   Space -> Pause')
occCells = []
while True:

    mouse = pygame.mouse.get_pressed()
    if mouse[0]:
        drawCell()
    if mouse[2]:
        occCells = []
        screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:

                os.system('cls')
                if playGame == True:
                    playGame = False
                    print('Simulation Paused')
                    print('Rule:',ruleString, '| Left Mouse -> Draw   Right Mouse -> Clear  Space -> Pause')

                else:
                    playGame = True
                    print('Running Simulation (Pause simulation to draw)')
                    print('Rule:',ruleString, '| Left Mouse -> Draw   Right Mouse -> Clear  Space -> Pause')
    
    if playGame == True:
        spawnCells = getSpawnCells()
        killCells = getKillCells()

        for cell in spawnCells:
            spawnCell(cell)

        for index in killCells:
            killCell(occCells[index])

        for index in range(len(killCells)):
            occCells.pop(killCells[index]-index)
        
        time.sleep(0.05)

    pygame.display.update()
