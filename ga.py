from match import *

numberofmatch = 1
numberofgeneration = 7
numberofpopulation = 6
numberofancestor = 2
numberofstages = 5

def tablesFromGen(gen):
    scoretables=[]
    for i in range(len(gen)):
        tmp = gen[i]
        scoretable = []
        scoretable.append(tmp[0:4]+tmp[3::-1])
        scoretable.append(tmp[4:8]+tmp[7:3:-1])
        scoretable.append(tmp[8:12]+tmp[11:7:-1])
        scoretable.append(tmp[12:16]+tmp[15:11:-1])
        scoretable.append(tmp[12:16]+tmp[15:11:-1])
        scoretable.append(tmp[8:12]+tmp[11:7:-1])
        scoretable.append(tmp[4:8]+tmp[7:3:-1])
        scoretable.append(tmp[0:4]+tmp[3::-1])
        scoretables.append(scoretable)
    return scoretables


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
newCreatures = initializeCreatures(2*numberofpopulation)
print("\n===Testing===\n")
fitness=0
for i in range(len(newCreatures)):
    tmp = versus(5, bestCreature['tables'],tablesFromGen(newCreatures[i]['gen']))
    fitness+=tmp
print(fitness/i)
import csv
with open('eggs.csv', 'w', newline='\n') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for table in (bestCreature['tables']):
        spamwriter.writerow(['== table =='])
        for row in table:
            spamwriter.writerow(row)
