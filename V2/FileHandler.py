import os
import tkinter as tk
import pyperclip
from tkinter import filedialog
import sys


class FileHandler:
    def __getPatients__(self):
        patients = []
        root = tk.Tk()
        root.withdraw()

        if len(sys.argv) == 2:
            file_path = sys.argv[1]
        else:
            file_path = filedialog.askopenfilename()
        try:
            with open(file_path) as fp:
                while True:
                    try:
                        line = fp.readline()
                    except UnicodeDecodeError as err:
                        print(err, "\nUn ou plusieurs charactere n'ont pas pû être lu")
                        continue
                    if not line:
                        break
                    if line.startswith('! NOM et PRENOM'):
                        line = fp.readline()
                        while True:
                            line = fp.readline()
                            if not line or not line.startswith('!'):
                                break
                            tab = line.split('!')
                            try:
                                patients.append({"Code": int(tab[2]),
                                                "Type": "",
                                                "Mut": ""})
                            except:
                                print("Erreur sur la ligne: ", line)
        except FileNotFoundError as err:
            print(err)
            input("Le fichier n'existe pas ou alors il y a un problème dedans\n")
            os._exit(84)
        except RuntimeError as err:
            print(err)
            input()
            os._exit(84)
        return (file_path, patients)

    def __getInfo__(self, line, word):
        Type = ""
        startIndex = line.find(word)
        startIndex += len(word)
        while startIndex < len(line) and line[startIndex] != '│':
            Type += line[startIndex]
            startIndex += 1
        return Type

    def __getType__(self, code):
        Caisse = ""
        Mutuelle = ""
        clipboard = pyperclip.paste()
        lastLine = ""
        tab = clipboard.split('\n')
        good = False

        for i in range(len(tab)):
            if good:
                if tab[i].startswith('──') or tab[i].startswith("│Pas d'écriture"):
                    if code == 2:
                        if tab[i].startswith("│Pas d'écriture"):
                            return "Pas MUT", False, Mutuelle
                    else:
                        if tab[i].startswith("│Pas d'écriture"):
                            return "Pas d'écriture", False, Mutuelle
                    return "", False, Mutuelle
                tab1 = tab[i].split('│')
                try:
                    if code == 2:
                        if tab1[2].startswith('TOTAL MUTUELLE__'):
                            value = tab1[2].split(' ')
                            if int((value[-1].split(','))[0]) == 0:
                                return "Payé", True, Mutuelle
                            else:
                                return "Non payé", True, Mutuelle
                    else:
                        if tab1[2].startswith('FAC'):
                            lastLine = tab1[3]
                        else:
                            if lastLine == Caisse:
                                return "Sécurité", True, Mutuelle
                            elif lastLine == Mutuelle:
                                return "Mutuelle", True, Mutuelle
                except:
                    pass
            if tab[i].startswith('│Assuré..... '):
                Caisse = self.__getInfo__(tab[i], "Caisse.. ")
            if tab[i].startswith('│Numéro sécu '):
                Mutuelle = self.__getInfo__(tab[i], "Mutuelle ")
            if tab[i].startswith('│   Date   │'):
                good = True
                i += 1
        return "", True, Mutuelle