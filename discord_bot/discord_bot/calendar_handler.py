#needed: NAME
#needed: datums- und zeitstring in yyyymmddhhMMhhMM as dzs

import datetime
import pickle
from pathlib import Path
from os import mkdir

dzs = None
dateDictionary = {}
date = dzs[0:8]
times = dzs[8:16]

exitCodes = {
    200: "Eingegebenes Datum ist ok.",
    222: "Eingegebenes Datum ist nicht ok.",
    277: "Datum ist nicht im Dictionary. Niemand hat für dieses Datum eine freie Zeit angegeben.",
    288: "Kleinste Endzeit ist früher als späteste Anfangszeit. Keine freie Zeit verfügbar."
}

saves_path = Path("./saves")
if not saves_path.exists() or not saves_path.is_dir():
    mkdir(saves_path)


def checkTimeInput():
    if dzs.isdecimal():
        if datetime.today().year == int(dzs[0:4]):
            if datetime.today().month == int(dzs[4:6]) and int(dzs[4:6]) <= 12 and int(dzs[6:8]) <= 31:
                if datetime.today().day <= int(dzs[6:8]) and int(dzs[6:8]) <= 31:
                    return 200
            else:
                if datetime.today().month < int(dzs[4:6]) and int(dzs[4:6]) <= 12 and int(dzs[6:8]) <= 31:
                    return 200
        else:
            if datetime.today().year < int(dzs[0:4]) and datetime.today().month >= int(dzs[4:6]) and int(dzs[6:8]) <= 31:
                return 200
            else:
                return 222
    else:
        return 222


def addToDict():
    global dateDictionary
    global NAME
    dateDictionary.update({date: {NAME: times}})


def save_dateDictionary():
  global dateDictionary
  with open(saves_path / 'dateDictionary.pkl', 'wb') as pickled_dateDictionary:
    pickle.dump(dateDictionary, pickled_dateDictionary) #, pickle.HIGHEST_PROTOCOL)


def checkWhoIsFreeOn(key):
    global timeDictionary
    freePeople = []
    for el in timeDictionary[key].keys():
        freePeople.append(el)
    return freePeople


def checkFreeTimesOn(key):
    global timeDictionary
    startTimes = []
    endTimes = []
    for value in timeDictionary[key].values():
        startTimes.append(value[0:4])
    for value in timeDictionary[key].values():
        endTimes.append(value[4:8])
    if key in timeDictionary.keys():
        if min(endTimes) < max(startTimes):
            return 288
        else:
            return "Free play time from " + max(startTimes) + " to " + min(endTimes) + "."
    else:
        return 277
