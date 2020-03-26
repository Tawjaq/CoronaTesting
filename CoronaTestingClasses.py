import random
import math

class CoronaSuspect(object):
    def __init__(self, infectionChance):
        ###Infection chance is expressed as a float value between 0-1"""
        self.infectionChance = infectionChance
        if random.random() <= self.infectionChance:
            self.infected = True
        else:
            self.infected = False

    def isInfected(self):
        return self.infected

class TestingGroup(object):
    def __init__(self, listOfSuspects):
        self.listOfSuspects = listOfSuspects
        self.infected = False
        for suspect in listOfSuspects:
            if suspect.isInfected():
                self.infected = True
                break
        self.numberOfPatients = len(listOfSuspects)

    def __len__(self):
        return self.numberOfPatients

    def runTest(self, splitInto):
        newGroups = []
        if self.infected:
            for i in range(splitInto):
                newGroups.append(TestingGroup([]))
            for i, suspect in enumerate(self.listOfSuspects):
                newGroups[i%splitInto].append(suspect)
        return newGroups

    def isInfected(self):
        return self.infected

    def append(self, suspect):
        self.listOfSuspects.append(suspect)
        if suspect.isInfected():
            self.infected = True
        self.numberOfPatients += 1

    def getSuspects(self):
        return self.listOfSuspects

class Population(object):
    def __init__(self, popSize, startingGroupSize, infectionSpread):
        self.popSize = popSize
        self.startingGroupSize = startingGroupSize
        self.infectionSpread = infectionSpread
        self.numberOfGroups = math.ceil(popSize/startingGroupSize)
        self.groupsToTest = []
        for i in range(self.numberOfGroups):
            self.groupsToTest.append(TestingGroup([]))
        for i in range(self.popSize):
            self.groupsToTest[i%self.numberOfGroups].append(CoronaSuspect(infectionSpread))
        self.infected = []
        self.testsUsed = 0

    def startTesting(self, splitInto):
        while self.groupsToTest:
            currentGroup = self.groupsToTest.pop()
            self.testsUsed += 1
            result = currentGroup.runTest(splitInto)
            for group in result:
                if len(group) == 1 and group.isInfected():
                    self.infected.append(group.getSuspects()[0])
                    self.testsUsed += 1
                elif len(group) > 1:
                    self.groupsToTest.append(group)
                else:
                    pass
        return self.testsUsed

    def percentageOfNegativeGroups(self):
        positiveGroups = 0
        negativeGroups = 0
        for group in self.groupsToTest:
            if group.isInfected():
                positiveGroups += 1
            else:
                negativeGroups += 1
        return [negativeGroups, positiveGroups, negativeGroups/(positiveGroups+negativeGroups)]

#a = Population(5000000, 2, 0.1)
#print(a.percentageOfNegativeGroups())
#print(a.startTesting(2))

def monteCarlo(population, startingGroupSize, infectionSpread, split, repeat):
    positiveGroupsList = []
    negativeGroupsList = []
    negativePercentages = []
    testsUsedList = []
    for i in range(repeat):
        print('Test ' + str(i))
        sample = Population(population, startingGroupSize, infectionSpread)
        initialGroupsResults = sample.percentageOfNegativeGroups()
        positiveGroupsList.append(initialGroupsResults[1])
        negativeGroupsList.append(initialGroupsResults[0])
        negativePercentages.append(initialGroupsResults[2])
        testsUsed = sample.startTesting(split)
        testsUsedList.append(testsUsed)
    positiveGroupsAverage = (sum(positiveGroupsList))/repeat
    negativeGroupsAverage = (sum(negativeGroupsList))/repeat
    negativePercentages = (sum(negativePercentages))/repeat
    testsUsedAverage = (sum(testsUsedList))/repeat
    print(testsUsedList)
    return [negativeGroupsAverage, positiveGroupsAverage, negativePercentages, testsUsedAverage]

print(monteCarlo(5000000, 1000, 0.001, 2, 5))
