import pyperclip

from FileHandler import *
from BotHandle import *
from ExcelHandle import *

Commands = ['M', 'S', 'N', 'R', 'E']

CommandsMUT = ['P', 'N']

Types = {
        "R": "Réglé",
        "S": "Sécurité",
        "M": "Mutuelle",
        "N": "Non réglé",
        "E": "Pas d'écriture"
    }

TypesMut = {
        "P": "Payé",
        "N": "Non payé",
    }

Counts = {
        "Pas d'écriture": 0,
        "Mutuelle": 0,
        "Sécurité": 0,
        "Non réglé": 0,
        "Réglé": 0
    }

CountsMUT = {
        "Payé": 0,
        "Non payé": 0
    }

def getType(patient, code):
    passed = False
    Type = ""
    wichCommand = []
    wichType = {}

    while 1:
        i = 0
        good = False
        if not passed:
            if code == 1:
                wichCommand = Commands.copy()
                wichType = Types.copy()
            elif code == 2:
                wichCommand = CommandsMUT.copy()
                wichType = TypesMut.copy()
            Type = input("\nLe patient %d n'a pas de type, il a été copier\nEntrer son type " %patient["Code"])
            passed = True

        while i < len(wichCommand):
            if Type.upper() == str(wichCommand[i]):
                good = True
                break
            i += 1

        if good:
            print("le patient est maintenant de type %s\n" %wichType[wichCommand[i]])
            patient["Type"] = wichType[wichCommand[i]]
            break
        else:
            if Type == 'h' or Type == 'H':
                if code == 2:
                    print("P\t-\tPayé")
                    print("N\t-\tPas Payé")
                else:
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
    mousePos = GetMousePos()
    excel = ExcelHandle()
    nbPatientMan = 0
    realCount = {}
    realType = {}

    func = input("Quelle type de pointage voulez-vous ?\n1: Pointage ATU\n2: Solde MUT\n")
    while func != '1' and func != '2':
        func = input("Quelle type de pointage voulez-vous ?\n1: Pointage ATU\n2: Solde MUT")

    func = int(func)
    if func == 1:
        realCount = Counts.copy()
        realType = Types.copy()
    elif func == 2:
        realCount = CountsMUT.copy()
        realType = TypesMut.copy()

    print("Sélectionner le fichier contenant la liste des patients")
    path, patients = fileHandler.__getPatients__()
    
    print("Positionner la souris sur l'icone cegi et appuyer sur c")
    mousePos, mousePos1 = mousePos.get_Mouse_Pos()
    bot = Bot(mousePos, mousePos1)

    bot.__loop__(patients, fileHandler, func)
    for patient in patients:
        if not patient["Type"]:
            nbPatientMan += 1
    print("Nombre de patients à faire manuellement: %d\n" %nbPatientMan)

    if func == 2:
        newPatient = []
        for patient in patients:
            if patient["Type"] != "Pas MUT":
                newPatient.append(patient)
        patients = []
        patients = newPatient.copy()

    for patient in patients:
        if not patient["Type"]:
            pyperclip.copy(str(patient["Code"]))
            getType(patient, func)
            nbPatientMan -= 1
            print("Nombre de patients manuel restant: %d\n" %nbPatientMan)
        realCount[patient["Type"]] = realCount[patient["Type"]] + 1
        print("%d: %s %s" %(patient["Code"], patient["Type"], patient["Mut"]))

    if func == 1:
        excel.writeInFile(path, patients, [0,0,0,0,0], func)
    elif func == 2:
        excel.writeInFile(path, patients, [0,0], func)

    print("Nombres totaux:\t%d" %sum(realCount.values()))

    for val in realType.values():
        print("%s:%s%d" %(val, "\t\t" if len(val) < 8 else "\t", realCount[val]))
    temp = input("Appuyer sur Entrée pour quitter")