from match import *

numberofmatch = 3
numberofgeneration = 3
numberofpopulation = 4
numberofancestor = 2

def initializeCreatures(numberofpopulation):
    creatures=[]
    for i in range(numberofpopulation):
        creatures.append({'fitness':0, 'tables':grst()})
    return creatures

def generateFitness(creatures):
    l = len(creatures)
    for i in range(l-1):
        for j in range(i+1,l):
            matchResult=versus(numberofmatch,creatures[i]['tables'],creatures[j]['tables'])
            print(i, j, 'result:', matchResult)
            creatures[i]['fitness']+=matchResult
            creatures[j]['fitness']+=(1-matchResult)
    for i in range(0,l):
        creatures[i]['fitness'] /= (l-1)

def simulateGeneration(creatures):
    for i in range(numberofgeneration):
        print('== Generation', i)
        for j in range(numberofpopulation):
            creatures[j]['fitness']=0
        generateFitness(creatures)
        insertionSort(creatures)
        newCreatures = initializeCreatures(numberofpopulation)
        creatures[numberofancestor:numberofpopulation] = newCreatures[numberofancestor:numberofpopulation]
        for j in range(8):
            for k in range(8):
                print(creatures[0]['tables'][0][j][k], end=",")
            print()
        print()
        for j in range(8):
            for k in range(8):
                print(creatures[0]['tables'][1][j][k], end=",")
            print()
    return creatures[0]

def insertionSort(creatures):
    i = 1
    while i<len(creatures):
        j = i
        while j>0 and creatures[j-1]['fitness']<creatures[j]['fitness']:
            creatures[j], creatures[j-1] = creatures[j-1], creatures[j]
            j = j-1
        i = i+1

creatures = initializeCreatures(numberofpopulation)
bestCreature = simulateGeneration(creatures)
newCreatures = initializeCreatures(numberofpopulation)
creatures[1:numberofpopulation] = newCreatures[1:numberofpopulation]
generateFitness(creatures)
print(creatures[0]['fitness'])
