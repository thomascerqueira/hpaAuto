from msvcrt import getch
from tkinter import Tk
import os

class Patients:

    patients = []

    def __getPatients__(self):
        buf = ""
        doss = -1
        print("Entrez les dossiers des patients. Une fois fais tappez OK")
        
        buf = input("> ")
        while buf.upper() != "OK":
            if (buf.upper() == 'P'):
                print("La dernière entré a été supprimée")
                self.patients.pop()
            elif (buf.upper() == "PT"):
                buf = input("Etes vous sûr de vouloir tout supprimer ? O/N\n")
                if buf == "O":
                    self.patients.clear()
                    print("Toutes les entrées on été supprimées")
            elif len(buf) != 9:
                print("Le numéro de dossier ne fait pas 9 chiffres\nIl a été ignoré")
            else:
                try:
                    doss = int(buf)
                    patient = {
                        "Doss": doss,
                        "Type" : "",
                        "R": False,
                        "S" : False,
                        "M" : False,
                        "NR": False,
                        "E" : False
                    }
                    self.patients.append(patient)
                except:
                    print("Le numero entré n'est pas un nombre\nIl a été ignoré")
            buf = input("> ")
        buf = input("appuyer sur entrée lorsque vous êtes prêt à tapper le dossier dans cegi\n")

    def __copyToClipboard__(self, str):
        command = 'echo ' + str.strip() + '| clip'
        os.system(command)

    def __loop__(self):
        buf = ""
        pause = False
        needEscape = 1
        nbEscape = 0
        index = 0

        self.__copyToClipboard__(str(self.patients[index]["Doss"]))
        print("Le dossier %d a été copier dans le press-papier" %self.patients[index]["Doss"])
        while (1):
            buf = str(getch())
            buff = buff.split("'")
            buff = buff[1]
            if (buf == "c"):
                self.__copyToClipboard__(str(self.patients[index]["Doss"]))
                print("Le dossier %d a été copier dans le press-papier" %self.patients[index]["Doss"])
            else:
                print("caca")

    def __printPatients__(self):
        for patient in self.patients:
            print("%d -> %s" %(patient['Doss'], patient['Type']))



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