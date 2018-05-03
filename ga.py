from match import *

numberofmatch = 3
numberofgeneration = 5
numberofpopulation = 3
numberofancestor = 2
numberofstages = 2
r = 1 #step in generation

def initializeCreatures(numberofpopulation):
    creatures=[]
    for i in range(numberofpopulation):
        randomgen = []
        for k in range(numberofstages):    
            randomsubgen=[]
            for j in range(16):
                randomsubgen.append(random.randint(0,63))
            randomgen.append(randomsubgen)
        creatures.append({'fitness':0, 'gen': randomgen,'tables':tablesFromGen(randomgen)})
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
            creatures[j]['tables']=tablesFromGen(creatures[j]['gen'])
        generateFitness(creatures)
        insertionSort(creatures)
        for i in range(numberofancestor, numberofpopulation):
            j = random.randint(0,numberofancestor-1)
            k = random.randint(0,numberofancestor-1)
            creatures[i]['gen']=crossover(creatures[j]['gen'], creatures[k]['gen'])
            creatures[i]['gen']=mutation(creatures[i]['gen'])
         
        for j in range(8):
            for k in range(8):
                print(creatures[0]['tables'][0][j][k],end=",")
            print()
        print()
        for j in range(8):
            for k in range(8):
                print(creatures[0]['tables'][1][j][k],end=",")
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


def mutation(gen):
    newgen = gen
    for i in range(r*len(newgen)):
        for l in range(r*random.randint(0,15)):
            j = random.randint(0,15)
            k = random.randint(0,15)
            newgen[i][j],newgen[i][k]=newgen[i][k],newgen[i][j]
    return newgen 

def crossover(gen1, gen2):
    gena = gen1
    genb = gen2
    for i in range(r*random.randint(0,len(gena)-1)):
        j = random.randint(0,len(gena)-1)
        k = random.randint(0,len(gena)-1)
        print("jk", j, k)
        print(gena)
        gena[j], genb[k] = gena[k], genb[j]
    return gena


creatures = initializeCreatures(numberofpopulation)
bestCreature = simulateGeneration(creatures)
newCreatures = initializeCreatures(numberofpopulation)
creatures[1:numberofpopulation] = newCreatures[1:numberofpopulation]
generateFitness(creatures)
print(creatures[0]['fitness'])
