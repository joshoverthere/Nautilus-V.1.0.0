# Simple pygame program
from cairo import ANTIALIAS_DEFAULT
import pygame
import random
import math
import time
import tkinter
from tkinter import *
from tkinter import messagebox


pygame.init()
screen = pygame.display.set_mode([1400,600])
random.seed(time.process_time())


class Cell:
    def __init__(self, dnaa, x, y):
        self.dna = dnaa
        self.posx = x
        self.posy = y
        self.proteinA = 0
        self.proteinB = 0
        self.proteinC = 0
        self.proteinD = 0
        self.proteinE = 0
        self.currentEnergy = 100

    def calculateMovement(self):
        foodDistances = {}

        for food in foods:
            foodDistances[foods.index(food)] = getDistanceBetween(self.posx, self.posy, food.posx, food.posy)


        nearestFood = min(foodDistances, key=foodDistances.get)
        

        xDisplacement = foods[nearestFood].posx - self.posx
        yDisplacement = foods[nearestFood].posy - self.posy


        print("Cell coordinates: [", self.posx, ",", self.posy, "]")
        print("Food coordinates: [", foods[nearestFood].posx, ",", foods[nearestFood].posy, "]")
        print("Number of glucose receptors: ", self.dna["glucoseReceptors"])
        print(xDisplacement, yDisplacement)

        try:
            angleOfDirection = math.degrees(math.atan(yDisplacement/xDisplacement))
        except:
            angleOfDirection = 0
        distanceToFood = math.sqrt((xDisplacement * xDisplacement) + (yDisplacement * yDisplacement))
        print("Distance to food: ", distanceToFood)

        if (self.dna["glucoseReceptors"]*5 + self.dna["diameter"]) >= distanceToFood:
            if self.currentEnergy >= distanceToFood:
                print("ATE A FOOD.")
                self.posx = foods[nearestFood].posx
                self.posy = foods[nearestFood].posy
                del foods[nearestFood]
                self.currentEnergy -= distanceToFood
                self.currentEnergy += 50
            else:
                print("MOVED TOWARDS A FOOD.")
                self.posx += self.currentEnergy * math.cos(angleOfDirection)
                self.posy += self.currentEnergy * math.sin(angleOfDirection)
                self.currentEnergy = 0

        print("Angle of direction: ", angleOfDirection)

class Food:
    def __init__(self, glucs, x, y):
        self.glucs = glucs
        self.posx = x
        self.posy = y



def drawCell(diameter, posx, posy, wallThickness):
    pygame.draw.circle(screen, (0, 0, 0), (posx, posy), diameter, wallThickness)
    pygame.draw.circle(screen, (255,255,255), (posx, posy), (diameter-wallThickness))

def drawCellRange(posx, posy, grange):
    pygame.draw.circle(screen, (179, 92, 255), (posx, posy), grange)

def drawFood(posx, posy):
    pygame.draw.circle(screen, (219,153,100), (posx, posy), 3)

def updateEnvironment(cells, foods):
    screen.fill((59, 94, 255))
    print("Updating environment...")

    for cell in cells:
        if cell.dna["glucoseReceptors"]>0:
            drawCellRange(cell.posx, cell.posy, ((cell.dna["glucoseReceptors"]*5)+cell.dna["diameter"]))
    
    for cell in cells:
        drawCell(cell.dna["diameter"], cell.posx, cell.posy, 1)

    for food in foods:
        drawFood(food.posx, food.posy)

    refreshSidebar()
    pygame.display.flip()

def getDistanceBetween(x1, y1, x2, y2):
    distanceBetween = 0
    distanceBetween = math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))
    return distanceBetween

def generateValidSpot(spotWidth, spotHeight):
    #print("Finding a valid spot of size [", spotWidth, " , ", spotHeight, "]")
    foundValidSpot = False
    randx = 0
    randy = 0

    while foundValidSpot == False:
        randx = random.randint(30,1070)
        randy = random.randint(30,570)
        foundValidSpot = True

        for cell in cells:
            distanceBetween = getDistanceBetween(cell.posx, cell.posy, randx, randy)
            #print("Distance between [", randx, " , ", randy, "] and [", cell.posx, " , ", cell.posy, "] is: ", distanceBetween)
            if (distanceBetween < (spotWidth + cell.dna["diameter"] + 2)):
                foundValidSpot = False



        for food in foods:
            distanceBetween = getDistanceBetween(food.posx, food.posy, randx, randy)
            if (distanceBetween < (spotWidth + 3 + 1)):
                foundValidSpot = False


    return randx, randy


def getCellDetails(cell):
    print(cell.dna)
    print(cell.posx)
    print(cell.posy)

def fillEnvironmentWithFood(amount):
    for x in range(amount):
        foodSpawnSpot = generateValidSpot(3,3)
        foods.append(Food(1, foodSpawnSpot[0], foodSpawnSpot[1]))
        if len(foods)%100==0:
            print("Added food ", x)


