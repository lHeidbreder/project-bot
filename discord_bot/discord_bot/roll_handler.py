"""
    Roll_Handler Module
    Module to interprete dice strings and create a dice value based on the input

    Date:       29.04.2021
    Version:    1.0.0
    Author:     Thomas Pietzka
"""

import random
#from logger import Logger

#Exit codes (for documentation only)
exitCodes = { 100 : "Dice string has been successfully interpreted. Izi snack!",
              110 : "Dice string has formatting error at index.",
              111 : "Dice string did not contain any dice." }

def rollDice(msg:str) -> (int, [str]):
    """
    Checks for the correct dice string format and outputs a value

    Checks for at least on dice contained in the dice string and the correct syntax of each die. 
    If dice have been entered, it checks for the correct dice syntax.
    If every dice syntax is correct, it will generete a value for each dice and return the calculated result.

    Parameters
    ----------
    msg: str
        The user entered message.

    Returns
    -------
    (int, [str])
        The first value indicates the exit code, the second is a string parameter used for the output method.
    """
    msg = msg.lower()
    diceTupel = __generateDiceAndOperandLists(msg)

    diceStringList = diceTupel[0]
    operandList = diceTupel[1]
    diceAmount = len(diceStringList)

    #check, if at least one dice is present
    if(diceAmount > 0):
        diceValues = []

        #generate dice value
        for i in range(0, diceAmount):
            diceValues.append(__testForCorrectDiceSyntax(diceStringList[i]))

            #break if dice had wrong syntax
            if(diceValues[i][1]):
                pass
            if(not diceValues[i][0]):
                return 110, [str(i)]

        #all dice had correct syntax, add them together
        for i in range(0, diceAmount):
            if(diceValues[i][1]): #is an literal
                diceValues[i]= diceValues[i][3]
            else:
                diceValues[i] = __throwDice(diceValues[i][2], diceValues[i][3])

        print("\t" + str(diceValues))
        print("\t" + str(operandList))

        calculatedResult = __calculateDiceResult(diceValues, operandList)
        return 100, [calculatedResult]
    else:
        return 111, []

#dice calculation
def __calculateDiceResult(operatorList:[int], operandList:[str]) -> int:
    """
    Given a list of operators and operants, it calculates the result

    Parameters
    ----------
    operatorList : [int]
        list of integers containing the operators
    operandList : [str]
        lost contraining strings that indicate the operands

    Returns
    -------
    int
        result of the calculation
    """
    result = operatorList.pop(0)

    #while there are still operands
    while(len(operandList) > 0):
        if(operandList.pop(0) == "+"):
            result += operatorList.pop(0)
        else:
            result -= operatorList.pop(0)

    return result
def __throwDice(amount:int, maxValue:int) -> int:
    """
    Given a dice amount and dice value, it will throw the dice multiple times and add them together.

    Parameters
    ----------
    amount : int
        How often the die should be thrown.
    maxValue : int
        The maximal die value (e.g. for a 6 sided die it would be 6).
    """
    result = 0
    for i in range(0, amount):
        result += random.randint(1, maxValue)

    return result

#dice string manipulation
def __generateDiceAndOperandLists(msg:str) -> ([str], [str]):
    """
    For a given string, it will attempt to get all dice strings and operands.

    Paramters
    ---------
    msg : str
        The message entered by the user.

    Returns
    -------
    ([str], [str])
        the first list contains all dice strings, the right the operands as string
    """
    operators = []
    operands = []

    nextOperandTupel = __findNextOperand(msg)
    nextOperand = nextOperandTupel[1]
    nextOperandIndex = nextOperandTupel[0]

    while(nextOperand != ""):
        leftPart = msg[0:nextOperandIndex]
        rightPart = msg[nextOperandIndex+1 : None]

        operators.append(leftPart)
        operands.append(nextOperand)
        msg = rightPart

        nextOperandTupel = __findNextOperand(msg)
        nextOperand = nextOperandTupel[1]
        nextOperandIndex = nextOperandTupel[0]

    operators.append(msg)

    return operators, operands
