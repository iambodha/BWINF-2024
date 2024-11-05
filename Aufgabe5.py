import requests

URL_AUFGABE = "https://bwinf.de/fileadmin/wettbewerbe/bundeswettbewerb/43/1_runde/grabmal4.txt"


GRABMAL_DATA = requests.get(URL_AUFGABE).text
GRABMAL_DATA_GETRENNT = GRABMAL_DATA.splitlines()
GRABMAL_DATA_LIST = values = list(map(int, GRABMAL_DATA_GETRENNT))


ANZAHL_QUADER = GRABMAL_DATA_LIST[0]
QUADER_FREQUENZ = GRABMAL_DATA_LIST[1:]


def doCheck(currentTime,currentIndex):
    quaderValue = currentTime//QUADER_FREQUENZ[currentIndex]
    if quaderValue % 2 == 0:
        return False
    else:
        return True

def advanceCheck(currentTime,currentIndex):
    nextQuaderValue1 = (currentTime//QUADER_FREQUENZ[currentIndex-1]+1)*QUADER_FREQUENZ[currentIndex-1]
    nextQuaderValue2 = (currentTime//QUADER_FREQUENZ[currentIndex]+1)*QUADER_FREQUENZ[currentIndex]
    if nextQuaderValue1 > nextQuaderValue2:
        return True
    else:
        return False

def backPropagation(stepList,currentIndex):
    if currentIndex == 0:
        return False
    
    nextQuaderValue1 = (stepList[currentIndex-1]//QUADER_FREQUENZ[currentIndex-1]+2)*QUADER_FREQUENZ[currentIndex-1]
    nextQuaderValue2 = (stepList[currentIndex-2]//QUADER_FREQUENZ[currentIndex-2]+1)*QUADER_FREQUENZ[currentIndex-2]
    print(currentIndex,stepList,nextQuaderValue1,nextQuaderValue2)
    if nextQuaderValue1 < nextQuaderValue2:
        return False
    else:
        return True

def backPropagationLoop(stepList,currentIndex):
    tempStepList = stepList.copy()
    while True:
        if backPropagation(stepList,currentIndex) == False:
            print("Propagation is over")
            print(stepList,currentIndex)
            print(tempStepList)
            if len(stepList) == 0:
                stepList.append((tempStepList[currentIndex]//QUADER_FREQUENZ[currentIndex]+2)*QUADER_FREQUENZ[currentIndex])
                print(tempStepList[currentIndex],QUADER_FREQUENZ[currentIndex])
                currentIndex += 1
            else:
                quaderValue = (stepList[currentIndex-1]//QUADER_FREQUENZ[currentIndex-1]+2)*QUADER_FREQUENZ[currentIndex-1]
                print(stepList[currentIndex-1],QUADER_FREQUENZ[currentIndex])
                stepList.pop()
                stepList.append(quaderValue)
            print(stepList)
            return stepList,currentIndex
        else:
            currentIndex -= 1
            stepList.pop()

def recursiveAlgorithm():
    currentIndex = 1
    currentTime = QUADER_FREQUENZ[currentIndex-1]
    stepList = [currentTime]
    run = True
    while run:
        if doCheck(currentTime, currentIndex):
            currentIndex += 1
            stepList.append(currentTime)
        elif advanceCheck(currentTime, currentIndex):
            currentTime = (currentTime//QUADER_FREQUENZ[currentIndex]+1)*QUADER_FREQUENZ[currentIndex]
            currentIndex += 1
            stepList.append(currentTime)
        else:
            print("BEfore start algorithm")
            print(currentIndex)
            print(stepList)
            print(QUADER_FREQUENZ)
            stepList,currentIndex = backPropagationLoop(stepList,currentIndex)
            currentTime = stepList[-1]

        if currentIndex == ANZAHL_QUADER:
            print(stepList)
            print(currentTime)
            break

recursiveAlgorithm()