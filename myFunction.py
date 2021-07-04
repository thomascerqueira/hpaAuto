from msvcrt import getch
from tkinter import Tk
import os

import pynput

from pynput.keyboard import Key, Listener

class MyException(Exception): pass

class Patients:

    patients = []
    index = 0
    pause = False
    haveToQuit = False

    Commands = ['m', 'M', 's', 'S', 'n', 'N', 'r', 'R', 'e', 'E']

    Types = {
        "E": "Pas d'écriture",
        "M": "Mutuelle",
        "S": "Sécurité",
        "N": "Non réglé",
        "R": "Réglé"
    }

    def on_press(self, key):
        # print("{0} pressed".format(key))
        pass

    def on_release(self, key):
        good = 0
        i = 0
        try:
            if key == Key.esc:
                return False
            elif key == Key.enter:
                if not self.haveToQuit:
                    if self.patients[self.index]["Type"] == "E":
                        print("doss %d n'a pas d'écriture", flush=True)
                    elif self.patients[self.index]["Type"] == "":
                        print("le patients n'a pas de type", flush=True)
                        return True
                    else:
                        print("Le dossier %d est %s\n" %(self.patients[self.index]["Doss"], self.patients[self.index]["Type"]), flush=True)
                    self.index += 1
                    if self.index >= len(self.patients):
                        print("Appuyer sur entré pour confirmer la saisie", flush=True)
                        self.haveToQuit = True
                    else:
                        self.__copyToClipboard__(str(self.patients[self.index]["Doss"]))
                        print("Le dossier %d a été copier dans le press-papier" %self.patients[self.index]["Doss"], flush=True)
                        if self.patients[self.index]["Type"] != "":
                            print("Son dernier type était : %s" %self.patients[self.index]["Type"])
                else:
                    print("Saisie validé")
                    return False
            elif key == Key.backspace:
                if not self.haveToQuit:
                    self.index -= 1 if self.index - 1 >= 0 else 0
                    print("\nLe Doss %d est sélectionner" %self.patients[self.index]["Doss"])
                    self.__copyToClipboard__(str(self.patients[self.index]["Doss"]))
                else:
                    self.index = len(self.patients) - 1
                    print("\nSaisie annulé\nDossier sélectionner : %d" %self.patients[self.index]["Doss"])
                    self.haveToQuit = False
            else:
                if self.haveToQuit:
                    return True
                while i < len(self.Commands):
                    if str(key.char) == str(self.Commands[i]):
                        good = True
                        break
                    i += 1
                if good:
                    self.patients[self.index]["Type"] = self.Types[self.Commands[i].upper()]
                    self.patients[self.index]["Code"] = self.Commands[i].upper()
                    print("doss %d num %d est %s" %(self.index, self.patients[self.index]["Doss"], self.patients[self.index]["Type"]), flush=True)
                # else:
                #     print("Pas trouvé", flush=True)

            # elif key.char == ('m') or key.char == ('M'):
            #     if not self.haveToQuit:
            #         self.patients[self.index]["Type"] = "Mutuelle"
            #         print("doss %d num %d est mutuelle" %(self.index, self.patients[self.index]["Doss"]), flush=True)
            # elif key.char == ('s') or key.char == ('S'):
            #     if not self.haveToQuit:
            #         self.patients[self.index]["Type"] = "Sécu" 
            #         print("doss %d num %d est sécu" %(self.index, self.patients[self.index]["Doss"]), flush=True)
            # elif key.char == ('r') or key.char == ('R'):
            #     if not self.haveToQuit:
            #         self.patients[self.index]["Type"] = "Réglé" 
            #         print("doss %d num %d est réglé" %(self.index, self.patients[self.index]["Doss"]), flush=True)
            # elif key.char == ('n') or key.char == ('N'):
            #     if not self.haveToQuit:
            #         self.patients[self.index]["Type"] = "Non réglé" 
            #         print("doss %d num %d est non réglé" %(self.index, self.patients[self.index]["Doss"]), flush=True)
            # elif key.char == ('e') or key.char == ('E'):
            #     if not self.haveToQuit:
            #         self.patients[self.index]["Type"] = "E" 
            #         print("doss %d num %d n'a pas d'écriture" %(self.index, self.patients[self.index]["Doss"]), flush=True)
        except:
            pass

    def get_input(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def __getPatients__(self):
        buf = ""
        doss = -1
        print("Entrez les dossiers des patients. Une fois fais tappez OK", flush=True)
        
        buf = input("> ")
        while buf.upper() != "OK":
            if (buf.upper() == 'P'):
                print("La dernière entré a été supprimée", flush=True)
                self.patients.pop()
            elif (buf.upper() == "PT"):
                buf = input("Etes vous sûr de vouloir tout supprimer ? O/N\n", flush=True)
                if buf == "O":
                    self.patients.clear()
                    print("Toutes les entrées on été supprimées", flush=True)
            elif len(buf) != 9:
                print("Le numéro de dossier ne fait pas 9 chiffres\nIl a été ignoré", flush=True)
            else:
                try:
                    doss = int(buf)
                    patient = {
                        "Doss": doss,
                        "Type" : "",
                        "Code" : ""
                    }
                    self.patients.append(patient)
                except:
                    print("Le numero entré n'est pas un nombre\nIl a été ignoré", flush=True)
            buf = input("> ")
        buf = input("appuyer sur entrée lorsque vous êtes prêt à tapper le dossier dans cegi\n")
        print("len du truc = ", len(self.patients), flush=True)

    def __copyToClipboard__(self, str):
        command = 'echo ' + str.strip() + '| clip'
        os.system(command)

    def __loop__(self):
        buf = ""
        pause = False
        needEscape = 1
        nbEscape = 0
        ready = False

        self.__copyToClipboard__(str(self.patients[self.index]["Doss"]))
        print("Le dossier %d a été copier dans le press-papier" %self.patients[self.index]["Doss"], flush=True)
        self.get_input()
        self.__printPatients__(True)

    def __printPatients__(self, clear=False):
        for patient in self.patients:
            print("%d -> %s\r" %(patient['Doss'], patient['Type']), flush=True)



    # def delete_last_lines(self, n=1): 
    #     for _ in range(n): 
    #         sys.stdout.write(CURSOR_UP_ONE) 
    #         sys.stdout.write(ERASE_LINE) 

    # def __getPatients__(self):
        
    #     buf = ""
    #     buff = ""
    #     doss = -1
    #     print("Entrez les dossiers des patients. Une fois fait tappez OK")

    #     while (1):
    #         buff = str(getche())
    #         buff = buff.split("'")
    #         buff = buff[1]
            
    #         if (buf == "OK" and buff == "\\r"):
    #             print()
    #             break
    #         if (buff == "\\x08"):
    #             buf = buf[:len(buf) - 1]
    #             self.delete_last_lines()
    #             print(buf, end="")
    #         elif (buff == "\\r"):
    #             print()
    #             self.__checkDoss__(buf)
    #             buf = ""
    #         else:
    #             buf += buff