from match import *

numberofmatch = 1
numberofgeneration = 8
numberofpopulation = 7
numberofancestor = 3
numberofstages = 2
r = 1

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
        creatures[i]['fitness']

def simulateGeneration(creatures):
    global r
    for i in range(numberofgeneration):
        print('\n\n== Generation', i+1)

        r = numberofgeneration - i - 1
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
    for i in range(len(newgen)):
        for j in range(16):
            newgen[i][j]+=r*random.randint(-5,5)
    return newgen 

def crossover(gen1, gen2):
    newgen = []
    for i in range(len(gen1)):
        tmp = []
        for j in range(16):
            if random.randint(1,numberofgeneration)<r:
                tmp.append([gen1[i][j],gen2[i][j]][random.randint(0,1)])
            tmp.append(gen1[i][j])
        newgen.append(tmp)
    return newgen


creatures = initializeCreatures(numberofpopulation)
bestCreature = simulateGeneration(creatures)
newCreatures = initializeCreatures(numberofpopulation)
for i in range(newCreatures):
    fitness += versus(5, bestCreature['tables'],tablesFromGen(newCreatures[i]['gen']))
print(fitness/i)
