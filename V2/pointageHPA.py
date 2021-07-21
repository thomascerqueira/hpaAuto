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
            Type = input("\nLe patient %d n'a pas de type, il a été copier\nEntrer son type " %patient["Code"])
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
                print("N\t-\tNon réglé")
                print("E\t-\tPas d'écriture")
                Type = input("Quel type voulez vous ? ")
            else:
                Type = input("Le type de patient n'est pas reconnu\nEntrer son type ")

if __name__ == '__main__':
    error = []
    fileHandler = FileHandler()
    MousePos = GetMousePos()
    excel = ExcelHandle()
    nbPatientMan = 0
    regle, secu, mut, nr, pe = 0, 0, 0, 0, 0

    print("Sélectionner le fichier contenant la liste des patients")
    path, patients = fileHandler.__getPatients__()
    
    print("Positionner la souris sur l'icone cegi et appuyer sur c")
    mousePos, mousePos1 = MousePos.get_Mouse_Pos()
    bot = Bot(mousePos, mousePos1)
    bot.printPos()

    bot.__loop__(patients, fileHandler)
    for patient in patients:
        if not patient["Type"]:
            nbPatientMan += 1
    print("Nombre de patients à faire manuellement: %d\n" %nbPatientMan)
    for patient in patients:
        if not patient["Type"]:
            pyperclip.copy(str(patient["Code"]))
            getType(patient)
            nbPatientMan -= 1
            print("Nombre de patients manuel restant: %d\n" %nbPatientMan)
        Counts[patient["Type"]] = Counts[patient["Type"]] + 1
        print(patient)
    excel.writeInFile(path, patients, regle, secu, mut, nr, pe)
    print("Nombres totaux:\t%d" %sum(Counts.values()))
    print("Réglé:\t\t%d" %Counts["Réglé"])
    print("Sécurité:\t%d" %Counts["Sécurité"])
    print("Mutuelle:\t%d" %Counts["Mutuelle"])
    print("Non réglé:\t%d" %Counts["Non réglé"])
    print("Pas d'écriture:\t%d" %Counts["Pas d'écriture"])
    temp = input("Appuyer sur Entrée pour quitter")