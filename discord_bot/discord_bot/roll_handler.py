'''
    Roll Handler Module
    Module to interprete dice strings and create a dice value based on the input

    Date:       29.04.2021
    Version:    1.0.0.0
    Author:     Thomas Pietzka
'''

import random

exitCodes = {
    100 : "Dice string has been successfully interpreted. Izi snack!",
    110 : "Dice string has formatting error at index.",
    111 : "Dice string did not contain any dice."
             }

def rollDice(msg:str) -> (int, [str]):
    msg = msg.lower()
    diceTupel = generateDiceAndOperandLists(msg)

    diceStringList = diceTupel[0]
    operandList = diceTupel[1]
    diceAmount = len(diceStringList)

    #check, if at least one dice is present
    if(diceAmount > 0):
        diceValues = []

        #generate dice value
        for i in range(0, diceAmount):
            diceValues.append(testForCorrectDiceSyntax(diceStringList[i]))

            #break if dice had wrong syntax
            if(not diceValues[i][0]):
                print("\tWrong syntax")
                return 110, [str(i)]

        #all dice had correct syntax, add them together
        for i in range(0, diceAmount):
            diceValues[i] = throwDice(diceValues[i][1], diceValues[i][2])
        
        return 100, calculateDiceResult(diceValues, operandList)
    else:
        print("\tNo dice found")
        return 111, []

def calculateDiceResult(operatorList:[int], operandList:[str]):
    result = operatorList.pop(0)

    while(len(operandList) > 0):
        if(operandList.pop(0) == "+"):
            result += operatorList.pop(0)
        else:
            result -= operatorList.pop(0)

    return result
def throwDice(amount:int, maxValue:int) -> int:
    result = 0
    for i in range(0, amount):
        result += random.randint(1, maxValue)

    return result

def generateDiceAndOperandLists(msg:str) -> (list, list):
    operators = []
    operands = []

    nextOperandTupel = findNextOperand(msg)
    nextOperand = nextOperandTupel[1]
    nextOperandIndex = nextOperandTupel[0]

    while(nextOperand != ""):
        leftPart = msg[0:nextOperandIndex]
        rightPart = msg[nextOperandIndex+1 : None]

        operators.append(leftPart)
        operands.append(nextOperand)
        msg = rightPart

        nextOperandTupel = findNextOperand(msg)
        nextOperand = nextOperandTupel[1]
        nextOperandIndex = nextOperandTupel[0]

    operators.append(msg)

    return operators, operands

def findNextOperand(msg:str)-> (int, str):
    space = msg.find(" ")
    plus = msg.find("+")

    #test, if spaces and pluses are found both
    if(space > 0 and plus > 0):
        if(space > plus):
            plus = space
    elif(space > plus):
        plus = space

    minus = msg.find("-")
    operand = ""
    operandIndex = -1

    #test for minus and plus and which comes first
    if(minus > 0 and plus > 0):
        if(minus < plus):
            operand = "-"
            operandIndex = minus
        else:
            operand = "+"
            operandIndex = plus
    elif(minus < 0 and plus > 0):
        operand = "+"
        operandIndex = plus
    elif(minus > 0 and plus < 0):
        operand = "-"
        operandIndex = minus

    return operandIndex, operand

def testForCorrectDiceSyntax(dice:str) -> (bool, int, int):
    #test, if there is a "d" in the string, otherwise return false
    if(dice.find("d") < 0):
        return False, -1, -1

    diceStringParts = dice.split("d")
    diceStringPartsLength = len(diceStringParts)

    #test, if there are enouth parts
    if(diceStringPartsLength < 0 or diceStringPartsLength > 2):
        #dice string either had to many or to few parts
        return False, -1, -1

    #count, how many spaces are empty
    spaceCounter = 0;
    for i in range(0, diceStringPartsLength):
        if(diceStringParts[i] == ''):
            spaceCounter += 1

    #remove all counted empty spaces
    for i in range(0, spaceCounter):
        diceStringParts.remove('')

    #update the length of the array after items were removes
    diceStringPartsLength = len(diceStringParts)

    for i in range(0, len(diceStringParts)):
        if(not TryParseInteger(diceStringParts[i])[0]):
            #could not convert to integer
            return False, -1, -1

    #placeholder variables for left and right side of each dice statement
    diceValue1 = 1
    diceValue2 = 6

    if(diceStringPartsLength == 1):
        if(dice.startswith('d')):
            diceValue2 = ParseInteger(diceStringParts[0])
        else:
            diceValue1 = ParseInteger(diceStringParts[0])
    elif (diceStringPartsLength == 2):
        diceValue1 = ParseInteger(diceStringParts[0])
        diceValue2 = ParseInteger(diceStringParts[1])

    return True, diceValue1, diceValue2

def ParseInteger(string:str) -> int:
    result = -1
    try:
        result = int(string)
    except:
        print("Couldn't convert" + string + "to integer in \"ParseInteger(string:str) -> int\"")

    return result
def TryParseInteger(string:str) -> (bool, int):
    result = -1
    worked = False
    
    try:
        result = int(string)
        worked = True
    except:
        pass

    return worked, result

rollDice("")
rollDice("4d5 3D6-2d10 1d20")
rollDice("4d d-2d 3d10 3d5")
rollDice("d d-d d-d d-d d-d d-d d-d d-d d-d d-d")
rollDice("Hello world")