def __findNextOperand(msg:str)-> (int, str):
    """
    Tries to find the next operand.

    Parameters
    ----------
    msg : str
        The message entered by the user.

    Returns
    -------
    (int, str)
        The first value indicates the index of the found operand, is -1 if no operand was found.
        The second value indicates the operand itself, is "" if no operand was found.
    """
    space = msg.find(" ")
    plus = msg.find("+")

    #test, if spaces and pluses are found both
    if(space >= 0 and plus >= 0):
        if(space > plus):
            plus = space
    elif(space > plus):
        plus = space

    minus = msg.find("-")
    operand = ""
    operandIndex = -1

    #test for minus and plus and which comes first
    if(minus >= 0 and plus >= 0):
        if(minus < plus):
            operand = "-"
            operandIndex = minus
        else:
            operand = "+"
            operandIndex = plus
    elif(minus < 0 and plus >= 0):
        operand = "+"
        operandIndex = plus
    elif(minus >= 0 and plus < 0):
        operand = "-"
        operandIndex = minus

    return operandIndex, operand
def __testForCorrectDiceSyntax(dice:str) -> (bool, bool, int, int):
    """
    Tests for the correct dice syntax

    Parameters
    ----------
    dice : str
        the string containing the dice definition

    Returns
    -------
    (bool, int, int)
        The first value indicates wether it is a correctly formatted string or not. If false, all other values are -1.
        The second value indicates wether the value is an literal.
        The third value indicates how often the die should be thrown.
        The fourth value indicates the sides of the die, meaning the max value that can be thrown using that dice.
    """
    #test, if there is a "d" in the string. If not, it could be an literal or wrongly formatted
    result = ()

    if(dice.find("d") < 0):
        integerParse = __TryParseInteger(dice)
        if (integerParse[0]):
            return True, True, -1, integerParse[1]
        return False, False, -1, -1

    diceStringParts = dice.split("d")
    diceStringPartsLength = len(diceStringParts)

    #test, if there are enouth parts
    if(diceStringPartsLength < 0 or diceStringPartsLength > 2):
        #dice string either had to many or to few parts
        return False, False, -1, -1

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
        if(not __TryParseInteger(diceStringParts[i])[0]):
            #could not convert to integer
            return False, False, -1, -1

    #placeholder variables for left and right side of each dice statement
    diceValue1 = 1
    diceValue2 = 6

    if(diceStringPartsLength == 1):
        if(dice.startswith('d')):
            diceValue2 = __ParseInteger(diceStringParts[0])
        else:
            diceValue1 = __ParseInteger(diceStringParts[0])
    elif (diceStringPartsLength == 2):
        diceValue1 = __ParseInteger(diceStringParts[0])
        diceValue2 = __ParseInteger(diceStringParts[1])

    return True, False, diceValue1, diceValue2

#help methods
def __ParseInteger(string:str) -> int:
    """
    Attempts to convert a string to an integer, will log an error if not possible.

    Parameters
    ----------
    string : str
        string that should be parsed.

    Returns
    -------
    int
        integer that has been parsed.
    """
    result = -1
    try:
        result = int(string)
    except:
        #log = Logger.get_instance()
        #log.severe("Couldn't convert" + string + "to integer in \"ParseInteger(string:str) -> int\"")
        pass
    return result
def __TryParseInteger(string:str) -> (bool, int):
    """
    Attempts to convert an string to an integer.

    Paramters
    ---------
    string : str
        string that should be parsed.

    Returns
    -------
    (bool, int)
        The first value indicates, if the parsing was successfull.
        The second value will contain the parsed value, -1 by default if parsing did not work.
    """
    result = -1
    worked = False
    
    try:
        result = int(string)
        worked = True
    except:
        pass

    return worked, result

print(rollDice("-4d-10"))
print(rollDice("-d"))
print(rollDice("4d-5"))