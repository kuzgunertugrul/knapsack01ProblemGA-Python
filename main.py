import random

parents = []
parentsAfterSelection = []
parentsProfit = []
parentsProfitAfterSelection = []
crossoveredChilds = []
itemsWeightList = []
itemsProfitList = []
itemsOptimalSelection = []
populationSayisi = 0
id = 0
repairedListInRepair = []
mutatedChilds = []
mutatedChildsProfit = []
capacity = 0

def fileRead(dataSetNumber):
    capacityFile = dataSetNumber + "knapsack01_c.txt"
    profitFile = dataSetNumber + "knapsack01_p.txt"
    weightFile = dataSetNumber + "knapsack01_w.txt"
    selectionFile = dataSetNumber + "knapsack01_s.txt"

    f = open(capacityFile,"r")
    capacityStr = f.read()
    capacityInFunc = int(capacityStr)
    f.close()

    f = open(profitFile,"r")
    profit = f.read()
    itemsProfitList = [int(n) for n in profit.split()]
    print(itemsProfitList)
    f.close()

    f = open(weightFile,"r")
    weights = f.read()
    itemsWeightList = [int(n) for n in weights.split()]
    print(itemsWeightList)
    f.close()

    f = open(selectionFile,"r")
    content = f.readlines()
    for line in content:
        for i in line:
            if i.isdigit() == True:
                itemsOptimalSelection.append(int(i))
    f.close()

    return capacityInFunc, itemsProfitList, itemsWeightList, itemsOptimalSelection
    
def tournamentSelection():
    lprofitList = [x for x in range(len(parentsProfit))]
    while len(lprofitList) >= 2:
        rand1 =  random.choice(lprofitList)
        rand2 = random.choice(lprofitList)
        while True:
            if rand1 == rand2:
                rand1 = random.choice(lprofitList)
            else:
                break
        if parentsProfit[rand1] >= parentsProfit[rand2]:
            lprofitList.remove(rand2)
            parentsAfterSelection.append(parents[rand1])
            parentsProfitAfterSelection.append(parentsProfit[rand1])
            lprofitList.remove(rand1)
        elif parentsProfit[rand2] > parentsProfit[rand1]:
            lprofitList.remove(rand1)
            parentsAfterSelection.append(parents[rand2])
            parentsProfitAfterSelection.append(parentsProfit[rand2])
            lprofitList.remove(rand2)
    print(parentsAfterSelection,"profits:",parentsProfitAfterSelection)
    return parentsProfitAfterSelection

def adayCozumUret():
    liste = []
    binaryChoice = [0,1]
    for i in range(len(itemsOptimalSelection)):
        liste.append(random.choice(binaryChoice))
    return liste

def cokluAdayCozum(adayCozumSayisi):
    for i in range(0,adayCozumSayisi):
        tekCozum = adayCozumUret()
        aday = fitness(tekCozum)
        #parents.append(tekCozum)
        print(aday[0],"profit:",aday[1])
        parents.append(aday[0])
        parentsProfit.append(aday[1])  

def calculateProfit(liste):
    profit_toplam = 0
    i = 0
    for index in liste:
        if index == 1:
            profit_toplam += int(itemsProfitList[i])
        else:
            pass
        i+=1
    return profit_toplam

def fitness(adayListe):
    weight_toplam = 0
    profit_toplam = 0
    i = 0
    for index in adayListe:
        if index == 1:
            weight_toplam += int(itemsWeightList[i])
            profit_toplam += int(itemsProfitList[i])
        else:
            pass
        i+=1

    if weight_toplam > capacity:
        repairedList = repairFunc(adayListe)
        repairedListProfit = calculateProfit(repairedList)
        return repairedList,repairedListProfit
    else:
        return adayListe,profit_toplam

def repairFunc(repairList:list):
    while True:
        print("************************************")
        repairedList=[]
        repaireddList=[]
        print("will repair",repairList)
        j = 0
        weight_toplam = 0
        indexList = []
        profitList = []
        for i in repairList:
            if i == 1:
                indexList.append(j)
            j+=1
        for i in indexList:
            profitList.append(itemsProfitList[i])
        minProfit = min(profitList)
        minProfitIndex_in_indexList = profitList.index(minProfit)
        minProfitIndex = indexList[minProfitIndex_in_indexList]
        repairList[minProfitIndex] = 0
        repairedList = repairList.copy()
        print("repaired list",repairedList)
        
        k = 0
        for index in repairList:
            if index == 1:
                weight_toplam += int(itemsWeightList[i])
                if weight_toplam > capacity:
                    break
            else:
                pass
            k+=1
        if weight_toplam <= capacity:
            repairedList = repairList.copy()
            print("************************************")
            return repairedList

def crossoverFunc():
    lparentList = [x for x in range(len(parentsAfterSelection))]
    while len(lparentList) >= 2:
        child = []
        rand1 =  random.choice(lparentList)
        rand2 = random.choice(lparentList)
        while True:
            if rand1 == rand2:
                rand1 = random.choice(lparentList)
            else:
                break
        threshold = random.randint(1, len(itemsOptimalSelection)-1)
        print("p1:",parentsAfterSelection[rand1],":","p2:",parentsAfterSelection[rand2])
        parent1 = parentsAfterSelection[rand1]
        parent2 = parentsAfterSelection[rand2]
        lparentList.remove(rand2)
        lparentList.remove(rand1)
        child.extend(parent1[:threshold])
        child.extend(parent2[threshold:])
        crossoveredChilds.append(child)
        print(child)

def mutation(ch):
    for i in range(len(ch)):
        k = random.uniform(0,1)
        if k > 0.8:
            if ch[i] == 1:
                ch[i] = 0
            else:
                ch[i] = 1
    return ch

selectedFiles = input("Enter dataset number: ")
fileReturns = fileRead(selectedFiles)
capacity = fileReturns[0]
itemsProfitList = fileReturns[1]
itemsWeightList = fileReturns[2]
itemsOptimalSelection = fileReturns[3]

adayCozumSayisi = int(input("Aday çözüm sayısı giriniz: "))
populationSayisi = adayCozumSayisi

cokluAdayCozum(adayCozumSayisi)
profits = tournamentSelection()
print(calculateProfit(itemsOptimalSelection), "maks",(max(profits) - calculateProfit(itemsOptimalSelection)))
crossoverFunc()
print("----------------------------------")
for i in range(len(crossoveredChilds)):
    mutatedChild = mutation(crossoveredChilds[i])
    repairedMutatedChild = fitness(mutatedChild)
    print(repairedMutatedChild[0],"profit:",repairedMutatedChild[1])
    mutatedChilds.append(repairedMutatedChild[0])
    mutatedChilds.append(repairedMutatedChild[1])