def spawnRandomCell():
    dna = {}

    dna["mitochondria"] = []
    numberOfMitochondria = random.randint(0,5)

    for x in range(0,numberOfMitochondria):
        dna["mitochondria"] += [[random.randint(50, 99), random.randint(1,2)]] # efficiency could vary from 50-99%, capacity could vary from 1-2 glucose molecules at a time.
    
    dna["ribosomes"] = []
    numberOfRibosomes = random.randint(0,5)

    for x in range(0,numberOfRibosomes):
        dna["ribosomes"] += [[random.randint(50,99), random.randint(1,2)]] # efficiency varies 50-99%, ribosome could process either 1 or 2 proteins at a time.



    hasFlagella = random.randint(0,1)

    if hasFlagella == True:
        dna["flagella"] = []
        dna["flagella"] += [random.randint(3,10), random.randint(10,90), random.randint(1,3)] 

    dna["chloroplasts"] = []
    numberOfChloroplasts = random.randint(0,5)

    for x in range(0,numberOfChloroplasts):
        dna["chloroplasts"] += [[random.randint(5,20)]] #energy output of chloroplast could vary from 5-20 per minute


    dna["glucoseReceptors"] = random.randint(0,10)
    dna["proteinAReceptors"] = random.randint(0,10)
    dna["proteinBReceptors"] = random.randint(0,10)
    dna["proteinCReceptors"] = random.randint(0,10)
    dna["proteinDReceptors"] = random.randint(0,10)
    dna["proteinEReceptors"] = random.randint(0,10)
    dna["energyEfficiency"] = random.randint(60,90)
    dna["proteinEfficiency"] = random.randint(60,90)
    dna["thermalEnergyLoss"] = random.randint(5,20)
    dna["agingFactor"] = random.randint(85,99)
    dna["wallType"] = random.randint(1,8)
    dna["wallThickness"] = random.randint(1,3)
    dna["diameter"] = random.randint(5, 10)



    randomSpawnSpot = generateValidSpot(dna["diameter"], dna["diameter"])

    dna["spawnx"] = randomSpawnSpot[0]
    dna["spawny"] = randomSpawnSpot[1]


    cells.append(Cell(dna, dna["spawnx"], dna["spawny"]))

def getPopulation():
    return len(cells)

def getWeakestCell():
    energyAmounts = {}
    for cell in cells:
        energyAmounts[cells.index(cell)] = cell.currentEnergy

    weakestCell = int(min(energyAmounts, key=energyAmounts.get))
    weakestCellEnergy = int(energyAmounts[weakestCell])

    return [weakestCell, weakestCellEnergy]

def getStrongestCell():
    energyAmounts = {}
    for cell in cells:
        energyAmounts[cells.index(cell)] = cell.currentEnergy

    strongestCell = int(max(energyAmounts, key=energyAmounts.get))
    strongestCellEnergy = int(energyAmounts[strongestCell])
    return [strongestCell, strongestCellEnergy]

def refreshSidebar():
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(1100, 0, 400, 600))
    font = pygame.font.SysFont(None, 30)
    img4 = font.render(('Minute: ' + str(minute)), True, (255,255,255))
    screen.blit(img4, (1150, 75))



    font = pygame.font.SysFont(None, 30)
    img = font.render(('Population: ' + str(getPopulation())), True, (255,255,255))
    screen.blit(img, (1150, 100))

    font = pygame.font.SysFont(None, 20)
    img2 = font.render(('Strongest Cell: ' + str(getStrongestCell()[0]) + ',   Energy: ' + str(getStrongestCell()[1])), True, (255,255,255))
    screen.blit(img2, (1150, 125))

    font = pygame.font.SysFont(None, 20)
    img3 = font.render(('Weakest Cell: ' + str(getWeakestCell()[0]) + ",   Energy: " + str(getWeakestCell()[1])), True, (255,255,255))
    screen.blit(img3, (1150, 150))

    pygame.display.update()


running = True

cells = []
foods = []
minute = 0


screen.fill((0, 23, 128))

for x in range(0,100):
    spawnRandomCell()
    print("Spawning cell ", x)




while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    updateEnvironment(cells, foods)



    yeah = 1
    time.sleep(3)
    fillEnvironmentWithFood(2000)
    for x in range(0,100000):
        cellsDied = []
        minute += 1
        fillEnvironmentWithFood(random.randint(1,8))

        for cell in cells:
            cell.currentEnergy -= cell.dna["thermalEnergyLoss"]
            cell.calculateMovement()
            
            if cell.currentEnergy <= 0:
                cellsDied.append(str(cells.index(cell)))
                cells.remove(cell)

        cellsDiedString = ""
        for deadCell in cellsDied:
            cellsDiedString += (deadCell + ", ")

        if len(cellsDiedString)>0:
            Tk().wm_withdraw()
            tkinter.messagebox.showinfo(title="Cell Death", message=("Cell " + cellsDiedString + " died."))
        
        updateEnvironment(cells, foods)
    



    time.sleep(10000)
        




# Done! Time to quit.
pygame.quit()