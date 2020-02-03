# -*-coding:utf-8-*-
from operator import itemgetter
from random import randint


def getSub(list, k):
    temp = 0
    if k == 0:
        temp = list[96] * 64 + list[97] * 32 + list[98] * 16 + list[0] * 8 + list[1] * 4 + list[2] * 2 + list[3] * 1
    elif k == 1:
        temp = list[97] * 64 + list[98] * 32 + list[0] * 16 + list[1] * 8 + list[2] * 4 + list[3] * 2 + list[4] * 1
    elif k == 2:
        temp = list[98] * 64 + list[0] * 32 + list[1] * 16 + list[2] * 8 + list[3] * 4 + list[4] * 2 + list[5] * 1
    elif k == 96:
        temp = list[93] * 64 + list[94] * 32 + list[95] * 16 + list[96] * 8 + list[97] * 4 + list[98] * 2 + list[0] * 1
    elif k == 98:
        temp = list[95] * 64 + list[96] * 32 + list[97] * 16 + list[98] * 8 + list[0] * 4 + list[1] * 2 + list[2] * 1
    elif k == 97:
        temp = list[94] * 64 + list[95] * 32 + list[96] * 16 + list[97] * 8 + list[98] * 4 + list[0] * 2 + list[1] * 1
    else:
        temp = list[k - 3] * 64 + list[k - 2] * 32 + list[k - 1] * 16 + list[k] * 8 + list[k + 1] * 4 + list[
            k + 2] * 2 + list[k + 3] * 1
    return temp


def getRandList():
    randList = []
    for i in range(0, LIST_SIZE):
        randList.append(randint(0, 1))
    return randList


def getRandRule():
    randRule = []
    for i in range(0, RULE_SIZE):
        randRule.append(randint(0, 1))
    return randRule


def changeList(list, randRule):
    tempList = []
    for i in range(0, LIST_SIZE):
        sub = getSub(list, i)
        tempList.append(randRule[sub])
    return tempList


def getScore(randList, randRule):
    flag = randList.count(0) > randList.count(1)
    tempList = randList
    zero_count = 0
    one_count = 0
    for i in range(0, STEP_NUMBER):
        tempList = changeList(tempList, randRule)
        zero_count += tempList.count(0)
        one_count += tempList.count(1)

    if flag:
        return zero_count - one_count, int(tempList.count(0) == LIST_SIZE)
    else:
        return one_count - zero_count, int(tempList.count(1) == LIST_SIZE)


# def getSuccessNumber(randlist, randRule):
#     flag = randList.count(0) > randList.count(1)
#     tempList = randList
#     for i in range(0, STEP_NUMBER):
#         tempList = changeList(tempList, randRule)
#     if flag:
#         if tempList.count(0) == 99:
#             return 1
#         else:
#             return 0
#     else:
#         if tempList.count(1) == 99:
#             return 1
#         else:
#             return 0


def getPicture(randList, randRule):
    tempList = randList
    for i in range(0, STEP_NUMBER):
        for t in tempList:
            print(t, end="")
        print()
        tempList = changeList(tempList, randRule)
    print('\n')


def getScoreList(randRules, randLists):
    scoreList = []
    count = 0
    for randRule in randRules:
        totalScore = 0
        successNumber = 0
        for randList in randLists:
            tempScore, tempSuccessNumber = getScore(randList, randRule)
            totalScore += tempScore
            successNumber += tempSuccessNumber
        avgScore = totalScore / LIST_NUMBER
        print(avgScore, "No." + str(count), successNumber / LIST_NUMBER)
        scoreList.append((avgScore, count, successNumber / LIST_NUMBER))
        count += 1
        scoreList.sort(key=itemgetter(2, 0), reverse=True)
        print(scoreList)

    return scoreList
    # for randList in randLists:
    #     getPicture(randList, randRules[scoreList[0][1]])


def generationChange(randRules, randLists):
    scoreList = getScoreList(randRules, randLists)
    print("generation change...")
    global best_rule
    if not best_rule:
        best_rule.extend([randRules[scoreList[0][1]], scoreList[0][2]])
    else:
        if scoreList[0][2] > best_rule[1]:
            best_rule.clear()
            best_rule.extend([randRules[scoreList[0][1]], scoreList[0][2]])
    file_write_obj = open("test5.txt", 'w')
    file_write_obj.writelines(str(best_rule[0]))
    file_write_obj.write('\n')
    file_write_obj.close()
    transmit(randRules, scoreList)


def getTransmitRules(rule1, rule2):
    point = randint(0, RULE_SIZE - 1)
    list1 = rule1[:point] + rule2[point:]
    list2 = rule2[:point] + rule1[point:]
    return list1, list2


def transmit(randRules, scoreList):
    tempRandRules = []
    for k in range(0, int(RULE_NUMBER / 2)):
        tempI = 0
        tempJ = 0

        tempSum = 0
        tempRand = randint(0, weight_sum - 1)
        for i in range(0, RULE_NUMBER):
            tempSum += weight_array[i]
            if tempSum > tempRand:
                tempI = i
                break

        tempSum = 0
        tempRand = randint(0, weight_sum - 1)
        for j in range(0, RULE_NUMBER):
            tempSum += weight_array[j]
            if tempSum > tempRand and j != tempI:
                tempJ = j
                break

        rule1, rule2 = getTransmitRules(randRules[scoreList[tempI][1]], randRules[scoreList[tempJ][1]])
        mutate(rule1)
        mutate(rule2)
        tempRandRules.append(rule1)
        tempRandRules.append(rule2)
    randRules.clear()
    randRules.extend(tempRandRules)


def mutate(rule):
    i = randint(0, RULE_SIZE - 1)
    if rule[i] == 0:
        rule[i] = 1
    else:
        rule[i] = 0


if __name__ == '__main__':
    RULE_NUMBER = 150
    LIST_NUMBER = 100
    STEP_NUMBER = 100
    GENERATION_NUMBER = 150
    LIST_SIZE = 99
    RULE_SIZE = 128
    randLists = []
    randRules = []
    best_rule = []
    weight_array = []

    for r in range(0, RULE_NUMBER):
        randRules.append(getRandRule())
    for r in range(0, LIST_NUMBER):
        randLists.append(getRandList())
    for r in range(0, RULE_NUMBER):
        weight_array.append((r + 1) * 10)
    weight_array.sort(reverse=True)
    weight_sum = sum(weight_array)
    for r in range(0, GENERATION_NUMBER):
        generationChange(randRules, randLists)

