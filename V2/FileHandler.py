import os
import pynput
import tkinter as tk
import pyperclip

from tkinter import filedialog
from pynput.keyboard import Key, Listener

class FileHandler:
    def __getPatients__(self):
        patients = []
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename()
        try:
            with open(file_path) as fp:
                while True:
                    line = fp.readline()
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
                                                "Type": ""})
                            except:
                                print("Error on line: ", line)
        except:
            print("Le fichier n'existe pas ou alors il y a un problème dedans")
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

    def __getType__(self):
        Caisse = ""
        Mutuelle = ""
        clipboard = pyperclip.paste()
        lastLine = ""
        tab = clipboard.split('\n')
        good = False
        for i in range(len(tab)):
            if good:
                if tab[i].startswith('──'):
                    return ""
                tab1 = tab[i].split('│')
                try:
                    if tab1[2].startswith('FAC'):
                        lastLine = tab1[3]
                    else:
                        if lastLine == Caisse:
                            return "Sécurité"
                        elif lastLine == Mutuelle:
                            return "Mutuelle"
                except:
                    pass
            if tab[i].startswith('│Assuré..... '):
                Caisse = self.__getInfo__(tab[i], "Caisse.. ")
            if tab[i].startswith('│Numéro sécu '):
                Mutuelle = self.__getInfo__(tab[i], "Mutuelle ")
            if tab[i].startswith('│   Date   │'):
                good = True
                i += 1
