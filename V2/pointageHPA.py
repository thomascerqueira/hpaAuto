from pynput import keyboard
from pynput.keyboard import Key, Listener, Controller

import pyperclip
import os
import time

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

Counts = {
        "Pas d'écriture": 0,
        "Mutuelle": 0,
        "Sécurité": 0,
        "Non réglé": 0,
        "Réglé": 0
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
            if Type == 'h' or Type == 'H':
                print("R\t-\tRéglé")
                print("S\t-\tSécurité (caisse)")
                print("M\t-\tMutuelle")
                print("NR\t-\tNon réglé")
                print("E\t-\tPas d'écriture")
            else:
                Type = input("Le type de patients n'est pas reconnu\nEntrer son type ")

def emergencyStop(key):
    if (key == keyboard.Key.f8):
        print("ERMERGENCY STOP")
        os._exit(84)

if __name__ == '__main__':
    error = []
    keyBoard = Controller()
    fileHandler = FileHandler()
    MousePos = GetMousePos()
    excel = ExcelHandle()
    regle, secu, mut, nr, pe = 0

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
        pyperclip.copy(str(patient["Code"]))
        print("clipboard = ", pyperclip.paste())
        bot.copyPage(patient["Code"])
        patient["Type"] = fileHandler.__getType__()
        keyboardPress(keyBoard, Key.esc)
        time.sleep(1)
    for patient in patients:
        if not patient["Type"]:
            pyperclip.copy(str(patient["Code"]))
            getType(patient)
        Counts[patient["Type"]] += 1
        print(patient)
    excel.writeInFile(path, patients, regle, secu, mut, nr, pe)
    print("Nombres totaux:")
    print("Réglé:\t%d", regle)
    print("Réglé:\t%d", secu)
    print("Réglé:\t%d", mut)
    print("Réglé:\t%d", nr)
    print("Réglé:\t%d", pe)
    temp = input("Appuyer sur Entrée pour quitter")