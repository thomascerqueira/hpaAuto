from pynput import keyboard
from pynput.keyboard import Key, Listener
from pynput.mouse import Button, Controller

import pyperclip
import os

from FileHandler import *
from BotHandle import *
from ExcelHandle import *

Commands = ['m', 'M', 's', 'S', 'n', 'N', 'r', 'R', 'e', 'E']

Types = {
        "E": "Pas d'écriture",
        "M": "Mutuelle",
        "S": "Sécurité",
        "N": "Non réglé",
        "R": "Réglé"
    }

def getType(patient):
    passed = False
    Type = ""
    while 1:
        i = 0
        good = False
        if not passed:
            Type = input("Le patient %d n'a pas de type, il a été copier\nEntrer son type " %patient["Code"])
        passed = True
        while i < len(Commands):
            if Type == str(Commands[i]):
                good = True
                break
            i += 1
        if good:
            print("le patient est maintenant de type %s\n" %Types[Commands[i].upper()])
            patient["Type"] = Types[Commands[i].upper()]
            break
        else:
            Type = input("Le type de patients n'est pas reconnu\nEntrer son type ")

def emergencyStop(key):
    if (key == keyboard.Key.f8):
        print("ERMERGENCY STOP")
        os._exit(84)



if __name__ == '__main__':
    error = []
    fileHandler = FileHandler()
    MousePos = GetMousePos()
    excel = ExcelHandle()

    print("Sélectionner le fichier contenant la listes des patients")
    path, patients = fileHandler.__getPatients__()
    print(patients)

    temp = input()
    
    print("Positionner la souris sur l'icone cegi et appuyer sur c")
    mousePos, mousePos1 = MousePos.get_Mouse_Pos()
    bot = Bot(mousePos, mousePos1)
    bot.printPos()

    keyListener = keyboard.Listener(on_release=emergencyStop)
    keyListener.start()
    for patient in patients:
        patient["Type"] = fileHandler.__getType__()
        bot.copyPage(patient["Code"])
    for patient in patients:
        if not patient["Type"]:
            pyperclip.copy(str(patient["Code"]))
            getType(patient)
        print(patient)
    excel.writeInFile(path, patients)

    
