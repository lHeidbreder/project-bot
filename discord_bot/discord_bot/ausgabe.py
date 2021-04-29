def printDiceValue(username:str, arg:[str]):
    ausgabe = username + " hat eine " + arg[0] + " gewürfelt"

    return ausgabe

def printDate(username:str, arg:[str]):
    namen = ""
    time = ""

    for x in arg[0]:
        namen = namen + x + ", "

    time = arg[1][0] + " bis " + arg[1][1]
  
    ausgabe = namen + "haben von " + time + " Zeit."
    
    return ausgabe

def printDateWasCorrect(username:str, arg:[str]):
    ausgabe = "Eingabe von " + username + " war korrekt."

    return ausgabe

def printFormatError(username:str, arg:[str]):
    ausgabe = "Der Würfel hat an Stelle " + arg[0] + " einen Fehler."
    
    return ausgabe

def printNoDiceError(username:str, arg:[str]):
    ausgabe = "Es wurde kein Würfel erkannt"

    return ausgabe 

def printHelp(username:str, arg:[str]):
    ausgabe = """
    Anleitung:

    1. Wie erstellt man einen Würfelstring?
    2. Wie verrechnet man Würfel?

    ______________________
    Würfelstring erstellen:

    Bsp.: 4d5 3D6-2d10 1d20
    Ein Würfelstring besteht aus mehreren Würfelelementen.

    Würfelelement erstellen:
    Bsp.: 2d6 -> 2x 6er-Würfel
    
    Jedes Element muss ein d enthalten. Es egal, ob dass d groß oder klein geschrieben ist.
    Die Zahl vor dem d ist die Anzahl der Würfel und die Zahl hinter dem d ist die Seitenzahl.

    Wenn man vor dem d keine Zahl schreibt, wird von einem Würfel ausgegangen.
    Wenn man hinter dem d keine Zahl schreibt, wird von einem sechseitigem Würfel ausgegangen.

    Man kann auch Ganzzahlen wie z.B. 5 oder 23 eingeben statt einem Würfelelement.

    ______________________
    Würfel addieren und subtrahieren:

    Bsp.: 4d d-2d 3d10-3d5

    Würfel werden addiert, wenn zwei Elemente mit einem Leerzeichen getrennt sind.
    Würfel werden subtrahiert, wenn zwei Elemente mit einem Minus getrennt sind.
    """
    
    return ausgabe
